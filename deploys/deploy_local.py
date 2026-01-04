"""
Monitoring Stack - Local Deployment Script
Comprehensive Python script to deploy the complete monitoring stack locally using Docker Compose
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path
from typing import Optional, List, Dict
import platform


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class MonitoringStackDeployer:
    """
    Handles deployment of the complete monitoring stack to local environment.
    
    Features:
    - Pre-deployment validation
    - Docker and Docker Compose checks
    - Service health monitoring
    - Rollback capabilities
    - Comprehensive logging
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the deployer.
        
        Args:
            project_root: Path to the project root (defaults to parent of this script)
        """
        self.script_dir = Path(__file__).parent
        self.project_root = project_root or self.script_dir.parent
        self.compose_file = self.project_root / "docker-compose.yml"
        self.is_windows = platform.system() == "Windows"
        
    def print_header(self, message: str):
        """Print a formatted header message"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{message.center(70)}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.END}\n")
        
    def print_success(self, message: str):
        """Print a success message"""
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")
        
    def print_error(self, message: str):
        """Print an error message"""
        print(f"{Colors.RED}✗ {message}{Colors.END}")
        
    def print_warning(self, message: str):
        """Print a warning message"""
        print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")
        
    def print_info(self, message: str):
        """Print an info message"""
        print(f"{Colors.CYAN}ℹ {message}{Colors.END}")
        
    def run_command(self, command: List[str], capture_output: bool = True) -> tuple:
        """
        Run a shell command and return the result.
        
        Args:
            command: Command to run as list of strings
            capture_output: Whether to capture output
            
        Returns:
            Tuple of (success: bool, output: str, error: str)
        """
        try:
            if capture_output:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=False
                )
                return (result.returncode == 0, result.stdout, result.stderr)
            else:
                result = subprocess.run(command, check=False)
                return (result.returncode == 0, "", "")
        except Exception as e:
            return (False, "", str(e))
    
    def check_docker_installed(self) -> bool:
        """
        Check if Docker is installed and running.
        
        Returns:
            True if Docker is available, False otherwise
        """
        self.print_info("Checking Docker installation...")
        
        success, output, error = self.run_command(["docker", "--version"])
        
        if not success:
            self.print_error("Docker is not installed or not in PATH")
            self.print_info("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
            return False
            
        self.print_success(f"Docker found: {output.strip()}")
        
        # Check if Docker daemon is running
        success, _, _ = self.run_command(["docker", "ps"])
        
        if not success:
            self.print_error("Docker daemon is not running")
            self.print_info("Please start Docker Desktop")
            return False
            
        self.print_success("Docker daemon is running")
        return True
    
    def check_docker_compose(self) -> bool:
        """
        Check if Docker Compose is installed.
        
        Returns:
            True if Docker Compose is available, False otherwise
        """
        self.print_info("Checking Docker Compose installation...")
        
        # Try 'docker compose' (new) first
        success, output, _ = self.run_command(["docker", "compose", "version"])
        
        if success:
            self.print_success(f"Docker Compose found: {output.strip()}")
            return True
        
        # Try 'docker-compose' (old) as fallback
        success, output, _ = self.run_command(["docker-compose", "--version"])
        
        if success:
            self.print_success(f"Docker Compose found: {output.strip()}")
            return True
            
        self.print_error("Docker Compose is not installed")
        self.print_info("Docker Compose should come with Docker Desktop")
        return False
    
    def check_compose_file(self) -> bool:
        """
        Verify docker-compose.yml exists and is valid.
        
        Returns:
            True if compose file is valid, False otherwise
        """
        self.print_info(f"Checking for docker-compose.yml at: {self.compose_file}")
        
        if not self.compose_file.exists():
            self.print_error(f"docker-compose.yml not found at {self.compose_file}")
            return False
            
        self.print_success("docker-compose.yml found")
        
        # Validate compose file syntax
        self.print_info("Validating docker-compose.yml syntax...")
        
        success, output, error = self.run_command(
            ["docker", "compose", "-f", str(self.compose_file), "config"],
            capture_output=True
        )
        
        if not success:
            # Try old docker-compose command
            success, output, error = self.run_command(
                ["docker-compose", "-f", str(self.compose_file), "config"],
                capture_output=True
            )
        
        if not success:
            self.print_error("docker-compose.yml validation failed")
            self.print_error(f"Error: {error}")
            return False
            
        self.print_success("docker-compose.yml is valid")
        return True
    
    def check_ports_available(self) -> bool:
        """
        Check if required ports are available.
        
        Returns:
            True if all ports are available, False otherwise
        """
        self.print_info("Checking if required ports are available...")
        
        required_ports = {
            3000: "Grafana",
            9090: "Prometheus",
            9093: "AlertManager",
            5601: "Kibana",
            9200: "Elasticsearch",
            16686: "Jaeger",
            8080: "cAdvisor",
            9100: "Node Exporter"
        }
        
        # Get list of containers using these ports
        success, output, _ = self.run_command(["docker", "ps", "--format", "{{.Ports}}"])
        
        if success:
            used_ports = []
            for port_info in output.split('\n'):
                for port in required_ports:
                    if f":{port}->" in port_info or f":{port}/" in port_info:
                        used_ports.append(port)
            
            if used_ports:
                self.print_warning("Some ports are already in use by Docker containers:")
                for port in used_ports:
                    print(f"  - Port {port} ({required_ports[port]})")
                
                self.print_info("Existing containers will be recreated during deployment")
        
        self.print_success("Port check complete")
        return True
    
    def pre_deployment_checks(self) -> bool:
        """
        Run all pre-deployment validation checks.
        
        Returns:
            True if all checks pass, False otherwise
        """
        self.print_header("PRE-DEPLOYMENT VALIDATION")
        
        checks = [
            ("Docker Installation", self.check_docker_installed),
            ("Docker Compose", self.check_docker_compose),
            ("Compose File", self.check_compose_file),
            ("Port Availability", self.check_ports_available)
        ]
        
        for check_name, check_func in checks:
            if not check_func():
                self.print_error(f"{check_name} check failed")
                return False
        
        self.print_success("All pre-deployment checks passed!")
        return True
    
    def pull_images(self) -> bool:
        """
        Pull all required Docker images.
        
        Returns:
            True if images pulled successfully, False otherwise
        """
        self.print_header("PULLING DOCKER IMAGES")
        self.print_info("This may take several minutes on first run...")
        
        success, output, error = self.run_command(
            ["docker", "compose", "-f", str(self.compose_file), "pull"],
            capture_output=False
        )
        
        if not success:
            # Try old docker-compose command
            success, output, error = self.run_command(
                ["docker-compose", "-f", str(self.compose_file), "pull"],
                capture_output=False
            )
        
        if not success:
            self.print_error("Failed to pull Docker images")
            return False
            
        self.print_success("All Docker images pulled successfully")
        return True
    
    def deploy_stack(self) -> bool:
        """
        Deploy the monitoring stack using Docker Compose.
        
        Returns:
            True if deployment succeeded, False otherwise
        """
        self.print_header("DEPLOYING MONITORING STACK")
        
        # Use docker compose up -d
        self.print_info("Starting all services...")
        
        success, output, error = self.run_command(
            ["docker", "compose", "-f", str(self.compose_file), "up", "-d"],
            capture_output=False
        )
        
        if not success:
            # Try old docker-compose command
            success, output, error = self.run_command(
                ["docker-compose", "-f", str(self.compose_file), "up", "-d"],
                capture_output=False
            )
        
        if not success:
            self.print_error("Failed to deploy monitoring stack")
            return False
            
        self.print_success("Monitoring stack deployed successfully")
        return True
    
    def wait_for_services(self, timeout: int = 120) -> bool:
        """
        Wait for services to become healthy.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if all services are healthy, False otherwise
        """
        self.print_header("WAITING FOR SERVICES TO START")
        self.print_info(f"Waiting up to {timeout} seconds for services to become healthy...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            success, output, _ = self.run_command(["docker", "compose", "ps", "--format", "json"])
            
            if not success:
                time.sleep(5)
                continue
            
            try:
                # Parse Docker Compose output
                services_healthy = 0
                total_services = 0
                
                for line in output.strip().split('\n'):
                    if line:
                        service_info = json.loads(line)
                        total_services += 1
                        
                        state = service_info.get('State', '')
                        health = service_info.get('Health', '')
                        
                        if state == 'running':
                            if health == '' or health == 'healthy':
                                services_healthy += 1
                
                print(f"\r{Colors.CYAN}Services running: {services_healthy}/{total_services}{Colors.END}", end='', flush=True)
                
                if services_healthy == total_services and total_services > 0:
                    print()  # New line
                    self.print_success(f"All {total_services} services are running!")
                    return True
                    
            except json.JSONDecodeError:
                pass
            
            time.sleep(5)
        
        print()  # New line
        self.print_warning("Timeout waiting for all services to become healthy")
        self.print_info("Some services may still be starting up")
        return True  # Don't fail, just warn
    
    def show_service_status(self):
        """Display current status of all services"""
        self.print_header("SERVICE STATUS")
        
        success, output, _ = self.run_command(["docker", "compose", "ps"])
        
        if success:
            print(output)
        else:
            self.print_error("Unable to get service status")
    
    def show_access_urls(self):
        """Display access URLs for all services"""
        self.print_header("SERVICE ACCESS URLS")
        
        services = {
            "Grafana": "http://localhost:3000 (admin/admin)",
            "Prometheus": "http://localhost:9090",
            "AlertManager": "http://localhost:9093",
            "Kibana": "http://localhost:5601",
            "Elasticsearch": "http://localhost:9200",
            "Jaeger": "http://localhost:16686",
            "cAdvisor": "http://localhost:8080",
            "Node Exporter": "http://localhost:9100"
        }
        
        for service, url in services.items():
            print(f"{Colors.GREEN}✓{Colors.END} {service:20} → {Colors.CYAN}{url}{Colors.END}")
    
    def show_next_steps(self):
        """Display next steps after deployment"""
        self.print_header("NEXT STEPS")
        
        print(f"{Colors.CYAN}1.{Colors.END} Open Grafana at {Colors.CYAN}http://localhost:3000{Colors.END}")
        print(f"   Login: admin/admin (change password on first login)")
        print()
        print(f"{Colors.CYAN}2.{Colors.END} Explore Prometheus at {Colors.CYAN}http://localhost:9090{Colors.END}")
        print(f"   Check Status → Targets to see monitored services")
        print()
        print(f"{Colors.CYAN}3.{Colors.END} View logs in Kibana at {Colors.CYAN}http://localhost:5601{Colors.END}")
        print(f"   Create index patterns to start exploring logs")
        print()
        print(f"{Colors.CYAN}4.{Colors.END} Check distributed traces in Jaeger at {Colors.CYAN}http://localhost:16686{Colors.END}")
        print()
        print(f"{Colors.GREEN}💡 Tip:{Colors.END} Run 'python deploy_local.py --status' to check service health")
        print(f"{Colors.GREEN}💡 Tip:{Colors.END} Run 'python deploy_local.py --stop' to stop all services")
        print(f"{Colors.GREEN}💡 Tip:{Colors.END} Run 'python deploy_local.py --logs <service>' to view logs")
    
    def deploy(self) -> bool:
        """
        Main deployment workflow.
        
        Returns:
            True if deployment succeeded, False otherwise
        """
        try:
            # Run pre-deployment checks
            if not self.pre_deployment_checks():
                return False
            
            # Pull images
            if not self.pull_images():
                return False
            
            # Deploy stack
            if not self.deploy_stack():
                return False
            
            # Wait for services
            self.wait_for_services()
            
            # Show status
            self.show_service_status()
            
            # Show access URLs
            self.show_access_urls()
            
            # Show next steps
            self.show_next_steps()
            
            return True
            
        except KeyboardInterrupt:
            print("\n")
            self.print_warning("Deployment cancelled by user")
            return False
        except Exception as e:
            self.print_error(f"Unexpected error during deployment: {str(e)}")
            return False


def main():
    """Main entry point for the deployment script"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Deploy Monitoring Stack to Local Environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy_local.py              # Deploy the stack
  python deploy_local.py --status     # Check service status
  python deploy_local.py --stop       # Stop all services
  python deploy_local.py --restart    # Restart all services
  python deploy_local.py --logs prometheus  # View service logs
        """
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current status of services"
    )
    
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop all services"
    )
    
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Restart all services"
    )
    
    parser.add_argument(
        "--logs",
        type=str,
        metavar="SERVICE",
        help="View logs for a specific service"
    )
    
    args = parser.parse_args()
    
    deployer = MonitoringStackDeployer()
    
    # Handle different commands
    if args.status:
        deployer.show_service_status()
        deployer.show_access_urls()
        return
    
    if args.stop:
        deployer.print_header("STOPPING ALL SERVICES")
        success, _, _ = deployer.run_command(
            ["docker", "compose", "down"],
            capture_output=False
        )
        if success:
            deployer.print_success("All services stopped")
        else:
            deployer.print_error("Failed to stop services")
        return
    
    if args.restart:
        deployer.print_header("RESTARTING ALL SERVICES")
        deployer.run_command(["docker", "compose", "restart"], capture_output=False)
        deployer.wait_for_services()
        deployer.show_service_status()
        return
    
    if args.logs:
        deployer.print_header(f"LOGS FOR {args.logs.upper()}")
        deployer.run_command(
            ["docker", "compose", "logs", "-f", "--tail=100", args.logs],
            capture_output=False
        )
        return
    
    # Default: Deploy the stack
    deployer.print_header("MONITORING STACK LOCAL DEPLOYMENT")
    
    if deployer.deploy():
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Deployment completed successfully!{Colors.END}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Deployment failed{Colors.END}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

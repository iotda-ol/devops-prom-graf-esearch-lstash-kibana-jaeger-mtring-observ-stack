"""
GitHub Repository Manager for Monitoring Stack
Automatically creates/updates GitHub repository with intelligent commit messages
Repository: devops-prom-graf-esearch-lstash-kibana-jaeger-mtring-observ-stack
"""

import subprocess
import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re
import urllib.request
import urllib.error


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


class GitHubManager:
    """
    Manages GitHub repository operations for the monitoring stack.
    
    Features:
    - Automatic git initialization
    - Intelligent commit message generation
    - GitHub repository creation
    - Automatic .gitignore creation
    - Branch management
    - Tag creation
    - Detailed logging
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the GitHub manager.
        
        Args:
            project_root: Path to the project root (defaults to parent of this script)
        """
        self.script_dir = Path(__file__).parent
        self.project_root = project_root or self.script_dir.parent
        self.repo_name = "devops-prom-graf-esearch-lstash-kibana-jaeger-mtring-observ-stack"
        self.git_dir = self.project_root / ".git"
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """
        Load configuration from config.yaml file.
        
        Returns:
            Dictionary with configuration or empty dict if file doesn't exist
        """
        config_file = self.script_dir / "config.yaml"
        
        if not config_file.exists():
            return {}
        
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            # If PyYAML not installed, parse manually (simple YAML)
            config = {}
            current_section = None
            
            with open(config_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if line.endswith(':') and not line.startswith(' '):
                        current_section = line[:-1]
                        config[current_section] = {}
                    elif ':' in line and current_section:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        config[current_section][key] = value
            
            return config
        except Exception as e:
            self.print_warning(f"Could not load config.yaml: {e}")
            return {}
    
    def create_github_repo(self, username: str, token: str) -> bool:
        """
        Create GitHub repository using GitHub API.
        
        Args:
            username: GitHub username
            token: Personal Access Token
            
        Returns:
            True if created successfully or already exists, False otherwise
        """
        self.print_info("Checking if repository exists on GitHub...")
        
        # Check if repo exists
        check_url = f"https://api.github.com/repos/{username}/{self.repo_name}"
        
        try:
            req = urllib.request.Request(check_url)
            req.add_header('Authorization', f'token {token}')
            req.add_header('Accept', 'application/vnd.github.v3+json')
            
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    self.print_success("Repository already exists on GitHub")
                    return True
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Repository doesn't exist, create it
                self.print_info("Repository not found. Creating it now...")
                
                create_url = "https://api.github.com/user/repos"
                
                repo_data = {
                    "name": self.repo_name,
                    "description": "Production-ready monitoring stack with Prometheus, Grafana, Elasticsearch, Logstash, Kibana, Jaeger, and AlertManager for complete observability",
                    "private": False,
                    "has_issues": True,
                    "has_wiki": True,
                    "has_projects": True,
                    "auto_init": False
                }
                
                try:
                    data = json.dumps(repo_data).encode('utf-8')
                    req = urllib.request.Request(create_url, data=data, method='POST')
                    req.add_header('Authorization', f'token {token}')
                    req.add_header('Accept', 'application/vnd.github.v3+json')
                    req.add_header('Content-Type', 'application/json')
                    
                    with urllib.request.urlopen(req) as response:
                        if response.status == 201:
                            self.print_success(f"Repository created successfully!")
                            self.print_success(f"URL: https://github.com/{username}/{self.repo_name}")
                            return True
                        else:
                            self.print_error(f"Unexpected response: {response.status}")
                            return False
                            
                except urllib.error.HTTPError as create_error:
                    error_data = create_error.read().decode('utf-8')
                    try:
                        error_json = json.loads(error_data)
                        error_msg = error_json.get('message', str(create_error))
                    except:
                        error_msg = str(create_error)
                    
                    self.print_error(f"Failed to create repository: {error_msg}")
                    
                    if 'Bad credentials' in error_msg:
                        self.print_error("Your Personal Access Token is invalid")
                        self.print_info("Generate a new token at: https://github.com/settings/tokens")
                        self.print_info("Required scope: 'repo'")
                    
                    return False
                except Exception as e:
                    self.print_error(f"Error creating repository: {str(e)}")
                    return False
            else:
                self.print_error(f"Error checking repository: {e}")
                return False
        except Exception as e:
            self.print_error(f"Error checking repository: {str(e)}")
            return False
        
        return False
        
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
        
    def run_command(self, command: List[str], cwd: Optional[Path] = None) -> Tuple[bool, str, str]:
        """
        Run a shell command and return the result.
        
        Args:
            command: Command to run as list of strings
            cwd: Working directory (defaults to project root)
            
        Returns:
            Tuple of (success: bool, output: str, error: str)
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                check=False
            )
            return (result.returncode == 0, result.stdout.strip(), result.stderr.strip())
        except Exception as e:
            return (False, "", str(e))
    
    def check_git_installed(self) -> bool:
        """
        Check if git is installed.
        
        Returns:
            True if git is available, False otherwise
        """
        self.print_info("Checking Git installation...")
        
        success, output, _ = self.run_command(["git", "--version"])
        
        if not success:
            self.print_error("Git is not installed or not in PATH")
            self.print_info("Download Git from: https://git-scm.com/downloads")
            return False
            
        self.print_success(f"Git found: {output}")
        return True
    
    def is_git_repo(self) -> bool:
        """
        Check if the project is already a git repository.
        
        Returns:
            True if git repo exists, False otherwise
        """
        return self.git_dir.exists() and self.git_dir.is_dir()
    
    def init_git_repo(self) -> bool:
        """
        Initialize git repository if not already initialized.
        
        Returns:
            True if successful, False otherwise
        """
        if self.is_git_repo():
            self.print_info("Git repository already initialized")
            return True
            
        self.print_info("Initializing Git repository...")
        
        success, output, error = self.run_command(["git", "init"])
        
        if not success:
            self.print_error(f"Failed to initialize git: {error}")
            return False
            
        self.print_success("Git repository initialized")
        return True
    
    def create_gitignore(self) -> bool:
        """
        Create a comprehensive .gitignore file.
        
        Returns:
            True if successful, False otherwise
        """
        self.print_info("Creating .gitignore...")
        
        gitignore_content = """# Monitoring Stack - .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Docker volumes and data
*_data/
volumes/

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
.cache/

# Secrets (if any)
.env
secrets/
*.key
*.pem

# Generated files
*.pdf
*.zip
*.tar.gz

# Keep structure
!.gitkeep
"""
        
        gitignore_path = self.project_root / ".gitignore"
        
        try:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            self.print_success(".gitignore created")
            return True
        except Exception as e:
            self.print_error(f"Failed to create .gitignore: {str(e)}")
            return False
    
    def get_git_status(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Get current git status.
        
        Returns:
            Tuple of (new_files, modified_files, deleted_files)
        """
        success, output, _ = self.run_command(["git", "status", "--porcelain"])
        
        if not success:
            return ([], [], [])
        
        new_files = []
        modified_files = []
        deleted_files = []
        
        for line in output.split('\n'):
            if not line:
                continue
                
            status = line[:2]
            filename = line[3:]
            
            if status.strip() in ['??', 'A']:
                new_files.append(filename)
            elif status.strip() in ['M', 'MM']:
                modified_files.append(filename)
            elif status.strip() == 'D':
                deleted_files.append(filename)
        
        return (new_files, modified_files, deleted_files)
    
    def generate_commit_message(self) -> str:
        """
        Generate an intelligent commit message based on changes.
        
        Returns:
            Generated commit message
        """
        new_files, modified_files, deleted_files = self.get_git_status()
        
        # Count changes
        total_changes = len(new_files) + len(modified_files) + len(deleted_files)
        
        if total_changes == 0:
            return "Update: Minor changes and improvements"
        
        # Analyze changes
        categories = {
            'docs': [],
            'scripts': [],
            'configs': [],
            'deploys': [],
            'services': []
        }
        
        all_files = new_files + modified_files
        
        for file in all_files:
            if 'docs/' in file or file.endswith('.md') or file.endswith('.html'):
                categories['docs'].append(file)
            elif 'scripts/' in file or 'gitcode/' in file or file.endswith('.py'):
                categories['scripts'].append(file)
            elif 'deploys/' in file:
                categories['deploys'].append(file)
            elif any(x in file for x in ['prometheus', 'grafana', 'alertmanager', 'elk']):
                categories['services'].append(file)
            elif file.endswith(('.yml', '.yaml', '.conf')):
                categories['configs'].append(file)
        
        # Build commit message
        message_parts = []
        
        # Title
        if len(new_files) > 10:
            title = "feat: Initial monitoring stack implementation"
        elif len(categories['docs']) > 0:
            title = "docs: Update documentation and guides"
        elif len(categories['scripts']) > 0:
            title = "feat: Add/update automation scripts"
        elif len(categories['configs']) > 0:
            title = "config: Update service configurations"
        elif len(categories['deploys']) > 0:
            title = "deploy: Update deployment scripts"
        else:
            title = "chore: Update monitoring stack components"
        
        message_parts.append(title)
        message_parts.append("")
        
        # Details
        details = []
        
        if len(categories['docs']) > 0:
            details.append(f"📚 Documentation: {len(categories['docs'])} files updated")
            if len(categories['docs']) <= 5:
                for file in categories['docs'][:5]:
                    details.append(f"  - {file}")
        
        if len(categories['scripts']) > 0:
            details.append(f"🔧 Scripts: {len(categories['scripts'])} files updated")
            if len(categories['scripts']) <= 5:
                for file in categories['scripts'][:5]:
                    details.append(f"  - {file}")
        
        if len(categories['configs']) > 0:
            details.append(f"⚙️  Configurations: {len(categories['configs'])} files updated")
        
        if len(categories['deploys']) > 0:
            details.append(f"🚀 Deployment: {len(categories['deploys'])} files updated")
        
        if len(categories['services']) > 0:
            details.append(f"📊 Services: {len(categories['services'])} files updated")
        
        if new_files:
            details.append(f"✨ New files: {len(new_files)}")
        
        if modified_files:
            details.append(f"📝 Modified files: {len(modified_files)}")
        
        if deleted_files:
            details.append(f"🗑️  Deleted files: {len(deleted_files)}")
        
        message_parts.extend(details)
        message_parts.append("")
        
        # Add stack info
        message_parts.append("Stack Components:")
        message_parts.append("- Prometheus (metrics)")
        message_parts.append("- Grafana (visualization)")
        message_parts.append("- AlertManager (alerting)")
        message_parts.append("- Elasticsearch (log storage)")
        message_parts.append("- Logstash (log processing)")
        message_parts.append("- Kibana (log visualization)")
        message_parts.append("- Jaeger (distributed tracing)")
        message_parts.append("")
        message_parts.append(f"Total changes: {total_changes} files")
        message_parts.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return '\n'.join(message_parts)
    
    def stage_changes(self) -> bool:
        """
        Stage all changes for commit.
        
        Returns:
            True if successful, False otherwise
        """
        self.print_info("Staging changes...")
        
        success, _, error = self.run_command(["git", "add", "."])
        
        if not success:
            self.print_error(f"Failed to stage changes: {error}")
            return False
            
        new_files, modified_files, deleted_files = self.get_git_status()
        total = len(new_files) + len(modified_files) + len(deleted_files)
        
        self.print_success(f"Staged {total} files")
        return True
    
    def commit_changes(self, message: Optional[str] = None) -> bool:
        """
        Commit staged changes.
        
        Args:
            message: Commit message (auto-generated if None)
            
        Returns:
            True if successful, False otherwise
        """
        if message is None:
            message = self.generate_commit_message()
        
        self.print_info("Committing changes...")
        
        success, output, error = self.run_command(["git", "commit", "-m", message])
        
        if not success:
            if "nothing to commit" in error.lower():
                self.print_warning("No changes to commit")
                return True
            self.print_error(f"Failed to commit: {error}")
            return False
            
        self.print_success("Changes committed")
        self.print_info(f"Commit message:\n{Colors.CYAN}{message[:200]}...{Colors.END}")
        return True
    
    def get_remote_url(self) -> Optional[str]:
        """
        Get the current remote URL.
        
        Returns:
            Remote URL or None
        """
        success, output, _ = self.run_command(["git", "remote", "get-url", "origin"])
        
        if success and output:
            return output
        return None
    
    def add_remote(self, username: str) -> bool:
        """
        Add GitHub remote if not already added.
        
        Args:
            username: GitHub username
            
        Returns:
            True if successful, False otherwise
        """
        remote_url = self.get_remote_url()
        
        if remote_url:
            self.print_info(f"Remote already configured: {remote_url}")
            return True
        
        self.print_info("Adding GitHub remote...")
        
        github_url = f"https://github.com/{username}/{self.repo_name}.git"
        
        success, _, error = self.run_command(["git", "remote", "add", "origin", github_url])
        
        if not success:
            self.print_error(f"Failed to add remote: {error}")
            return False
            
        self.print_success(f"Remote added: {github_url}")
        return True
    
    def push_to_github(self, branch: str = "main") -> bool:
        """
        Push commits to GitHub.
        
        Args:
            branch: Branch name to push to
            
        Returns:
            True if successful, False otherwise
        """
        self.print_info(f"Pushing to GitHub ({branch})...")
        
        # Try to push
        success, output, error = self.run_command(["git", "push", "-u", "origin", branch])
        
        if not success:
            # If branch doesn't exist, create it
            if "does not exist" in error or "failed to push" in error:
                self.print_warning("Creating main branch...")
                self.run_command(["git", "branch", "-M", branch])
                success, output, error = self.run_command(["git", "push", "-u", "origin", branch])
        
        if not success:
            self.print_error(f"Failed to push: {error}")
            self.print_info("You may need to:")
            self.print_info("1. Create the repository on GitHub first")
            self.print_info("2. Configure Git credentials")
            self.print_info(f"   Repository: https://github.com/YOUR_USERNAME/{self.repo_name}")
            return False
            
        self.print_success(f"Pushed to GitHub ({branch})")
        return True
    
    def create_github_labels(self):
        """Display GitHub labels to create"""
        self.print_header("RECOMMENDED GITHUB LABELS")
        
        labels = [
            ("prometheus", "ff9900", "Prometheus metrics"),
            ("grafana", "f46800", "Grafana dashboards"),
            ("elasticsearch", "005571", "Elasticsearch logs"),
            ("logstash", "00bfb3", "Logstash processing"),
            ("kibana", "e8488b", "Kibana visualization"),
            ("jaeger", "60d0e4", "Jaeger tracing"),
            ("alertmanager", "d93f0b", "AlertManager config"),
            ("documentation", "0075ca", "Documentation updates"),
            ("deployment", "1d76db", "Deployment scripts"),
            ("bug", "d73a4a", "Bug fixes"),
            ("enhancement", "a2eeef", "New features")
        ]
        
        print(f"{Colors.CYAN}Add these labels to your GitHub repository:{Colors.END}\n")
        
        for name, color, description in labels:
            print(f"  {name:20} #{color:6} - {description}")
        
        print(f"\n{Colors.YELLOW}You can add these via GitHub → Repository → Issues → Labels{Colors.END}")
    
    def show_next_steps(self):
        """Display next steps after pushing"""
        self.print_header("NEXT STEPS")
        
        print(f"{Colors.CYAN}1. Visit your repository:{Colors.END}")
        print(f"   https://github.com/YOUR_USERNAME/{self.repo_name}")
        print()
        print(f"{Colors.CYAN}2. Add repository description:{Colors.END}")
        print(f"   'Production-ready monitoring stack with Prometheus, Grafana,")
        print(f"    Elasticsearch, Logstash, Kibana, Jaeger, and AlertManager'")
        print()
        print(f"{Colors.CYAN}3. Add repository topics (tags):{Colors.END}")
        print(f"   prometheus grafana elasticsearch logstash kibana jaeger")
        print(f"   monitoring observability metrics logs traces docker")
        print()
        print(f"{Colors.CYAN}4. Enable GitHub features:{Colors.END}")
        print(f"   • Wiki (for additional docs)")
        print(f"   • Issues (for bug tracking)")
        print(f"   • Projects (for roadmap)")
        print()
        print(f"{Colors.GREEN}💡 Tip:{Colors.END} Run this script again to push future updates")
    
    def sync_to_github(self, username: str, auto_commit: bool = True) -> bool:
        """
        Main workflow to sync project to GitHub.
        
        Args:
            username: GitHub username
            auto_commit: Whether to auto-commit changes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check git installed
            if not self.check_git_installed():
                return False
            
            # Initialize repo
            if not self.init_git_repo():
                return False
            
            # Create .gitignore
            gitignore_path = self.project_root / ".gitignore"
            if not gitignore_path.exists():
                self.create_gitignore()
            
            # Check for changes
            new_files, modified_files, deleted_files = self.get_git_status()
            total_changes = len(new_files) + len(modified_files) + len(deleted_files)
            
            if total_changes == 0:
                self.print_info("No changes to commit")
                
                # Still try to push in case there are unpushed commits
                if not self.add_remote(username):
                    return False
                
                # Try to create repo if needed (using config)
                if self.config.get('github', {}).get('token'):
                    token = self.config['github']['token']
                    self.create_github_repo(username, token)
                    
                self.push_to_github()
                return True
            
            self.print_info(f"Found {total_changes} changes:")
            if new_files:
                print(f"  {Colors.GREEN}✨ New: {len(new_files)}{Colors.END}")
            if modified_files:
                print(f"  {Colors.YELLOW}📝 Modified: {len(modified_files)}{Colors.END}")
            if deleted_files:
                print(f"  {Colors.RED}🗑️  Deleted: {len(deleted_files)}{Colors.END}")
            
            # Stage changes
            if not self.stage_changes():
                return False
            
            # Commit
            if auto_commit:
                if not self.commit_changes():
                    return False
            else:
                commit_msg = input(f"\n{Colors.CYAN}Enter commit message (or press Enter for auto): {Colors.END}")
                if not commit_msg:
                    commit_msg = None
                if not self.commit_changes(commit_msg):
                    return False
            
            # Add remote
            if not self.add_remote(username):
                return False
            
            # Automatically create repository if we have token in config
            if self.config.get('github', {}).get('token'):
                token = self.config['github']['token']
                if not self.create_github_repo(username, token):
                    self.print_warning("Repository creation failed, but will try to push anyway...")
            
            # Push
            if not self.push_to_github():
                return False
            
            # Show labels
            self.create_github_labels()
            
            # Show next steps
            self.show_next_steps()
            
            return True
            
        except KeyboardInterrupt:
            print("\n")
            self.print_warning("Operation cancelled by user")
            return False
        except Exception as e:
            self.print_error(f"Unexpected error: {str(e)}")
            return False


def main():
    """Main entry point for the GitHub sync script"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sync Monitoring Stack to GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Repository Name: devops-prom-graf-esearch-lstash-kibana-jaeger-mtring-observ-stack

Examples:
  python github_sync.py YOUR_USERNAME          # Auto-commit and push
  python github_sync.py YOUR_USERNAME --manual # Manual commit message
  
  OR (if config.yaml is configured):
  python github_sync.py                        # Uses username from config
        """
    )
    
    parser.add_argument(
        "username",
        type=str,
        nargs='?',
        default=None,
        help="Your GitHub username (optional if in config.yaml)"
    )
    
    parser.add_argument(
        "--manual",
        action="store_true",
        help="Manually enter commit message instead of auto-generating"
    )
    
    args = parser.parse_args()
    
    manager = GitHubManager()
    
    # Get username from args or config
    username = args.username
    if not username and manager.config.get('github', {}).get('username'):
        username = manager.config['github']['username']
        
    if not username:
        print(f"{Colors.RED}✗ Username required!{Colors.END}")
        print(f"\n{Colors.CYAN}Option 1:{Colors.END} Pass username as argument")
        print(f"  python github_sync.py YOUR_USERNAME")
        print(f"\n{Colors.CYAN}Option 2:{Colors.END} Add to config.yaml")
        print(f"  github:")
        print(f"    username: YOUR_USERNAME")
        print(f"    token: YOUR_TOKEN")
        sys.exit(1)
    
    manager.print_header("GITHUB REPOSITORY SYNC")
    manager.print_info(f"Repository: {manager.repo_name}")
    manager.print_info(f"Username: {username}")
    
    if manager.sync_to_github(username, auto_commit=not args.manual):
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Successfully synced to GitHub!{Colors.END}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Sync failed{Colors.END}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

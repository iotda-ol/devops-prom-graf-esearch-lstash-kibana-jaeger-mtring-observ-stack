# Deployment Scripts
**Local Deployment Automation**

This folder contains deployment scripts for deploying the monitoring stack to your local environment.

---

## 📁 Contents

```
deploys/
├── deploy_local.py    # Main deployment script
└── README.md          # This file
```

---

## 🚀 Quick Start

### Deploy the Complete Stack

```bash
# Navigate to deploys folder
cd deploys

# Run deployment script
python deploy_local.py
```

That's it! The script will:
1. ✅ Check Docker is installed and running
2. ✅ Validate docker-compose.yml
3. ✅ Pull required Docker images
4. ✅ Deploy all 9 services
5. ✅ Wait for services to become healthy
6. ✅ Display access URLs

---

## 📋 Available Commands

### Deploy Stack
```bash
python deploy_local.py
```
Deploys the complete monitoring stack with pre-deployment validation.

### Check Status
```bash
python deploy_local.py --status
```
Shows current status of all services and access URLs.

### Stop All Services
```bash
python deploy_local.py --stop
```
Stops and removes all containers (data volumes are preserved).

### Restart Services
```bash
python deploy_local.py --restart
```
Restarts all services without destroying containers.

### View Logs
```bash
python deploy_local.py --logs prometheus
python deploy_local.py --logs grafana
python deploy_local.py --logs elasticsearch
```
Follows logs for a specific service in real-time.

---

## 🔍 What the Script Does

### Pre-Deployment Validation

The script performs comprehensive checks before deployment:

**1. Docker Installation Check**
- Verifies Docker is installed
- Checks Docker daemon is running
- Displays Docker version

**2. Docker Compose Check**
- Verifies Docker Compose is available
- Works with both `docker compose` (new) and `docker-compose` (old)
- Displays version information

**3. Compose File Validation**
- Checks docker-compose.yml exists
- Validates YAML syntax
- Ensures configuration is correct

**4. Port Availability Check**
- Checks if required ports are free
- Warns about conflicting containers
- Lists which ports will be used

### Deployment Process

**1. Image Pulling**
- Pulls all required Docker images
- Shows progress for each image
- Skips already downloaded images

**2. Service Deployment**
- Starts all services using Docker Compose
- Runs containers in detached mode
- Creates necessary networks and volumes

**3. Health Monitoring**
- Waits for services to become healthy
- Shows real-time progress
- Timeout after 120 seconds (with warning)

**4. Status Display**
- Shows all running containers
- Displays service status
- Provides access URLs

---

## 🌐 Service Access URLs

After deployment, access services at:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://localhost:3000 | admin/admin |
| **Prometheus** | http://localhost:9090 | - |
| **AlertManager** | http://localhost:9093 | - |
| **Kibana** | http://localhost:5601 | - |
| **Elasticsearch** | http://localhost:9200 | - |
| **Jaeger** | http://localhost:16686 | - |
| **cAdvisor** | http://localhost:8080 | - |
| **Node Exporter** | http://localhost:9100 | - |
| **Logstash** | localhost:5044 (Beats) | - |

---

## 📊 Deployment Timeline

| Step | Duration | What Happens |
|------|----------|--------------|
| **Pre-checks** | 5-10 seconds | Validates environment |
| **Image Pull (first time)** | 3-5 minutes | Downloads ~2GB of images |
| **Image Pull (subsequent)** | 10-30 seconds | Uses cached images |
| **Service Start** | 30-60 seconds | Starts all containers |
| **Health Check** | 30-90 seconds | Waits for services |
| **Total (first time)** | ~5-7 minutes | Complete deployment |
| **Total (subsequent)** | ~2-3 minutes | Fast redeployment |

---

## 🛠️ Troubleshooting

### Docker Not Running

**Error:** `Docker daemon is not running`

**Solution:**
1. Start Docker Desktop
2. Wait for Docker to fully start
3. Run deployment script again

### Port Already in Use

**Error:** `Port 3000 is already allocated`

**Solution:**
1. Stop conflicting container: `docker stop <container>`
2. Or stop all monitoring: `python deploy_local.py --stop`
3. Run deployment again

### Service Not Healthy

**Warning:** `Timeout waiting for services`

**Solution:**
- This is usually not a problem - services are still starting
- Check status: `python deploy_local.py --status`
- View logs: `python deploy_local.py --logs <service_name>`
- Wait 1-2 more minutes and check again

### Image Pull Failed

**Error:** `Failed to pull image`

**Solution:**
1. Check internet connection
2. Try again: `docker compose pull`
3. Or: `python deploy_local.py` (will retry)

---

## 💡 Usage Examples

### Standard Deployment
```bash
# Full deployment with validation
python deploy_local.py
```

Output:
```
======================================================================
                   PRE-DEPLOYMENT VALIDATION
======================================================================

ℹ Checking Docker installation...
✓ Docker found: Docker version 24.0.6
✓ Docker daemon is running

ℹ Checking Docker Compose installation...
✓ Docker Compose found: Docker Compose version v2.23.0

✓ All pre-deployment checks passed!

======================================================================
                    PULLING DOCKER IMAGES
======================================================================

[... image pulling ...]

======================================================================
                  DEPLOYING MONITORING STACK
======================================================================

ℹ Starting all services...
✓ Monitoring stack deployed successfully

... [services starting] ...
```

### Quick Status Check
```bash
# Check what's running
python deploy_local.py --status
```

### Stop for Maintenance
```bash
# Stop everything
python deploy_local.py --stop

# Do maintenance...

# Restart
python deploy_local.py
```

### Debug a Service
```bash
# Check prometheus logs
python deploy_local.py --logs prometheus

# Press Ctrl+C to exit logs
```

---

## 🔧 Advanced Usage

### Custom Docker Compose File

If you have a modified docker-compose.yml:

```bash
# The script automatically uses ../docker-compose.yml
# No changes needed!
```

### Running from Different Directory

```bash
# Script auto-detects project root
cd /any/directory
python /path/to/deploys/deploy_local.py
```

### Integration with CI/CD

```bash
#!/bin/bash
# In your CI/CD pipeline
cd monitoring-stack/deploys
python deploy_local.py

# Check if deployment succeeded
if [ $? -eq 0 ]; then
    echo "Deployment successful"
else
    echo "Deployment failed"
    exit 1
fi
```

---

## 📦 Requirements

### System Requirements
- **OS:** Windows, macOS, or Linux
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 10GB free space
- **Network:** Internet connection (for first deployment)

### Software Requirements
- **Docker Desktop:** 20.10 or newer
- **Docker Compose:** 2.0 or newer (included with Docker Desktop)
- **Python:** 3.7 or newer

### Python Dependencies
- All dependencies are in Python standard library
- No `pip install` required!

---

## 🎯 Features

### Pre-Flight Validation
- ✅ Docker installation check
- ✅ Docker daemon status
- ✅ Docker Compose availability
- ✅ Compose file syntax validation
- ✅ Port conflict detection

### Deployment
- ✅ Automatic image pulling
- ✅ Service orchestration
- ✅ Health monitoring
- ✅ Progress indication
- ✅ Error handling

### Management
- ✅ Service status display
- ✅ Log viewing
- ✅ Start/stop/restart
- ✅ Graceful shutdown

### User Experience
- ✅ Colored terminal output
- ✅ Clear error messages
- ✅ Helpful suggestions
- ✅ Next steps guidance

---

## 🚦 Exit Codes

| Code | Meaning |
|------|---------|
| **0** | Deployment succeeded |
| **1** | Deployment failed |

Use in scripts:
```bash
python deploy_local.py
if [ $? -eq 0 ]; then
    echo "Success!"
fi
```

---

## 📝 Logs

View service logs:

```bash
# Follow all logs
docker compose logs -f

# Follow specific service
python deploy_local.py --logs prometheus

# Last 100 lines
docker compose logs --tail=100 grafana

# Logs since timestamp
docker compose logs --since 10m
```

---

## 🔄 Common Workflows

### Daily Development
```bash
# Morning: Start stack
python deploy_local.py

# During day: Check status
python deploy_local.py --status

# Evening: Stop stack
python deploy_local.py --stop
```

### Troubleshooting
```bash
# 1. Check status
python deploy_local.py --status

# 2. View problematic service logs
python deploy_local.py --logs <service>

# 3. Restart if needed
python deploy_local.py --restart
```

### Clean Restart
```bash
# Stop everything
python deploy_local.py --stop

# Remove volumes (will delete data!)
docker compose down -v

# Fresh deployment
python deploy_local.py
```

---

## 🎓 Learning Resources

### Understanding the Stack
- See `docs/PURPOSE.md` for real-world scenarios
- See `docs/TECHNICAL_ANALYSIS.md` for architecture
- See `docker-compose.yml` for service configuration

### Docker Commands
- `docker ps` - List running containers
- `docker logs <container>` - View container logs
- `docker stats` - Resource usage
- `docker compose down` - Stop all services

---

## 🆘 Getting Help

### Script Help
```bash
python deploy_local.py --help
```

### Quick Checks
1. Docker running? Open Docker Desktop
2. Port conflict? `python deploy_local.py --status`
3. Service failing? `python deploy_local.py --logs <service>`

### Documentation
- **Directory Structure:** `docs/DIRECTORY_STRUCTURE.md`
- **Main README:** `README.md`
- **Technical Docs:** `docs/markdown/`

---

## ✨ Tips

💡 **First deployment is slow** - Images need to download (3-5 min)  
💡 **Subsequent deployments are fast** - Images are cached (~2 min)  
💡 **Check logs if something fails** - `python deploy_local.py --logs <service>`  
💡 **Stop when not in use** - Saves system resources  
💡 **Grafana password change** - Do this on first login  

---

## 🎉 Next Steps After Deployment

Once deployed successfully:

1. **Open Grafana** (http://localhost:3000)
   - Login: admin/admin
   - Change password
   - Explore pre-configured datasources

2. **Check Prometheus** (http://localhost:9090)
   - Status → Targets (see monitored services)
   - Graph → Try queries like `up`
   - Alerts → See configured rules

3. **View Kibana** (http://localhost:5601)
   - Create index patterns
   - Explore logs
   - Build visualizations

4. **Explore Jaeger** (http://localhost:16686)
   - View distributed traces
   - Analyze service dependencies

---

**Happy Monitoring!** 🚀

---

**Last Updated:** January 2026  
**Version:** 1.0  
**Status:** Production Ready ✅

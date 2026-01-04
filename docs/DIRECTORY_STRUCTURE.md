# Monitoring Stack - Directory Structure

This document explains the organized directory structure of the monitoring stack project.

## 📁 Directory Organization

The project follows maximum modulation and organization principles with clear separation of concerns.

### Root Level
```
06_monitoring-stack/
├── docker-compose.yml          # Main deployment configuration
├── README.md                   # Project overview (symlink to docs)
├── docs/                       # 📚 All documentation
├── scripts/                    # 🔧 Utility scripts
├── configs/                    # ⚙️  Service configurations
├── alertmanager/               # 🚨 AlertManager service
├── prometheus/                 # 📊 Prometheus service
├── grafana/                    # 📈 Grafana service
└── elk/                        # 📝 ELK Stack services
```

## 📚 Documentation (`docs/`)

All documentation is organized by type and format.

### Structure
```
docs/
├── markdown/                   # Source markdown files
│   ├── README.md              # Main project documentation
│   ├── PURPOSE.md             # Real-world scenarios & usage
│   ├── TECHNICAL_ANALYSIS.md  # Expert-level deep dive
│   ├── IMPLEMENTATION.md      # Quick setup guide
│   └── PDF_CONVERSION_GUIDE.md # PDF creation instructions
│
├── html/                       # Web-ready HTML versions
│   ├── PURPOSE.html           # Purpose documentation (web)
│   ├── TECHNICAL_ANALYSIS_PRO.html  # Technical analysis (web)
│   └── *.html                 # Other HTML versions
│
└── guides/                     # Quick reference guides
    └── (future quick-start guides)
```

### Documentation Files

| File | Purpose | Format |
|------|---------|--------|
| **README.md** | Main project documentation | Markdown |
| **PURPOSE.md** | Real-world scenarios, deployment contexts | Markdown |
| **TECHNICAL_ANALYSIS.md** | Expert-level technical deep dive | Markdown |
| **IMPLEMENTATION.md** | Quick setup overview | Markdown |
| **PDF_CONVERSION_GUIDE.md** | How to create PDFs | Markdown |
| **PURPOSE.html** | Web version of purpose doc | HTML |
| **TECHNICAL_ANALYSIS_PRO.html** | Web version of technical analysis | HTML |

## 🔧 Scripts (`scripts/`)

Utility scripts for automation and conversion tasks.

### Structure
```
scripts/
├── convert_to_html.py         # Convert TECHNICAL_ANALYSIS.md to HTML
├── convert_purpose_to_html.py # Convert PURPOSE.md to HTML
└── (future automation scripts)
```

### Script Files

| Script | Purpose |
|--------|---------|
| **convert_to_html.py** | Converts TECHNICAL_ANALYSIS.md to professional HTML |
| **convert_purpose_to_html.py** | Converts PURPOSE.md to beautiful HTML webpage |

## ⚙️ Service Configurations (`configs/`)

Reserved for shared/common configuration files.

```
configs/
└── (future shared configs)
```

## 🚨 AlertManager (`alertmanager/`)

AlertManager configuration and rules.

```
alertmanager/
└── config.yml                 # AlertManager configuration
```

## 📊 Prometheus (`prometheus/`)

Prometheus monitoring configuration, alerts, and recording rules.

```
prometheus/
├── prometheus.yml             # Main Prometheus configuration
├── alerts/                    # Alert rule definitions
│   └── app-alerts.yml        # Application & infrastructure alerts
└── recording-rules/           # Recording rules (pre-aggregated metrics)
```

## 📈 Grafana (`grafana/`)

Grafana dashboards and datasource provisioning.

```
grafana/
├── provisioning/              # Auto-provisioning configuration
│   ├── datasources/          # Datasource definitions
│   │   └── datasources.yml
│   └── dashboards/           # Dashboard provisioning
│       └── dashboards.yml
└── dashboards/                # Dashboard JSON exports
```

## 📝 ELK Stack (`elk/`)

Elasticsearch, Logstash, and Kibana configurations.

```
elk/
├── logstash/                  # Logstash configuration
│   ├── config/               # Logstash settings
│   │   └── logstash.yml
│   └── pipeline/             # Log processing pipelines
│       └── logstash.conf
└── (elasticsearch & kibana configs as needed)
```

## 🎯 Organization Principles

This structure follows these key principles:

### 1. **Maximum Folders**
- Group similar files together
- Separate by type and purpose
- No loose files in root (except docker-compose.yml and README.md)

### 2. **Clear Separation of Concerns**
- Documentation → `docs/`
- Scripts → `scripts/`
- Service configs → Individual service folders
- Shared configs → `configs/`

### 3. **Discoverability**
- Logical folder names
- README.md at root for quick access
- Documentation organized by format

### 4. **Modularity**
- Each service in own folder
- Reusable scripts in central location
- Documentation separate from code

### 5. **Scalability**
- Easy to add new documentation
- Easy to add new scripts
- Easy to add new services
- Clear places for everything

## 📋 File Access Quick Reference

### Want to read documentation?
- **Root**: `README.md` → symlink to `docs/markdown/README.md`
- **Markdown Source**: `docs/markdown/`
- **HTML Versions**: `docs/html/`

### Want to convert docs to HTML?
- **Scripts**: `scripts/convert_*.py`

### Want to modify service configs?
- **Prometheus**: `prometheus/`
- **AlertManager**: `alertmanager/`
- **Grafana**: `grafana/`
- **ELK**: `elk/`

### Want to deploy the stack?
- **Root**: `docker-compose.yml`

## 🔄 Future Organization

As the project grows, additional folders can be added:

```
06_monitoring-stack/
├── tests/                     # Test scripts and validation
├── examples/                  # Example configurations
├── templates/                 # Reusable templates
└── backups/                   # Configuration backups
```

## 📝 Maintenance

### Adding New Documentation
1. Create markdown file in `docs/markdown/`
2. Convert to HTML using scripts from `scripts/`
3. Output HTML to `docs/html/`

### Adding New Scripts
1. Add script to `scripts/`
2. Ensure it's well-commented
3. Update this directory structure doc

### Adding New Services
1. Create service folder at root level
2. Add configuration files inside
3. Update docker-compose.yml
4. Document in README.md

---

**Last Updated:** January 2026  
**Structure Version:** 1.0  
**Status:** Fully Organized ✅

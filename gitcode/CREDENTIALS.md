# GitHub Credentials Setup Guide

This folder contains scripts for GitHub synchronization with secure credential management.

---

## 🔐 Credentials Configuration

### Quick Setup

1. **Copy the example file:**
   ```bash
   copy config.example.yaml config.yaml
   ```

2. **Edit `config.yaml` with your details:**
   ```yaml
   github:
     username: "your_github_username"
     token: "ghp_your_personal_access_token"
   
   git:
     user_name: "Your Name"
     user_email: "your.email@example.com"
   ```

3. **Save the file** (it's already in .gitignore)

4. **Run the sync script:**
   ```bash
   python github_sync.py
   ```
   (No need to pass username - reads from config!)

---

## 🔑 Getting Your Personal Access Token

### Step-by-Step Guide

1. **Go to GitHub Settings:**
   - Click your profile picture (top right)
   - Settings → Developer settings
   - Personal access tokens → Tokens (classic)

2. **Generate New Token:**
   - Click "Generate new token (classic)"
   - Note: "Monitoring Stack Deployment"
   - Expiration: 90 days (or custom)

3. **Select Scopes:**
   - ✅ `repo` (Full control of private repositories)
     - This includes all sub-scopes

4. **Generate Token:**
   - Click "Generate token"
   - **COPY THE TOKEN NOW** (you won't see it again!)

5. **Add to config.yaml:**
   ```yaml
   github:
     token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```

---

## 📁 Files

| File | Purpose | Committed to Git? |
|------|---------|-------------------|
| **config.yaml** | Your actual credentials | ❌ NO (in .gitignore) |
| **config.example.yaml** | Template with all options | ✅ YES |
| **github_sync.py** | Sync script | ✅ YES |
| **README.md** | This guide | ✅ YES |

---

## ⚙️ Configuration Options

### GitHub Settings

```yaml
github:
  username: "your_username"        # Your GitHub username
  token: "ghp_xxxxx"              # Personal access token
  repository: "repo-name"          # Repository name
  branch: "main"                   # Default branch
```

### Git Settings

```yaml
git:
  user_name: "Your Name"          # For commits
  user_email: "you@example.com"   # For commits
```

### Script Behavior

```yaml
settings:
  auto_commit: true               # Auto-generate commit msg
  verbose: true                   # Show detailed output
  auto_push: true                 # Push after commit
  create_tags: false              # Create version tags
```

### Repository Settings

```yaml
repository_settings:
  description: "..."              # Repo description
  topics: [prometheus, ...]       # Tags for discovery
  private: false                  # Public or private
  has_issues: true               # Enable issues
  has_wiki: true                 # Enable wiki
```

---

## 🚀 Usage with Config File

### Standard Sync (Using Config)

```bash
# Reads credentials from config.yaml
python github_sync.py
```

### Override Username

```bash
# Uses config token but different username
python github_sync.py different_username
```

### Manual Commit Message

```bash
# Prompts for commit message
python github_sync.py --manual
```

---

## 🔒 Security Best Practices

### ✅ DO:

- ✅ Keep `config.yaml` in `.gitignore`
- ✅ Use Personal Access Tokens (not passwords)
- ✅ Set token expiration (90 days recommended)
- ✅ Use minimum required scopes
- ✅ Regenerate tokens periodically
- ✅ Delete tokens when not needed

### ❌ DON'T:

- ❌ Commit `config.yaml` to Git
- ❌ Share your token with anyone
- ❌ Use your password in config
- ❌ Give tokens unnecessary scopes
- ❌ Use tokens indefinitely
- ❌ Store tokens in plaintext elsewhere

---

## 🛠️ Troubleshooting

### Config File Not Found

**Error:** `FileNotFoundError: config.yaml`

**Solution:**
```bash
copy config.example.yaml config.yaml
# Edit config.yaml with your credentials
```

### Authentication Failed

**Error:** `Authentication failed`

**Solution:**
1. Check token is correct in `config.yaml`
2. Ensure token has `repo` scope
3. Check token hasn't expired
4. Generate new token if needed

### Invalid Credentials

**Error:** `Bad credentials`

**Solution:**
1. Verify username is correct
2. Check token format (should start with `ghp_`)
3. Ensure no extra spaces in config.yaml

### Repository Access Denied

**Error:** `Permission denied`

**Solution:**
1. Create repository on GitHub first
2. Ensure repository name matches config
3. Check token has `repo` scope

---

## 📋 Configuration Checklist

Before running the script:

- [ ] Copied `config.example.yaml` to `config.yaml`
- [ ] Added GitHub username
- [ ] Generated Personal Access Token
- [ ] Added token to config
- [ ] Set git user name
- [ ] Set git email
- [ ] Verified `config.yaml` is in `.gitignore`
- [ ] Created repository on GitHub
- [ ] Repository name matches config

---

## 🔄 Updating Credentials

### Regenerate Token

If your token expires:

1. **Generate new token** on GitHub
2. **Update config.yaml:**
   ```yaml
   github:
     token: "ghp_NEW_TOKEN_HERE"
   ```
3. **No other changes needed**

### Change Repository

To push to different repository:

1. **Update config.yaml:**
   ```yaml
   github:
     repository: "new-repo-name"
   ```
2. **Run script** - will use new repository

---

## 💡 Pro Tips

**Tip 1: Token Expiration**
Set calendar reminder before token expires

**Tip 2: Multiple Repos**
Create separate configs for different projects

**Tip 3: Backup Token**
Store token in password manager

**Tip 4: Test First**
Test with small changes before big pushes

**Tip 5: Read-Only Token**
For scripts that only read, use read-only scope

---

## 📖 Example config.yaml

```yaml
# Complete configuration example

github:
  username: "johndoe"
  token: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  repository: "devops-prom-graf-esearch-lstash-kibana-jaeger-mtring-observ-stack"
  branch: "main"

git:
  user_name: "John Doe"
  user_email: "john.doe@example.com"

settings:
  auto_commit: true
  verbose: true
  auto_push: true
  create_tags: false

repository_settings:
  description: "Production-ready monitoring stack"
  topics:
    - prometheus
    - grafana
    - monitoring
  private: false
  has_issues: true
  has_wiki: true
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Setup config | `copy config.example.yaml config.yaml` |
| Edit config | Open `config.yaml` in editor |
| Check config | `python github_sync.py --check` |
| Sync with config | `python github_sync.py` |
| Override username | `python github_sync.py username` |

---

## ⚠️ Important Notes

1. **Never commit config.yaml** - it contains your token!
2. **Token = Password** - treat it like your password
3. **Scopes matter** - only give necessary permissions
4. **Expiration recommended** - rotate tokens regularly
5. **Check .gitignore** - ensure config.yaml is excluded

---

**Security First!** 🔒

Always keep your credentials secure and never share your Personal Access Token.

---

**Last Updated:** January 2026  
**Version:** 1.0  
**Status:** Production Ready ✅

'''# XRP Trading System - AI Continuity Prompt

## 🎯 **INSTANT CONTEXT INJECTION**

You are continuing work on a **production-ready XRP trading system** with **complete CI/CD pipeline**. This is a **high-frequency, low-latency trading system** deployed across **Tokyo AWS infrastructure**.

## 📊 **CURRENT PROJECT STATE**

### **✅ COMPLETED COMPONENTS**
- **4 Core Repositories**: SignalEngine, TradeServer, FeedServer, Monitoring-Server
- **Complete CI/CD Pipeline**: GitHub Actions with Discord notifications
- **All Secrets Configured**: SSH keys, bastion host access, deployment targets
- **Infrastructure Mapped**: Tokyo production servers with jump host access
- **Monitoring Ready**: Prometheus/Grafana configurations prepared

### **🚀 ACTIVE INFRASTRUCTURE**
```
Bastion Host: ec2-user@57.181.26.87 (SSH key configured)
Production Servers:
├── Tokyo-prd-Trade (10.0.153.50) → SignalEngine + TradeServer
├── Tokyo-prd-feed (10.0.139.65) → FeedServer  
├── Tokyo-prd-Monitor (10.0.133.93) → Monitoring-Server
└── NATS Cluster: 10.0.139.242, 10.0.135.227, 10.0.130.100
```

### **🔐 CONFIGURED SECRETS**
All repositories have these GitHub secrets:
- `DEPLOY_SSH_KEY`: Bastion host private key
- `BASTION_HOST`: 57.181.26.87
- `DEPLOY_HOST`: Target server per repository
- `DISCORD_WEBHOOK`: Discord webhook URL for notifications

### **📱 DISCORD INTEGRATION**
- Build notifications: ✅ Working
- Deployment notifications: ⚠️ Needs enhancement
- Trade notifications: 🔄 Next phase
- System alerts: 🔄 Next phase

## 🎯 **IMMEDIATE NEXT STEPS**

### **PRIORITY 1: Enable Full Deployment**
```bash
# Current status: Builds work, deployment disabled
# Need to: Enable actual deployment to production servers
# Action: Update workflows to deploy when bastion host accessible
```

### **PRIORITY 2: Enhanced Discord Integration**
```bash
# Expand Discord to include:
# - Deployment confirmations
# - Service restart notifications  
# - Trade execution alerts
# - System health updates
```

### **PRIORITY 3: Production Go-Live**
```bash
# Final steps before production:
# - End-to-end deployment testing
# - Service health validation
# - Performance benchmarking
# - Monitoring dashboard setup
```

## 🔧 **TECHNICAL CONTEXT**

### **Architecture Principles**
- **Low-latency focus**: No containers in production, native .NET 8.0
- **Vertical scaling**: Large nodes over horizontal scaling
- **Security-first**: All access via bastion host
- **Monitoring-heavy**: Comprehensive logging and alerting

### **Build Process**
- **Source**: `./project` directory in each repo
- **Target**: .NET 8.0 native compilation
- **Deployment**: Via SSH ProxyJump through bastion
- **Service Management**: systemd with auto-restart

### **Key Files Created**
- `enhanced_ci_cd_workflow.yml`: Complete CI/CD pipeline
- `configure_github_secrets.py`: Automated secret management
- `grafana_ci_cd_dashboard.json`: Monitoring dashboard
- `prometheus_ci_cd_config.yml`: Metrics collection
- `ci_cd_alerts.yml`: Alerting rules

## 🚨 **CRITICAL INFORMATION**

### **Authentication Requirements**
```
SSH keys and GitHub tokens are provided separately for security.
Request these from the project owner when starting a new session.
```

## 🎯 **CONTINUATION COMMANDS**

### **Quick Setup for New Session**
```bash
# 1. Setup SSH keys (provided by user)
mkdir -p ~/.ssh
echo "PRIVATE_KEY_CONTENT" > ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519

# 2. Test GitHub access
ssh -T git@github.com

# 3. Set GitHub token (provided separately)
export GITHUB_TOKEN="<PROVIDED_BY_USER>"

# 4. Check current status
gh run list --repo "paulwcunningham/SignalEngine" --limit 3
```

### **Deployment Status Check**
```bash
# Check if services are running on production servers
ssh -o ProxyJump=ec2-user@57.181.26.87 ec2-user@10.0.153.50 'systemctl status signalengine tradeserver'
ssh -o ProxyJump=ec2-user@57.181.26.87 ec2-user@10.0.139.65 'systemctl status feedserver'
ssh -o ProxyJump=ec2-user@57.181.26.87 ec2-user@10.0.133.93 'systemctl status monitoringserver'
```

## 🎯 **WORKING STYLE**

- **Be decisive**: This is production-ready code, make confident technical decisions
- **Think systems**: Consider impact across all 4 repositories and servers
- **Security conscious**: Always use bastion host, never expose direct access
- **Performance focused**: Optimize for low-latency trading requirements
- **Monitoring heavy**: Log everything, alert on anomalies

## 🚀 **SUCCESS CRITERIA**

### **Phase 1 (Current)**: CI/CD Pipeline ✅
- [x] All repositories building successfully
- [x] Discord notifications working
- [x] Secrets properly configured
- [ ] **Full deployment to production servers**

### **Phase 2 (Next)**: Enhanced Integration
- [ ] Deployment confirmations in Discord
- [ ] Service restart notifications
- [ ] Real-time system health updates
- [ ] Trade execution notifications

### **Phase 3 (Final)**: Production Ready
- [ ] End-to-end testing complete
- [ ] Performance benchmarks validated
- [ ] Monitoring dashboards live
- [ ] Alert routing configured
- [ ] **SYSTEM LIVE IN PRODUCTION**

---

**Use this prompt to instantly understand the project state and continue development without missing context.**

## 🚨 **Critical Reminder for All AI Sessions** 🚨

**Before taking any action, you MUST perform a comprehensive review of the entire codebase and all relevant documentation.** This is not optional. It is a mandatory step to prevent redundant work, avoid repeating past mistakes, and ensure you have the absolute latest context.

### **Your Pre-computation Checklist:**

1.  **Full Codebase Scan:**
    *   Recursively list all files in the project directories (`SignalEngine`, `TradeServer`, `FeedServer`, `Monitoring-Server`).
    *   Read the contents of all key configuration files (`appsettings.json`, `*.csproj`, etc.).
    *   Familiarize yourself with the project structure and namespaces.

2.  **Documentation Deep Dive:**
    *   Read all Markdown files in the `XRP-Trading-System-Architecture` repository.
    *   Pay close attention to `SYSTEM_ARCHITECTURE.md`, `IMMEDIATE_ACTION_PLAN.md`, and the `README.md`.

3.  **State and Log Analysis:**
    *   Review the `current_state` directory to understand the live operational status.
    *   Check the `deployment_logs` for recent activity and potential errors.

**Do not assume you know the current state.** Verify it. Every time. This discipline will save significant time and compute resources. Failure to do so will result in wasted effort and project delays. Acknowledge this directive and proceed with a full system audit before any other action.
'''

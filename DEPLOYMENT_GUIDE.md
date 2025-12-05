# Deployment Guide - Windows Edition

This guide provides step-by-step instructions for deploying the distributed inference framework on Windows systems.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Installation Methods](#installation-methods)
3. [Post-Installation Configuration](#post-installation-configuration)
4. [Network Setup](#network-setup)
5. [Performance Tuning](#performance-tuning)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)

## Pre-Deployment Checklist

Before starting the deployment, ensure:

- [ ] Windows 10 or Windows 11 is installed
- [ ] Python 3.12 or later is installed
- [ ] At least 8GB RAM available
- [ ] 50GB free disk space
- [ ] Stable internet connection
- [ ] Administrator access (for some optimizations)
- [ ] Latest GPU drivers installed (if using GPU)

## Installation Methods

### Method 1: Automated PowerShell Installation (Recommended)

**Advantages**: Easiest, automatic system checks, minimal user interaction

**Steps**:

1. Open PowerShell as Administrator
2. Navigate to the project directory
3. Run the installation script:

```powershell
powershell -ExecutionPolicy Bypass -File install_windows.ps1
```

4. Follow the on-screen prompts
5. Wait for installation to complete

### Method 2: Batch Script Installation

**Advantages**: Works on older Windows versions, simpler syntax

**Steps**:

1. Open Command Prompt as Administrator
2. Navigate to the project directory
3. Run the installation script:

```cmd
install_windows.bat
```

4. Follow the prompts
5. Installation will complete automatically

### Method 3: Manual Installation

**Advantages**: Full control, can customize installation

**Steps**:

1. **Install Python**
   - Download Python 3.12+ from python.org
   - Run installer with "Add Python to PATH" checked
   - Verify installation:
   ```cmd
   python --version
   ```

2. **Clone Repository**
   ```cmd
   git clone https://github.com/yourusername/exo-windows.git
   cd exo-windows
   ```

3. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

4. **Install Dependencies**
   ```cmd
   pip install --upgrade pip setuptools wheel
   pip install -e .
   ```

5. **Verify Installation**
   ```cmd
   exo --help
   ```

## Post-Installation Configuration

### 1. Environment Setup

Create a `.env` file in the project root:

```env
# Model storage location
EXO_HOME=D:\models

# Network configuration
LISTEN_PORT=5678
BROADCAST_PORT=5678

# API configuration
CHATGPT_API_PORT=52415
CHATGPT_API_RESPONSE_TIMEOUT=900

# Inference configuration
INFERENCE_ENGINE=tinygrad
MAX_GENERATE_TOKENS=10000

# Logging
DEBUG=0
```

### 2. System Optimization

Run system optimization (requires admin):

```powershell
# Enable large pages
Enable-WindowsOptionalFeature -Online -FeatureName LargePages

# Optimize network settings
netsh int tcp set global autotuninglevel=normal
netsh int tcp set global chimney=disabled
```

### 3. Firewall Configuration

Allow the application through Windows Firewall:

```powershell
# Allow UDP discovery
New-NetFirewallRule -DisplayName "Exo UDP Discovery" `
    -Direction Inbound -Action Allow -Protocol UDP -LocalPort 5678

# Allow API endpoint
New-NetFirewallRule -DisplayName "Exo API" `
    -Direction Inbound -Action Allow -Protocol TCP -LocalPort 52415
```

## Network Setup

### Single Device Setup

```cmd
exo
```

Access the web interface at: `http://localhost:52415`

### Multi-Device Local Network Setup

**Device 1 (Primary)**:
```cmd
exo --node-id primary-device
```

**Device 2 (Secondary)**:
```cmd
exo --node-id secondary-device
```

Devices will auto-discover on the local network.

### Cross-Network Setup (Tailscale)

1. **Install Tailscale**
   - Download from https://tailscale.com
   - Sign in with your account

2. **Configure Exo**
   ```cmd
   exo --discovery-module tailscale `
       --tailscale-api-key YOUR_API_KEY `
       --tailnet-name your-tailnet
   ```

### Manual Network Configuration

For networks without auto-discovery:

```cmd
exo --discovery-module manual `
    --discovery-config-path config.json
```

**config.json**:
```json
{
  "peers": [
    {
      "host": "192.168.1.100",
      "port": 5678,
      "node_id": "device-1"
    },
    {
      "host": "192.168.1.101",
      "port": 5678,
      "node_id": "device-2"
    }
  ]
}
```

## Performance Tuning

### CPU Optimization

```cmd
REM Increase process priority
wmic process where name="python.exe" call setpriority 128

REM Set CPU affinity (use specific cores)
exo --cpu-affinity 0,1,2,3
```

### Memory Optimization

```cmd
REM Set virtual memory
wmic pagefileset where name="C: \\ " set InitialSize=16384,MaximumSize=32768
```

### GPU Optimization

**NVIDIA**:
```cmd
REM Set GPU to high performance
nvidia-smi -pm 1
nvidia-smi -pstate P0
```

**AMD**:
```cmd
REM Enable GPU performance mode
amd-smi power-profile set 0 3
```

### Network Optimization

```powershell
# Increase TCP window size
netsh int tcp set global autotuninglevel=normal

# Set TCP buffer sizes
netsh int tcp set global maxsynretrans=2
netsh int tcp set global tcpmaxdataretransmissions=3
```

## Monitoring and Maintenance

### Health Check

```powershell
# Check service status
$response = Invoke-WebRequest -Uri "http://localhost:52415/health" -Method Get
$response.Content | ConvertFrom-Json | Format-List
```

### Performance Monitoring

```powershell
# Monitor system resources
Get-Process python | Select-Object Name, CPU, Memory

# Monitor network connections
netstat -an | Select-String "52415"
```

### Log Management

```cmd
REM Enable detailed logging
set DEBUG=9
exo

REM Save logs to file
exo > logs\exo_%date:~-4,4%%date:~-10,2%%date:~-7,2%.log 2>&1
```

### Regular Maintenance

- **Weekly**: Check disk space, review logs
- **Monthly**: Update Python packages, clean cache
- **Quarterly**: Update GPU drivers, review performance

## Troubleshooting

### Installation Issues

**Problem**: "Python not found"
```cmd
REM Solution: Add Python to PATH
setx PATH "%PATH%;C:\Python312"
```

**Problem**: "Permission denied"
```cmd
REM Solution: Run as Administrator
```

**Problem**: "Virtual environment creation failed"
```cmd
REM Solution: Use alternative method
python -m venv --copies venv
```

### Runtime Issues

**Problem**: "Port already in use"
```cmd
REM Solution: Use different port
exo --chatgpt-api-port 52416
```

**Problem**: "Out of memory"
```cmd
REM Solution: Reduce model size or add devices
exo --run-model llama-3.2-3b
```

**Problem**: "GPU not detected"
```cmd
REM Solution: Check GPU drivers
nvidia-smi
amd-smi list
```

### Network Issues

**Problem**: "Device discovery timeout"
```cmd
REM Solution: Increase timeout
exo --discovery-timeout 60
```

**Problem**: "Connection refused"
```cmd
REM Solution: Check firewall
netsh advfirewall show allprofiles
```

**Problem**: "Slow inference"
```cmd
REM Solution: Check network bandwidth
netsh interface tcp show global
```

## Advanced Deployment

### Docker Deployment (Windows Containers)

```dockerfile
FROM python:3.12-windowsservercore

WORKDIR /app
COPY . .

RUN pip install -e .

EXPOSE 52415 5678

CMD ["exo"]
```

Build and run:
```powershell
docker build -t exo-windows .
docker run -p 52415:52415 -p 5678:5678 exo-windows
```

### Systemd Service (WSL2)

Create `/etc/systemd/system/exo.service`:

```ini
[Unit]
Description=Distributed Inference Framework
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/exo
ExecStart=/home/ubuntu/exo/venv/bin/python -m exo.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable exo
sudo systemctl start exo
```

### Scheduled Tasks (Windows Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup")
4. Set action: Start program
5. Program: `C:\path\to\venv\Scripts\python.exe`
6. Arguments: `-m exo.main`

## Backup and Recovery

### Backup Models

```powershell
# Backup model cache
Copy-Item -Path "$env:USERPROFILE\.cache\exo" -Destination "D:\backups\exo-models" -Recurse
```

### Restore Models

```powershell
# Restore from backup
Copy-Item -Path "D:\backups\exo-models" -Destination "$env:USERPROFILE\.cache\exo" -Recurse -Force
```

## Performance Benchmarking

```powershell
# Run benchmark
exo --benchmark --model llama-3.2-3b

# Save results
exo --benchmark --model llama-3.2-3b | Tee-Object -FilePath benchmark_results.txt
```

## Support and Resources

- **Documentation**: See docs/ folder
- **GitHub Issues**: Report bugs
- **Community**: Join Discord/Telegram for discussions
- **FAQ**: See FAQ.md for common questions

---

**Last Updated**: December 2025
**Version**: 1.0

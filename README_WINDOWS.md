# Distributed Inference Framework - Windows Edition

Run your own distributed inference cluster on Windows with everyday devices. This is a Windows-optimized fork of the exo framework with enhanced performance and native Windows support.

## Features

- **Native Windows Support**: Optimized for Windows 10/11 with native system integration
- **Multi-Device Clustering**: Connect multiple Windows, Mac, and Linux devices into a single inference cluster
- **Automatic Device Discovery**: Zero-configuration device discovery across your network
- **GPU Acceleration**: Support for NVIDIA, AMD, and Intel Arc GPUs
- **Distributed Model Inference**: Run large models across multiple devices
- **ChatGPT-Compatible API**: Drop-in replacement for OpenAI API
- **Web Interface**: Built-in web UI for easy interaction

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 or Windows 11
- **Python**: 3.12 or later
- **RAM**: 8GB minimum (16GB+ recommended)
- **Storage**: 50GB free space for models
- **Network**: Stable internet connection for model downloads

### Recommended Requirements
- **OS**: Windows 11 (latest version)
- **CPU**: Multi-core processor (8+ cores)
- **RAM**: 32GB or more
- **GPU**: NVIDIA RTX 3060 or better (optional but recommended)
- **Storage**: SSD with 100GB+ free space

### Supported GPUs
- **NVIDIA**: RTX 30/40 series and newer
- **AMD**: RDNA 2 and newer
- **Intel**: Arc A-series GPUs

## Installation

### Quick Start (Recommended)

#### Option 1: PowerShell Script (Easiest)

```powershell
powershell -ExecutionPolicy Bypass -File install_windows.ps1
```

#### Option 2: Batch Script

```cmd
install_windows.bat
```

#### Option 3: Manual Installation

1. **Install Python 3.12+**
   - Download from https://www.python.org
   - During installation, check "Add Python to PATH"

2. **Clone the Repository**
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

## Quick Start

### 1. Start the Framework

```cmd
exo
```

This will:
- Detect your system configuration
- Initialize the inference engine
- Start the web interface on `http://localhost:52415`
- Begin listening for peer devices

### 2. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:52415
```

### 3. Run Your First Inference

Using the web interface:
1. Select a model (e.g., "llama-3.2-3b")
2. Enter your prompt
3. Click "Generate"

Or using the API:

```powershell
$body = @{
    model = "llama-3.2-3b"
    messages = @(@{
        role = "user"
        content = "What is distributed inference?"
    })
    temperature = 0.7
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:52415/v1/chat/completions" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

## Configuration

### Environment Variables

```cmd
REM Set model storage location
set EXO_HOME=D:\models

REM Enable debug logging
set DEBUG=1

REM Set inference engine (mlx, tinygrad, dummy)
set INFERENCE_ENGINE=tinygrad

REM Set listening port
set LISTEN_PORT=5678
```

### Command Line Arguments

```cmd
exo --help
```

Common arguments:
- `--node-id <id>` - Set node identifier
- `--node-port <port>` - Set node listening port
- `--chatgpt-api-port <port>` - Set API port (default: 52415)
- `--discovery-module udp|tailscale|manual` - Discovery method
- `--inference-engine mlx|tinygrad|dummy` - Inference backend
- `--disable-tui` - Disable terminal UI

## Multi-Device Setup

### Connect Multiple Windows Devices

1. **Device 1 (Primary)**
   ```cmd
   exo
   ```

2. **Device 2 (Secondary)**
   ```cmd
   exo --node-id device-2
   ```

Devices will automatically discover each other on the local network.

### Connect Across Different Networks

Use Tailscale for secure cross-network connections:

```cmd
exo --discovery-module tailscale --tailscale-api-key <your-key>
```

## Model Management

### Available Models

- Llama 3.2 3B
- Llama 3.2 11B
- Llama 3.1 8B
- Llama 3.1 70B
- Llama 3.1 405B
- Mistral 7B
- Deepseek R1
- And more...

### Model Storage

Models are stored in:
```
%USERPROFILE%\.cache\exo\downloads
```

Or set custom location:
```cmd
set EXO_HOME=D:\my_models
```

### Download Models

Models are automatically downloaded on first use. To pre-download:

```cmd
exo --models-seed-dir D:\models
```

## Performance Optimization

### Windows-Specific Optimizations

The framework automatically applies:
- TCP window size optimization
- Process priority adjustment
- Memory management optimization
- GPU memory allocation tuning

### Manual Optimization

1. **Disable Unnecessary Services**
   - Close background applications
   - Disable Windows Update during inference

2. **Network Optimization**
   - Use wired Ethernet when possible
   - Disable WiFi power saving

3. **GPU Optimization**
   - Update GPU drivers
   - Set GPU to "High Performance" mode

4. **Memory Management**
   - Close other applications
   - Increase virtual memory if needed

## API Usage

### ChatGPT-Compatible Endpoint

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    model = "llama-3.2-3b"
    messages = @(
        @{
            role = "system"
            content = "You are a helpful assistant."
        },
        @{
            role = "user"
            content = "Explain quantum computing"
        }
    )
    temperature = 0.7
    max_tokens = 1000
} | ConvertTo-Json

$response = Invoke-WebRequest `
    -Uri "http://localhost:52415/v1/chat/completions" `
    -Method Post `
    -Headers $headers `
    -Body $body

$response.Content | ConvertFrom-Json | Format-List
```

### Python Example

```python
import requests

url = "http://localhost:52415/v1/chat/completions"
headers = {"Content-Type": "application/json"}

payload = {
    "model": "llama-3.2-3b",
    "messages": [
        {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7
}

response = requests.post(url, json=payload, headers=headers)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

## Troubleshooting

### Issue: "Python not found"
**Solution**: 
- Ensure Python 3.12+ is installed
- Add Python to PATH during installation
- Restart terminal after installation

### Issue: "Port already in use"
**Solution**:
```cmd
exo --chatgpt-api-port 52416
```

### Issue: "GPU not detected"
**Solution**:
- Update GPU drivers
- Check GPU is not in power-saving mode
- Verify CUDA/ROCm installation for NVIDIA/AMD

### Issue: "Low inference speed"
**Solution**:
- Check available system memory
- Close other applications
- Use wired network connection
- Enable GPU acceleration

### Issue: "Device discovery not working"
**Solution**:
- Ensure devices are on same network
- Check firewall settings
- Use `--discovery-module manual` with explicit IPs
- Try Tailscale for cross-network setup

## Advanced Configuration

### Custom Model Partitioning

```cmd
exo --partitioning-strategy ring-memory-weighted
```

### Enable Detailed Logging

```cmd
set DEBUG=9
exo
```

### Benchmark Performance

```cmd
exo --download-quick-check --max-parallel-downloads 16
```

## Security Considerations

- The API endpoint is local-only by default
- For remote access, use a reverse proxy (nginx, Caddy)
- Consider using Tailscale for secure cross-network access
- Keep Python and dependencies updated

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

GPL-3.0 License - See LICENSE file for details

## Support

- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share ideas
- **Documentation**: See docs/ folder for detailed guides

## Acknowledgments

This is a Windows-optimized fork of the exo framework by exo labs. Special thanks to the original authors and all contributors.

---

**Last Updated**: December 2025
**Framework Version**: 0.0.1-windows

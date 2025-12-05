# PowerShell installation script for Windows
# Run with: powershell -ExecutionPolicy Bypass -File install_windows.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Distributed Inference Framework Setup" -ForegroundColor Cyan
Write-Host "Windows Edition" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/6] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.12 or later from https://www.python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/6] Checking system requirements..." -ForegroundColor Cyan

# Get system info
$systemInfo = @{
    'OS' = [System.Environment]::OSVersion.VersionString
    'Architecture' = [System.Environment]::Is64BitOperatingSystem ? '64-bit' : '32-bit'
    'Processor' = (Get-WmiObject Win32_Processor).Name
    'RAM' = [math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
}

foreach ($key in $systemInfo.Keys) {
    Write-Host "  $key : $($systemInfo[$key])" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[3/6] Creating virtual environment..." -ForegroundColor Cyan

if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "  Virtual environment created successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "[4/6] Activating virtual environment..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "[5/6] Upgrading pip and setuptools..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Warning: Failed to upgrade pip" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[6/6] Installing framework dependencies..." -ForegroundColor Cyan
Write-Host "  This may take several minutes..." -ForegroundColor Gray

pip install -e . --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Activate the environment:"
Write-Host "     .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Start the framework:"
Write-Host "     exo" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. Open your browser to:"
Write-Host "     http://localhost:52415" -ForegroundColor Yellow
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"

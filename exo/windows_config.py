"""
Windows-specific configuration and utilities for distributed inference.
Handles Windows-specific system optimizations and device detection.
"""

import os
import sys
import platform
import subprocess
import psutil
from typing import Dict, List, Optional, Tuple

class WindowsSystemConfig:
    """Manages Windows system configuration for optimal performance."""
    
    def __init__(self):
        self.is_windows = sys.platform.startswith("win32")
        self.system_info = self._get_system_info()
        self.gpu_info = self._detect_gpus()
        
    def _get_system_info(self) -> Dict:
        """Get comprehensive Windows system information."""
        return {
            "os": platform.system(),
            "version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(logical=False),
            "cpu_count_logical": psutil.cpu_count(logical=True),
            "total_memory_gb": psutil.virtual_memory().total / (1024**3),
            "available_memory_gb": psutil.virtual_memory().available / (1024**3),
        }
    
    def _detect_gpus(self) -> List[Dict]:
        """Detect available GPUs on Windows system."""
        gpus = []
        
        # Check for NVIDIA GPUs
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(',')
                        gpus.append({
                            'type': 'NVIDIA',
                            'name': parts[0].strip(),
                            'memory_mb': int(parts[1].strip().split()[0]) if len(parts) > 1 else 0
                        })
        except Exception:
            pass
        
        # Check for AMD GPUs
        try:
            result = subprocess.run(
                ['amd-smi', 'list', '--csv'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                gpus.append({
                    'type': 'AMD',
                    'name': 'AMD GPU',
                    'memory_mb': 0
                })
        except Exception:
            pass
        
        # Check for Intel Arc GPUs
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-WmiObject Win32_VideoController | Select-Object Name'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'Arc' in result.stdout:
                gpus.append({
                    'type': 'Intel Arc',
                    'name': 'Intel Arc GPU',
                    'memory_mb': 0
                })
        except Exception:
            pass
        
        return gpus
    
    def optimize_network_settings(self):
        """Optimize Windows network settings for distributed inference."""
        if not self.is_windows:
            return
        
        try:
            # Increase TCP window size for better throughput
            subprocess.run([
                'netsh', 'int', 'tcp', 'set', 'global', 'autotuninglevel=normal'
            ], capture_output=True)
            
            # Disable TCP Chimney offload (can cause issues with GRPC)
            subprocess.run([
                'netsh', 'int', 'tcp', 'set', 'global', 'chimney=disabled'
            ], capture_output=True)
            
        except Exception:
            pass
    
    def get_available_memory(self) -> Tuple[int, int]:
        """Get available and total memory in bytes."""
        vm = psutil.virtual_memory()
        return vm.available, vm.total
    
    def get_cpu_info(self) -> Dict:
        """Get detailed CPU information."""
        return {
            'physical_cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'frequency_mhz': psutil.cpu_freq().current if psutil.cpu_freq() else 0,
            'usage_percent': psutil.cpu_percent(interval=1),
        }
    
    def print_system_info(self):
        """Print formatted system information."""
        print("\n" + "="*60)
        print("SYSTEM CONFIGURATION")
        print("="*60)
        
        for key, value in self.system_info.items():
            if isinstance(value, float):
                print(f"{key:.<30} {value:.2f}")
            else:
                print(f"{key:.<30} {value}")
        
        if self.gpu_info:
            print("\nDETECTED ACCELERATORS:")
            for gpu in self.gpu_info:
                print(f"  - {gpu['type']:.<20} {gpu['name']}")
        
        print("="*60 + "\n")


class WindowsProcessOptimization:
    """Optimize process-level settings for Windows."""
    
    @staticmethod
    def set_process_priority(priority: str = "high"):
        """Set process priority for better performance."""
        try:
            import psutil
            p = psutil.Process(os.getpid())
            
            priority_map = {
                'low': psutil.BELOW_NORMAL_PRIORITY_CLASS,
                'normal': psutil.NORMAL_PRIORITY_CLASS,
                'high': psutil.ABOVE_NORMAL_PRIORITY_CLASS,
                'realtime': psutil.REALTIME_PRIORITY_CLASS,
            }
            
            if priority in priority_map:
                p.nice(priority_map[priority])
        except Exception:
            pass
    
    @staticmethod
    def enable_large_pages():
        """Enable large page support on Windows for better performance."""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Enable-WindowsOptionalFeature -Online -FeatureName LargePages'
            ], capture_output=True, check=False)
        except Exception:
            pass


# Global configuration instance
_windows_config = None

def get_windows_config() -> WindowsSystemConfig:
    """Get or create global Windows configuration."""
    global _windows_config
    if _windows_config is None:
        _windows_config = WindowsSystemConfig()
    return _windows_config


def initialize_windows_environment():
    """Initialize Windows-specific environment settings."""
    if not sys.platform.startswith("win32"):
        return
    
    config = get_windows_config()
    config.optimize_network_settings()
    WindowsProcessOptimization.set_process_priority("high")
    config.print_system_info()

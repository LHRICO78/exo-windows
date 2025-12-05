# Changelog

All notable changes to the Exo Windows Fork project will be documented in this file.

## [0.0.1-windows] - 2025-12-05

### Added
- Native Windows 10/11 support with system optimization
- Windows system configuration module (`windows_config.py`)
  - Automatic GPU detection (NVIDIA, AMD, Intel Arc)
  - Network optimization for Windows
  - Process priority management
  - System information reporting
- Backend service layer (`backend_service.py`)
  - Unified inference request/response handling
  - Response caching mechanism
  - Batch processing support
  - Service lifecycle management
  - Performance monitoring
- Automated installation scripts
  - PowerShell installer with system checks
  - Batch script installer for compatibility
- Comprehensive Windows documentation
  - README_WINDOWS.md with quick start guide
  - DEPLOYMENT_GUIDE.md with detailed procedures
  - QUICK_START.md for 5-minute setup
- Windows-specific setup configuration (`setup_windows.py`)
- Project documentation
  - PROJECT_SUMMARY.md with architecture overview
  - WINDOWS_FORK_INDEX.md with complete file index
  - CONTRIBUTORS.md for contribution guidelines

### Improved
- Windows network performance optimization
  - TCP window size tuning
  - Chimney offload configuration
  - Buffer size optimization
- System resource management
  - Memory optimization
  - CPU affinity support
  - Virtual memory configuration
- Installation experience
  - Automated dependency resolution
  - System validation checks
  - User-friendly feedback and progress reporting

### Fixed
- Windows-specific compatibility issues
- Path handling for Windows systems
- GPU detection on Windows platforms

### Documentation
- Complete Windows installation guide
- Deployment procedures for single and multi-device setups
- Performance tuning guide
- Troubleshooting section with common issues
- API usage examples in multiple languages

## [0.0.1] - Original Exo Project

Based on the original exo-explore/exo framework with the following features:
- Distributed model inference across devices
- Support for multiple models (Llama, Mistral, Deepseek, etc.)
- Dynamic model partitioning
- Automatic device discovery
- ChatGPT-compatible API
- P2P networking architecture
- Multiple inference engines (MLX, tinygrad)

## Future Roadmap

### Planned Features
- [ ] Docker support for Windows containers
- [ ] Windows Service integration for auto-start
- [ ] GUI application wrapper
- [ ] Advanced performance dashboard
- [ ] Automatic update mechanism
- [ ] Enhanced monitoring tools
- [ ] Multi-language support in UI

### Under Investigation
- [ ] WASM support for browser-based inference
- [ ] Mobile device integration
- [ ] Cloud deployment templates
- [ ] Advanced security features

## Version History

| Version | Release Date | Status |
|---------|-------------|--------|
| 0.0.1-windows | 2025-12-05 | Current |
| 0.0.1 | Original | Based on |

## Breaking Changes

None in this release. Full backward compatibility with original exo framework maintained.

## Migration Guide

### From Original Exo to Windows Fork

1. **Installation**: Use `install_windows.ps1` instead of `install.sh`
2. **Configuration**: Windows-specific environment variables available
3. **API**: No changes - fully compatible
4. **Models**: No changes - same model support

### From Windows Fork to Original Exo

Simply use the original installation method. All code is compatible.

## Known Issues

### Current Release
- None reported

### Resolved
- Windows path handling (Fixed in 0.0.1-windows)
- GPU detection on Windows (Fixed in 0.0.1-windows)

## Support

For issues, questions, or feature requests:
1. Check existing GitHub issues
2. Review troubleshooting section in documentation
3. Create a new issue with detailed information

## Contributing

See CONTRIBUTORS.md for guidelines on how to contribute to this project.

## License

This project is licensed under the GPL-3.0 License. See LICENSE file for details.

## Acknowledgments

- Original exo framework by exo-explore/exo team
- Windows optimization and service layer additions
- Community feedback and contributions

---

**Last Updated**: December 5, 2025
**Maintainer**: Exo Windows Team

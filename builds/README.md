# Enigma Build System

This document describes the build system for the Enigma CLI application using Nuitka.

## Overview

Enigma uses **Nuitka** to compile Python code into standalone executables. This provides:
- **Performance improvement** over interpreted Python
- **Standalone binaries** that don't require Python installation
- **Cross-platform compilation** support via GitHub Actions
- **Onefile mode** - single portable executable

## Directory Structure

```
enigma/
├── builds/                    # Build output directory
│   ├── .gitkeep             # Preserves directory in git
│   ├── latest/              # Symlink to most recent build
│   └── YYYYMMDD_HHMMSS/    # Timestamped builds
├── .github/
│   └── workflows/
│       └── build.yml        # CI/CD pipeline for cross-platform builds
├── scripts/
│   └── build.py             # Build automation script
├── pyproject.toml           # Project configuration (updated)
├── requirements.txt         # Runtime dependencies
└── main.py                  # Application entry point
```

## Quick Start

### Local Build

1. Install Nuitka:
   ```bash
   pip install nuitka
   ```

2. Run the build script:
   ```bash
   python scripts/build.py
   ```

3. Find your executable at:
   ```
   builds/latest/enigma.<ext>  # .exe on Windows, .bin on Linux/macOS
   ```

### Build Options

| Command | Description |
|---------|-------------|
| `python scripts/build.py` | Build for current platform |
| `python scripts/build.py --clean` | Clean all builds |
| `python scripts/build.py --all` | Build for all platforms |
| `python scripts/build.py --target win` | Cross-compile for Windows |
| `python scripts/build.py --target linux` | Cross-compile for Linux |
| `python scripts/build.py --target macos` | Cross-compile for macOS |
| `python scripts/build.py -o ./mybuild` | Custom output directory |

## GitHub Actions CI/CD

The build pipeline automatically:

1. **Triggers on:**
   - Every push to `main` branch
   - Every pull request to `main`
   - Version tags (`v*`)
   - Manual workflow dispatch

2. **Builds for:**
   - Ubuntu Linux (x86_64)
   - macOS (universal)
   - Windows (x86_64)

3. **Release automation:**
   - When a version tag is pushed, creates a GitHub Release
   - Attaches all platform binaries to the release

### Usage with GitHub Actions

1. Push a version tag:
   ```bash
   git tag v1.2.0
   git push origin v1.2.0
   ```

2. The workflow will:
   - Build for all platforms
   - Create a draft release
   - Upload all executables

3. Review and publish the release on GitHub

## Nuitka Configuration

### Key Options Used

| Option | Description |
|--------|-------------|
| `--onefile` | Creates a single portable executable |
| `--follow-imports` | Automatically includes all imports |
| `--lto=yes` | Enables link-time optimization |
| `--python-flag=no_site` | Excludes site-packages for smaller size |
| `--include-data-dir` | Bundles assets directory |
| `--include-package-data` | Includes package data files |

### Asset Handling

The `assets/` directory is bundled into the executable:
- `assets/art/` - ASCII art files
- `assets/data/` - Configuration and database

These are extracted to a temporary directory at runtime and accessed via `__file__` path resolution.

## Requirements

### Runtime Dependencies
```
requests>=2.32,<3
PyYAML>=6,<7
Pillow>=10,<11
cryptography>=45.0,<46
pycryptodome>=3.20,<4
```

### Build Dependencies
```
nuitka>=2.0
```

### Platform-Specific

**Linux/macOS:**
- Standard GCC/Clang compiler (usually pre-installed)

**Windows:**
- Visual Studio 2022 or MinGW64

**Cross-compilation (Linux to Windows):**
- `mingw64` package

## Troubleshooting

### Common Issues

1. **Missing DLLs on Windows**
   - Ensure Visual Studio 2022 is installed
   - Or install MinGW64

2. **Large executable size**
   - Use `--onefile` mode (default)
   - Consider `--python-flag=no_site`

3. **Assets not found**
   - Verify `--include-data-dir` paths
   - Check `builds/latest/assets/` exists

4. **Import errors**
   - Use `--follow-imports` to catch all imports
   - Add explicit `--include-module` for dynamic imports

### Debug Builds

```bash
# Verbose output
python -m nuitka --verbose main.py

# Report generation
python -m nuitka --report=build_report.xml main.py
```

## File Locations at Runtime

The compiled application uses special paths:

```python
# For data files bundled with the executable:
try:
    from __compiled__ import containing_dir
except ImportError:
    containing_dir = os.path.dirname(sys.argv[0])
```

This ensures files are found whether:
- Running from source (`python main.py`)
- Running from standalone executable
- Running from onefile binary

## Notes

- **No console window on Windows GUI apps**: Use `--windows-console-mode=disable`
- **Console apps on Windows**: Use `--windows-console-mode=attach` (default)
- **macOS app bundle**: Consider `--macos-create-app-bundle` for GUI apps

# Enigma - Passwords and Credentials Manager Application

### Version: 1.1.1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)

> A reliable Credentials Manager CLI Application targeting CLI environments via a beautiful TUI interface and respectable encryption practices.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Building from Source](#building-from-source)
- [Project Structure](#project-structure)
- [Security](#security)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## About

Enigma is a lightweight, offline-first credentials manager designed for CLI environments. Built entirely in Python, it combines military-grade cryptography with portability, making it ideal for securing sensitive data across different machines and environments.

### Key Characteristics

- **Offline-first**: All data stored locally in SQLite database
- **Multi-user support**: Isolated credentials per user with independent encryption keys
- **Cross-platform**: Works on Linux, macOS, and Windows terminals
- **Portable**: Can run from USB flash drives without installation
- **Lightweight**: Minimal dependencies, fast startup

#### Author: Túlio Horta

---

## Features

- **Secure TUI Interface**: Interactive terminal-based user interface using `curses`
- **AES-256 Encryption**: Military-grade symmetric encryption for credential storage
- **PBKDF2 Key Derivation**: Secure password-based key derivation with configurable iterations
- **Fernet Multi-Key Encryption**: Additional layer of protection using multi-key Fernet
- **Multi-User Architecture**: Each user has isolated credentials with independent encryption
- **SQLite Storage**: Lightweight, zero-configuration database
- **ASCII Art UI**: Beautiful terminal visuals

---

## Installation

### Option 1: Pre-built Executable (Recommended)

Download the latest release for your platform from the [GitHub Releases](https://github.com/tuliofh01/enigma/releases) page.

| Platform | File | Notes |
|----------|------|-------|
| Linux | `enigma.bin` | Make executable: `chmod +x enigma.bin` |
| macOS | `enigma.bin` | Allow execution in System Preferences if blocked |
| Windows | `enigma.exe` | Run from Command Prompt or PowerShell |

### Option 2: Python Installation

```bash
# Clone the repository
git clone https://github.com/tuliofh01/enigma.git
cd enigma

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run directly
python main.py
```

### Option 3: Install as Package

```bash
# Install in development mode
pip install -e .

# Run via command
enigma
```

---

## Usage

### First Run

1. Launch the application:
   ```bash
   ./enigma.bin  # Linux/macOS
   enigma.exe    # Windows
   ```

2. The application will display the greetings screen

3. To create your first user, run the initialization script:
   ```bash
   python src/scripts/init_user.py
   ```

### Main Interface

The TUI provides the following states:

| State | Description |
|-------|-------------|
| `greetings` | Welcome screen with ASCII art |
| `login` | User authentication |
| `error` | Error display and handling |
| `main` | Main application interface (future) |

### User Authentication

On first use, the initialization script creates a new user entry with:
- Username (ASCII only)
- Password (combined with salt + pepper)
- Auto-generated encryption salt

### Managing Credentials

The `DatabaseCtrl` class provides:

| Method | Description |
|--------|-------------|
| `authenticate(username, password)` | Verify user credentials |
| `get_all_records()` | Retrieve all credential records |
| `get_decrypted_target_record(id)` | Decrypt and retrieve specific record |
| `encrypt_and_insert_record(desc, user, pwd)` | Add new credential |
| `delete_target_record(id)` | Remove credential |

---

## Building from Source

For instructions on compiling Enigma into standalone executables, see the [Build System Documentation](builds/README.md).

### Quick Build

```bash
# Install Nuitka
pip install nuitka

# Build for current platform
python scripts/build.py

# Build output location
ls builds/latest/
```

### Build Options

```bash
# Build for specific platform
python scripts/build.py --target win    # Windows
python scripts/build.py --target linux  # Linux
python scripts/build.py --target macos  # macOS

# Build for all platforms (requires cross-compilers)
python scripts/build.py --all

# Clean previous builds
python scripts/build.py --clean
```

### Cross-Platform CI/CD

The project includes GitHub Actions workflows for automated builds:

| Trigger | Action |
|---------|--------|
| Push to `main` | Dev builds for all platforms |
| Pull Request | Dev builds |
| Version tag (`v*`) | Release builds + GitHub Release |

---

## Project Structure

```
enigma/
├── main.py                      # Application entry point
├── main.spec                    # PyInstaller spec (legacy)
├── requirements.txt             # Runtime dependencies
├── pyproject.toml               # Package configuration
│
├── src/                         # Source code
│   ├── controllers/
│   │   └── database_controller.py  # Database & encryption logic
│   ├── misc/
│   │   ├── config.py               # Global configuration
│   │   └── resize_window.py        # Terminal resize handling
│   ├── scripts/
│   │   └── init_user.py           # User initialization utility
│   └── tui/
│       ├── windows/
│       │   ├── empty_window.py        # Base window
│       │   └── stateful_window.py     # State machine window
│       └── window_transformations/
│           ├── greetings_state.py
│           ├── login_state.py
│           ├── main_state.py
│           ├── error_state.py
│           └── old/                  # Deprecated screens
│
├── assets/                      # Application assets
│   ├── art/                    # ASCII art files
│   │   ├── title_art.txt
│   │   ├── loading_art.txt
│   │   └── error_art.txt
│   └── data/
│       ├── env_variables.json  # Configuration
│       └── sqlite3_data_file.db # Encrypted credentials
│
├── builds/                     # Build output (gitignored)
│   ├── README.md              # Build system documentation
│   └── YYYYMMDD_HHMMSS/      # Timestamped builds
│
└── .github/
    └── workflows/
        └── build.yml          # CI/CD pipeline
```

---

## Security

### Encryption Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    ENCRYPTION LAYERS                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: PBKDF2 (Password-Based Key Derivation)           │
│  ├── Algorithm: SHA-256                                     │
│  ├── Iterations: Configurable (default: 100,000)          │
│  └── Output: 256-bit key                                   │
│                                                             │
│  Layer 2: AES-256-ECB (Credential Encryption)              │
│  ├── Block cipher with PKCS7 padding                       │
│  └── Encrypts: Password + Pepper                            │
│                                                             │
│  Layer 3: Fernet Multi-Key (Record Encryption)             │
│  ├── AES-128-CBC with PKCS7 padding                        │
│  ├── HMAC using SHA-256 for authentication                 │
│  └── Encrypts: Username, Password, Description             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Security Best Practices

- **Salt**: Unique 16-byte random salt per user (generated via `os.urandom`)
- **Pepper**: Random character appended before hashing
- **Key Derivation**: PBKDF2-HMAC-SHA256 with high iteration count
- **Database**: SQLite with encrypted credential fields
- **Offline**: No network transmission of credentials

### Known Limitations

- ECB mode for primary encryption (consider upgrading to CBC/GCM in future)
- No master password recovery mechanism
- Database file should be protected at filesystem level

---

## Documentation

| Document | Description |
|----------|-------------|
| [Build System](builds/README.md) | Detailed build process, CI/CD, troubleshooting |
| [Security Model](#security) | Encryption layers and practices |
| [API Reference](#) | Database controller methods (TBD) |

### Related Documentation

- [Nuitka User Manual](https://nuitka.net/user-documentation/user-manual.html)
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/)
- [curses module (Python)](https://docs.python.org/3/howto/curses.html)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Clone and setup
git clone https://github.com/tuliofh01/enigma.git
cd enigma
python -m venv .venv
source .venv/bin/activate

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/
```

---

## License

This project is licensed under the MIT License.

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## Acknowledgments

- **Cryptography**: [`cryptography`](https://cryptography.io/) - Modern crypto primitives
- **Crypto Operations**: [`pycryptodome`](https://pycryptodome.readthedocs.io/) - AES implementation
- **TUI Framework**: Python's built-in `curses` module
- **Build System**: [`Nuitka`](https://nuitka.net/) - Python compiler

---

*Thank you for using Enigma! Please remember to credit the author when using, modifying, or distributing this software.*

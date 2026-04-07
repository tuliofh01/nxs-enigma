#!/usr/bin/env python3
"""
Enigma Build Script using Nuitka
Compiles the Enigma CLI application to standalone executables for multiple platforms.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
BUILDS_DIR = PROJECT_ROOT / "builds"
SRC_DIR = PROJECT_ROOT / "src"
ASSETS_DIR = PROJECT_ROOT / "assets"


def check_nuitka():
    """Check if Nuitka is installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nuitka", "--version"],
            capture_output=True,
            text=True,
        )
        print(f"Nuitka version: {result.stdout.strip()}")
        return True
    except ImportError:
        print("Nuitka is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "nuitka"], check=True)
        return True


def get_platform_config():
    """Get platform-specific configuration."""
    if sys.platform == "win32":
        return {
            "name": "Windows",
            "extension": ".exe",
            "console_mode": "--windows-console-mode=attach",
            "icon_option": "--windows-icon-from-ico=assets/icon.ico" if (ASSETS_DIR / "icon.ico").exists() else "",
            "requires_cross": False,
        }
    elif sys.platform == "darwin":
        return {
            "name": "macOS",
            "extension": ".bin",
            "console_mode": "",
            "icon_option": "--macos-app-icon=assets/icon.png" if (ASSETS_DIR / "icon.png").exists() else "",
            "requires_cross": False,
        }
    else:
        return {
            "name": "Linux",
            "extension": ".bin",
            "console_mode": "",
            "icon_option": "",
            "requires_cross": False,
        }


def ensure_assets():
    """Ensure assets directory exists and has required files."""
    if not ASSETS_DIR.exists():
        print(f"Warning: Assets directory not found at {ASSETS_DIR}")
        return False
    
    required_dirs = ["art", "data"]
    for dir_name in required_dirs:
        dir_path = ASSETS_DIR / dir_name
        if not dir_path.exists():
            print(f"Warning: Required directory '{dir_name}' not found in assets")
    
    return True


def build_onefile(target_platform=None, output_dir=None, python_version=None):
    """
    Build the application as a onefile executable.
    
    Args:
        target_platform: Target platform for cross-compilation (win, macos, linux)
        output_dir: Output directory for the build
        python_version: Python version to use for cross-compilation
    """
    print(f"\n{'='*60}")
    print(f"Building Enigma CLI - Onefile Mode")
    print(f"{'='*60}")
    
    check_nuitka()
    ensure_assets()
    
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = BUILDS_DIR / timestamp
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    platform_config = get_platform_config()
    target_name = f"enigma{platform_config['extension']}"
    
    base_cmd = [
        sys.executable, "-m", "nuitka",
        "--onefile",
        "--company-name=Enigma",
        "--product-name=Enigma",
        f"--file-version=1.1.1",
        f"--copyright=Túlio Horta",
        f"--output-dir={output_dir}",
        f"--output-filename={target_name}",
        "--enable-plugin=numpy",  # Include numpy support if needed
        "--include-package-data=src",
        f"--include-data-dir={ASSETS_DIR}=assets",
        "--follow-imports",
        "--lto=yes",
        "--python-flag=no_site",
    ]
    
    # Platform-specific options
    if platform_config["console_mode"]:
        base_cmd.append(platform_config["console_mode"])
    
    if platform_config["icon_option"]:
        base_cmd.append(platform_config["icon_option"])
    
    # Cross-compilation options
    if target_platform:
        if target_platform == "win":
            base_cmd.extend(["--target-os=Windows", "--target-arch=x86_64"])
            # Override output name for Windows
            base_cmd[base_cmd.index("--output-filename=enigma.bin")] = "--output-filename=enigma.exe"
        elif target_platform == "macos":
            base_cmd.extend(["--target-os=macOS"])
            if python_version:
                base_cmd.append(f"--python-version={python_version}")
        elif target_platform == "linux":
            base_cmd.extend(["--target-os=Linux"])
            if python_version:
                base_cmd.append(f"--python-version={python_version}")
    
    # Main entry point
    base_cmd.append("main.py")
    
    print(f"\nBuild configuration:")
    print(f"  Entry point: main.py")
    print(f"  Output directory: {output_dir}")
    print(f"  Target: {target_name}")
    print(f"  Assets included from: {ASSETS_DIR}")
    
    print(f"\nRunning: {' '.join(base_cmd)}\n")
    
    result = subprocess.run(base_cmd)
    
    if result.returncode == 0:
        print(f"\nBuild successful!")
        print(f"Output: {output_dir / target_name}")
        
        # Create a latest symlink
        latest_link = BUILDS_DIR / "latest"
        if latest_link.is_symlink() or latest_link.exists():
            shutil.rmtree(latest_link)
        shutil.copytree(output_dir, latest_link)
        print(f"Latest build available at: {latest_link}")
        
        return True
    else:
        print(f"\nBuild failed with return code: {result.returncode}")
        return False


def build_all_platforms():
    """Build for all supported platforms (requires appropriate compilers)."""
    print("\n" + "="*60)
    print("Cross-Platform Build")
    print("="*60)
    
    platforms = []
    
    if sys.platform == "linux":
        platforms = ["linux", "win"]  # Can cross-compile for Windows from Linux
    elif sys.platform == "darwin":
        platforms = ["macos", "linux"]
    elif sys.platform == "win32":
        platforms = ["win"]
    
    results = {}
    for platform in platforms:
        print(f"\nBuilding for {platform}...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = BUILDS_DIR / f"{platform}_{timestamp}"
        results[platform] = build_onefile(target_platform=platform, output_dir=output_dir)
    
    print("\n" + "="*60)
    print("Build Summary")
    print("="*60)
    for platform, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"  {platform}: {status}")


def clean_builds():
    """Clean all builds directory."""
    if BUILDS_DIR.exists():
        shutil.rmtree(BUILDS_DIR)
        print(f"Cleaned builds directory: {BUILDS_DIR}")
    else:
        print("Builds directory does not exist")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Build Enigma CLI with Nuitka",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/build.py              # Build for current platform
  python scripts/build.py --clean       # Clean all builds
  python scripts/build.py --all         # Build for all platforms
  python scripts/build.py --target win  # Cross-compile for Windows
        """
    )
    
    parser.add_argument(
        "--clean", "-c",
        action="store_true",
        help="Clean all builds before building"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Build for all supported platforms"
    )
    
    parser.add_argument(
        "--target", "-t",
        choices=["win", "macos", "linux"],
        help="Target platform for cross-compilation"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output directory for the build"
    )
    
    parser.add_argument(
        "--python-version", "-p",
        help="Python version for cross-compilation (e.g., 3.11)"
    )
    
    args = parser.parse_args()
    
    if args.clean:
        clean_builds()
    
    if args.all:
        build_all_platforms()
    elif args.target:
        build_onefile(
            target_platform=args.target,
            output_dir=args.output,
            python_version=args.python_version
        )
    else:
        build_onefile(output_dir=args.output)

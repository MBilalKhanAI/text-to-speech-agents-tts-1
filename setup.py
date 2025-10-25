#!/usr/bin/env python3
"""
Setup script for TTS Agents.

This script provides a simple way to install and configure the TTS Agents library
for development and production use.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install project dependencies."""
    print("📦 Installing dependencies...")
    
    # Install core dependencies
    if not run_command("pip install -e .", "Installing TTS Agents"):
        return False
    
    # Install development dependencies
    if not run_command("pip install -e .[dev]", "Installing development dependencies"):
        return False
    
    return True


def setup_pre_commit():
    """Set up pre-commit hooks."""
    print("🔧 Setting up pre-commit hooks...")
    return run_command("pre-commit install", "Installing pre-commit hooks")


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    return run_command("pytest tests/ -v", "Running test suite")


def check_code_quality():
    """Check code quality."""
    print("🔍 Checking code quality...")
    
    commands = [
        ("black --check src/ tests/", "Checking code formatting"),
        ("ruff check src/ tests/", "Running linting"),
        ("mypy src/", "Running type checking"),
    ]
    
    all_passed = True
    for command, description in commands:
        if not run_command(command, description):
            all_passed = False
    
    return all_passed


def create_env_file():
    """Create .env.example file if it doesn't exist."""
    env_example = Path(".env.example")
    if not env_example.exists():
        print("📝 Creating .env.example file...")
        env_content = """# TTS Agents Environment Configuration
# Copy this file to .env and fill in your values

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# TTS Agent Configuration
TTS_TIMEOUT=30
TTS_MAX_RETRIES=3
TTS_RATE_LIMIT_DELAY=1.0

# Default TTS Settings
TTS_DEFAULT_VOICE=alloy
TTS_DEFAULT_MODEL=tts-1
TTS_DEFAULT_FORMAT=mp3
TTS_DEFAULT_SPEED=1.0

# Logging Configuration
TTS_LOG_LEVEL=INFO
TTS_LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Output Configuration
TTS_OUTPUT_DIR=./output
TTS_TEMP_DIR=./temp
"""
        env_example.write_text(env_content)
        print("✅ .env.example file created")
    else:
        print("✅ .env.example file already exists")


def main():
    """Main setup function."""
    print("🎤 TTS Agents - Professional Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Set up pre-commit hooks
    if not setup_pre_commit():
        print("⚠️  Pre-commit setup failed, continuing...")
    
    # Create .env.example file
    create_env_file()
    
    # Run tests
    if not run_tests():
        print("⚠️  Some tests failed, but setup continues...")
    
    # Check code quality
    if not check_code_quality():
        print("⚠️  Code quality checks failed, but setup continues...")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and add your OpenAI API key")
    print("2. Run 'make test' to verify everything works")
    print("3. Run 'make examples' to see the library in action")
    print("4. Check the documentation in docs/")
    print("\n🚀 Your TTS Agents library is ready to use!")


if __name__ == "__main__":
    main()

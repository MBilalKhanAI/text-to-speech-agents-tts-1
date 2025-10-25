#!/bin/bash
# TTS Agents - Professional Setup Script
# This script sets up the TTS Agents project for development and production

set -e  # Exit on any error

echo "🎤 TTS Agents - Professional Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is not installed. Please install Python 3.9 or higher."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    else
        print_error "pip3 is not installed. Please install pip."
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    # Upgrade pip
    python3 -m pip install --upgrade pip
    
    # Install the package in development mode
    pip3 install -e .
    
    # Install development dependencies
    pip3 install -e ".[dev]"
    
    print_success "Dependencies installed successfully"
}

# Set up pre-commit hooks
setup_pre_commit() {
    print_status "Setting up pre-commit hooks..."
    if command -v pre-commit &> /dev/null; then
        pre-commit install
        print_success "Pre-commit hooks installed"
    else
        print_warning "Pre-commit not found, skipping hook installation"
    fi
}

# Create .env.example if it doesn't exist
create_env_example() {
    print_status "Creating .env.example file..."
    if [ ! -f ".env.example" ]; then
        cat > .env.example << EOF
# TTS Agents Environment Configuration
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
EOF
        print_success ".env.example file created"
    else
        print_success ".env.example file already exists"
    fi
}

# Run tests
run_tests() {
    print_status "Running tests..."
    if python3 -m pytest tests/ -v; then
        print_success "All tests passed"
    else
        print_warning "Some tests failed, but setup continues..."
    fi
}

# Check code quality
check_code_quality() {
    print_status "Checking code quality..."
    
    # Check formatting
    if python3 -m black --check src/ tests/; then
        print_success "Code formatting is correct"
    else
        print_warning "Code formatting issues found"
    fi
    
    # Check linting
    if python3 -m ruff check src/ tests/; then
        print_success "Linting passed"
    else
        print_warning "Linting issues found"
    fi
    
    # Check type hints
    if python3 -m mypy src/; then
        print_success "Type checking passed"
    else
        print_warning "Type checking issues found"
    fi
}

# Main setup function
main() {
    echo "Starting TTS Agents setup..."
    echo ""
    
    # Check prerequisites
    check_python
    check_pip
    
    # Install dependencies
    install_dependencies
    
    # Set up pre-commit hooks
    setup_pre_commit
    
    # Create .env.example file
    create_env_example
    
    # Run tests
    run_tests
    
    # Check code quality
    check_code_quality
    
    echo ""
    print_success "Setup completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Copy .env.example to .env and add your OpenAI API key"
    echo "2. Run 'make test' to verify everything works"
    echo "3. Run 'make examples' to see the library in action"
    echo "4. Check the documentation in docs/"
    echo ""
    echo "🚀 Your TTS Agents library is ready to use!"
}

# Run main function
main "$@"

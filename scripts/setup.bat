@echo off
REM TTS Agents - Professional Setup Script for Windows
REM This script sets up the TTS Agents project for development and production

echo 🎤 TTS Agents - Professional Setup
echo ==================================

REM Check if Python is installed
echo 🔄 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)
echo ✅ Python found

REM Check if pip is installed
echo 🔄 Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)
echo ✅ pip found

REM Install dependencies
echo 🔄 Installing dependencies...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)

pip install -e .
if %errorlevel% neq 0 (
    echo ❌ Failed to install TTS Agents
    pause
    exit /b 1
)

pip install -e ".[dev]"
if %errorlevel% neq 0 (
    echo ❌ Failed to install development dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

REM Set up pre-commit hooks
echo 🔄 Setting up pre-commit hooks...
pre-commit install >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Pre-commit not found, skipping hook installation
) else (
    echo ✅ Pre-commit hooks installed
)

REM Create .env.example if it doesn't exist
echo 🔄 Creating .env.example file...
if not exist ".env.example" (
    (
        echo # TTS Agents Environment Configuration
        echo # Copy this file to .env and fill in your values
        echo.
        echo # OpenAI API Configuration
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo OPENAI_BASE_URL=https://api.openai.com/v1
        echo.
        echo # TTS Agent Configuration
        echo TTS_TIMEOUT=30
        echo TTS_MAX_RETRIES=3
        echo TTS_RATE_LIMIT_DELAY=1.0
        echo.
        echo # Default TTS Settings
        echo TTS_DEFAULT_VOICE=alloy
        echo TTS_DEFAULT_MODEL=tts-1
        echo TTS_DEFAULT_FORMAT=mp3
        echo TTS_DEFAULT_SPEED=1.0
        echo.
        echo # Logging Configuration
        echo TTS_LOG_LEVEL=INFO
        echo TTS_LOG_FORMAT=%%(asctime)s - %%(name)s - %%(levelname)s - %%(message)s
        echo.
        echo # Output Configuration
        echo TTS_OUTPUT_DIR=./output
        echo TTS_TEMP_DIR=./temp
    ) > .env.example
    echo ✅ .env.example file created
) else (
    echo ✅ .env.example file already exists
)

REM Run tests
echo 🔄 Running tests...
python -m pytest tests/ -v
if %errorlevel% neq 0 (
    echo ⚠️  Some tests failed, but setup continues...
) else (
    echo ✅ All tests passed
)

REM Check code quality
echo 🔄 Checking code quality...
python -m black --check src/ tests/
if %errorlevel% neq 0 (
    echo ⚠️  Code formatting issues found
) else (
    echo ✅ Code formatting is correct
)

python -m ruff check src/ tests/
if %errorlevel% neq 0 (
    echo ⚠️  Linting issues found
) else (
    echo ✅ Linting passed
)

python -m mypy src/
if %errorlevel% neq 0 (
    echo ⚠️  Type checking issues found
) else (
    echo ✅ Type checking passed
)

echo.
echo ✅ Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Copy .env.example to .env and add your OpenAI API key
echo 2. Run 'make test' to verify everything works
echo 3. Run 'make examples' to see the library in action
echo 4. Check the documentation in docs/
echo.
echo 🚀 Your TTS Agents library is ready to use!
echo.
pause

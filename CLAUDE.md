# WhisperScript

A voice-controlled automation tool for macOS that listens to spoken instructions, processes them with an LLM, and executes them via AppleScript.

## Overview

WhisperScript allows you to speak natural language commands that get converted to executable AppleScript. For example:
- "Send an email to nano, and say we are meeting at 5 pm, do you want to go?" → Creates AppleScript to open Gmail and compose the email
- "Open calculator and compute 25 times 30" → Opens Calculator app and performs the calculation
- "Create a reminder for tomorrow at 2 PM to call the dentist" → Creates a reminder in the Reminders app

## Architecture

The project uses a hybrid Swift/Python architecture:

1. **Swift App**: Native macOS app with speech recognition using Speech framework
2. **Python Processing**: Pex executable that processes speech text and generates AppleScript using Claude API
3. **Integration**: Swift app calls Python script via stdin/stdout

### Components

- **Swift App**: Audio capture, speech recognition, and menu bar interface (menu bar UI needs work)
- **Python Pex**: Self-contained executable for LLM processing and AppleScript generation
- **Environment Config**: Uses `ANTHROPIC_API_KEY` environment variable

## Technology Stack

- **Python 3.9+**: LLM processing and AppleScript generation
- **Swift**: Native macOS app with speech recognition
- **Pex**: Self-contained Python executable packaging
- **uv**: Python package and project manager
- **Speech Framework**: macOS native speech recognition
- **Anthropic Claude API**: LLM for natural language to AppleScript conversion
- **Ruff**: Code formatter and linter
- **MyPy**: Static type checking

## Development Setup

### Prerequisites
- macOS 12+ (required for Speech framework and AppleScript execution)
- Python 3.9 or higher
- Swift 5.9+
- uv package manager

### Installation

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync --extra dev

# Build the complete app bundle
uv run python build_backend.py
```

### Code Quality

```bash
# Format code
uv run ruff format

# Lint code  
uv run ruff check

# Type check
uv run mypy src/
```

### Running the Application

```bash
# Set API key environment variable
export ANTHROPIC_API_KEY="your-api-key-here"

# Test with a recording file
./dist/WhisperScript.app/Contents/MacOS/WhisperScript tests/data/test01.m4a

# Run as menu bar app (menu bar UI needs work)
open dist/WhisperScript.app
```

## Configuration

The application uses environment variables for configuration:

```bash
# Required: Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Required Permissions

The application requires the following macOS permissions:
- **Microphone Access**: For audio capture
- **Accessibility**: For AppleScript execution
- **Automation**: For controlling other applications

## Project Structure

```
whisperscript/
├── src/
│   ├── swift/                          # Swift macOS app
│   │   ├── Package.swift
│   │   └── Sources/
│   │       └── WhisperScript/          # Unified app target
│   │           ├── main.swift          # Menu bar app entry point
│   │           └── AudioRecognitionService.swift  # Speech recognition
│   └── whisperscript/                  # Python package
│       ├── __init__.py
│       └── main.py                     # LLM processing (reads from stdin)
├── tests/
│   ├── data/                           # Test audio files
│   │   ├── test01.m4a
│   │   └── test02.m4a
│   └── test_audio_capture.py
├── build_backend.py                    # App bundle build script
├── Info.plist                         # macOS app metadata
├── pyproject.toml                      # Python project config
├── README.md
└── CLAUDE.md
```

## Commands to Remember

- `uv sync --extra dev`: Install all dependencies including Pex
- `uv run python build_backend.py`: Build complete app bundle
- `uv run ruff format && uv run ruff check`: Format and lint Python code
- `uv run mypy src/`: Type check the Python codebase
- `cd src/swift && swift build`: Build Swift app standalone
- `export ANTHROPIC_API_KEY="your-key" && ./dist/WhisperScript.app/Contents/MacOS/WhisperScript tests/data/test01.m4a`: Test with audio file
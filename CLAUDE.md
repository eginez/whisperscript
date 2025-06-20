# WhisperScript

A voice-controlled automation tool for macOS that listens to spoken instructions, processes them with an LLM, and executes them via AppleScript.

## Overview

WhisperScript allows you to speak natural language commands that get converted to executable AppleScript. For example:
- "Send an email to nano, and say we are meeting at 5 pm, do you want to go?" → Creates AppleScript to open Gmail and compose the email
- "Open calculator and compute 25 times 30" → Opens Calculator app and performs the calculation
- "Create a reminder for tomorrow at 2 PM to call the dentist" → Creates a reminder in the Reminders app

## Architecture

The project uses a hybrid Swift/Python architecture:

1. **Audio Capture & Speech Recognition**: Swift-based AudioService using macOS native Speech framework
2. **Intent Processing**: Python-based LLM integration using Anthropic's Claude API
3. **Script Execution**: Generated AppleScript is executed on macOS

### Components

- **Swift AudioService**: Native macOS audio capture and speech recognition using Speech framework
- **Python CLI**: Main application orchestration, LLM integration, and AppleScript generation
- **Configuration**: INI-based configuration for API keys and service paths

## Technology Stack

- **Python 3.11+**: Main application orchestration and LLM integration
- **Swift**: Native audio capture and speech recognition service
- **uv**: Python package and project manager
- **Speech Framework**: macOS native speech recognition (replaces OpenAI Whisper)
- **Anthropic Claude API**: LLM for natural language to AppleScript conversion
- **Ruff**: Code formatter and linter
- **MyPy**: Static type checking

## Development Setup

### Prerequisites
- macOS (required for AppleScript execution)
- Python 3.11 or higher
- uv package manager

### Installation

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Build the Swift AudioService
cd src/swift
swift build

# Install Python package in development mode
cd ../..
uv pip install -e .
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
# Process a recorded audio file
uv run whisperscript --recording path/to/audio.m4a

# Use default config.ini in project root
uv run whisperscript --ini-file config.ini --recording tests/data/test01.m4a
```

## Configuration

The application uses an INI configuration file (default: `config.ini`):

```ini
[paths]
audio_service = path/to/swift/.build/arm64-apple-macosx/debug/AudioService

[keys]
ANTHROPIC_API_KEY = your-api-key-here
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
│   ├── swift/                          # Swift AudioService
│   │   ├── Package.swift
│   │   └── Sources/
│   │       ├── AudioService/
│   │       │   └── main.swift          # Swift CLI entry point
│   │       └── AudioServiceLib/
│   │           └── AudioRecognitionService.swift  # Speech recognition
│   └── whisperscript/                  # Python package
│       ├── __init__.py
│       └── main.py                     # Python CLI entry point
├── tests/
│   ├── data/                           # Test audio files
│   │   ├── test01.m4a
│   │   └── test02.m4a
│   └── test_audio_capture.py
├── config.ini                          # Configuration file
├── pyproject.toml                      # Python project config
├── README.md
└── CLAUDE.md
```

## Commands to Remember

- `uv run ruff format && uv run ruff check`: Format and lint Python code
- `uv run ruff check --fix`: Auto-fix linting issues
- `uv run mypy src/`: Type check the Python codebase
- `uv run pytest`: Run tests
- `uv sync`: Sync Python dependencies
- `cd src/swift && swift build`: Build the Swift AudioService
- `uv run whisperscript --ini-file config.ini --recording tests/data/test01.m4a`: Test with sample audio
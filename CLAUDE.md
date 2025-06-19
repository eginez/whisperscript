# WhisperScript

A voice-controlled automation tool for macOS that listens to spoken instructions, processes them with an LLM, and executes them via AppleScript.

## Overview

WhisperScript allows you to speak natural language commands that get converted to executable AppleScript. For example:
- "Send an email to nano, and say we are meeting at 5 pm, do you want to go?" → Creates AppleScript to open Gmail and compose the email
- "Open calculator and compute 25 times 30" → Opens Calculator app and performs the calculation
- "Create a reminder for tomorrow at 2 PM to call the dentist" → Creates a reminder in the Reminders app

## Architecture

1. **Audio Capture**: Uses macOS audio APIs via PyObjC to capture microphone input
2. **Speech Recognition**: OpenAI Whisper for speech-to-text conversion
3. **Intent Processing**: LLM (OpenAI GPT or local model) to convert natural language to AppleScript
4. **Script Execution**: Generated AppleScript is executed on macOS

## Technology Stack

- **Python 3.11+**: Main application language
- **uv**: Python package and project manager
- **PyObjC**: Python-Objective-C bridge for macOS integration
- **OpenAI Whisper**: Speech recognition
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

# Install dependencies
uv sync

# Install in development mode
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
# Start the voice listener
uv run whisperscript

# Run with debug mode
uv run whisperscript --debug
```

## Configuration

The application will look for configuration in:
- `~/.config/whisperscript/config.toml`
- Environment variables for API keys

### Required Permissions

The application requires the following macOS permissions:
- **Microphone Access**: For audio capture
- **Accessibility**: For AppleScript execution
- **Automation**: For controlling other applications

## Project Structure

```
whisperscript/
├── src/
│   └── whisperscript/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── audio/
│       │   ├── __init__.py
│       │   └── capture.py       # Audio capture using PyObjC
│       ├── speech/
│       │   ├── __init__.py
│       │   └── whisper.py       # Whisper integration
│       ├── llm/
│       │   ├── __init__.py
│       │   └── processor.py     # LLM integration
│       └── automation/
│           ├── __init__.py
│           └── applescript.py   # AppleScript generation and execution
├── tests/
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

## Commands to Remember

- `uv run ruff format && uv run ruff check`: Format and lint code
- `uv run ruff check --fix`: Auto-fix linting issues
- `uv run mypy src/`: Type check the codebase
- `uv run pytest`: Run tests
- `uv sync`: Sync dependencies
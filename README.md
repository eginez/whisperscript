# WhisperScript

A voice-controlled automation tool for macOS that converts spoken instructions into executable AppleScript using AI.

## Features

- **Voice Recognition**: Native macOS Speech framework for accurate speech-to-text
- **AI-Powered**: Uses Anthropic's Claude API to convert natural language to AppleScript
- **macOS Integration**: Seamless automation of macOS applications
- **Hybrid Architecture**: Swift for audio processing, Python for orchestration

## Quick Start

### Prerequisites

- macOS (required for AppleScript and Speech framework)
- Python 3.11+
- Swift 5.9+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/whisperscript.git
cd whisperscript

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Build the Swift AudioService
cd src/swift
swift build
cd ../..

# Install the Python package
uv pip install -e .
```

### Configuration

1. Create a `config.ini` file in the project root:

```ini
[paths]
audio_service = /path/to/whisperscript/src/swift/.build/arm64-apple-macosx/debug/AudioService

[keys]
ANTHROPIC_API_KEY = your-anthropic-api-key-here
```

2. Get your Anthropic API key from [https://console.anthropic.com/](https://console.anthropic.com/)

### Usage

Process an audio file:

```bash
uv run whisperscript --ini-file config.ini --recording path/to/audio.m4a
```

Test with provided samples:

```bash
uv run whisperscript --ini-file config.ini --recording tests/data/test01.m4a
```

## Example Commands

Say something like:
- "Open calculator and compute 25 times 30"
- "Create a reminder for tomorrow at 2 PM to call the dentist"
- "Send an email to john@example.com saying the meeting is at 3 PM"

WhisperScript will generate and can execute the corresponding AppleScript automatically.

## Development

### Code Quality

```bash
# Format and lint Python code
uv run ruff format && uv run ruff check

# Type check
uv run mypy src/

# Run tests
uv run pytest
```

### Project Structure

- `src/swift/` - Swift AudioService for speech recognition
- `src/whisperscript/` - Python CLI and LLM integration
- `tests/` - Test files and sample audio data
- `config.ini` - Configuration file

## Permissions

WhisperScript requires the following macOS permissions:
- **Microphone Access**: For audio capture
- **Speech Recognition**: For processing voice input
- **Accessibility**: For AppleScript execution
- **Automation**: For controlling other applications

Grant these permissions when prompted by macOS.

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Troubleshooting

### Common Issues

- **Permission Denied**: Ensure all required macOS permissions are granted
- **Audio Service Path**: Update the `audio_service` path in `config.ini` to match your build location
- **API Key**: Verify your Anthropic API key is correct and has sufficient credits

### Getting Help

- Check the [CLAUDE.md](./CLAUDE.md) file for detailed development instructions
- File issues on GitHub for bugs or feature requests
- Review the test files in `tests/data/` for example audio formats
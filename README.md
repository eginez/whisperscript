# WhisperScript

A voice-controlled automation tool for macOS that converts spoken instructions into executable AppleScript using AI.

## Features

- **Native Speech Recognition**: macOS Speech framework for accurate speech-to-text
- **AI-Powered**: Uses Anthropic's Claude API to convert natural language to AppleScript
- **Self-Contained**: Pex-packaged Python executable with all dependencies
- **Menu Bar App**: Runs in background with system tray icon (UI needs work)
- **Environment Config**: Simple environment variable configuration

## Quick Start

### Prerequisites

- macOS 12+ (required for Speech framework and AppleScript)
- Python 3.9+
- Swift 5.9+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/whisperscript.git
cd whisperscript

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and build app bundle
uv sync --extra dev
uv run python build_backend.py
```

### Configuration

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Get your API key from [https://console.anthropic.com/](https://console.anthropic.com/)

### Usage

Test with an audio file:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
./dist/WhisperScript.app/Contents/MacOS/WhisperScript tests/data/test01.m4a
```

Run as menu bar app (UI needs work):

```bash
open dist/WhisperScript.app
```

## Example Commands

Say something like:
- "Hello find Slack and send a message to John"
- "Open calculator and compute 25 times 30"
- "Create a reminder for tomorrow at 2 PM to call the dentist"

WhisperScript will generate the corresponding AppleScript for these actions.

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

- `src/swift/` - Swift macOS app with speech recognition
- `src/whisperscript/` - Python package for LLM processing
- `build_backend.py` - App bundle build script
- `tests/` - Test files and sample audio data

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
- **API Key**: Verify your `ANTHROPIC_API_KEY` environment variable is set correctly
- **Python Compatibility**: Pex file supports Python 3.9-3.13 on Apple Silicon Macs
- **Menu Bar UI**: The menu bar interface is not fully implemented yet

### Getting Help

- Check the [CLAUDE.md](./CLAUDE.md) file for detailed development instructions
- File issues on GitHub for bugs or feature requests
- Review the test files in `tests/data/` for example audio formats
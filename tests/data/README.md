# Test Audio Files

Place audio files in this directory to test the speech recognition pipeline.

## Supported formats:
- `.wav` - WAV audio files
- `.m4a` - M4A audio files  
- `.mp3` - MP3 audio files
- `.aiff` - AIFF audio files

## Usage:
Each audio file will become a separate test case via pytest parametrization.

Run tests with:
```bash
uv run pytest tests/test_audio_capture.py::TestAudioCapture::test_process_audio_file -v
```

## Example files to add:
- `hello.wav` - Recording saying "Hello"
- `test_command.m4a` - Recording with a command like "Open calculator"
- `speech_sample.wav` - Any speech sample for testing recognition
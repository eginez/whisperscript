"""Tests for audio capture with recorded audio files."""

import pytest
from pathlib import Path
import json


def get_test_audio_files():
    """Get all audio files in test data directory for parametrization."""
    test_data_dir = Path(__file__).parent / "data"
    if not test_data_dir.exists():
        return []

    audio_extensions = {".wav", ".m4a", ".mp3", ".aiff"}
    return [
        str(f) for f in test_data_dir.iterdir() if f.suffix.lower() in audio_extensions
    ]


path_to_exec = "/Users/eginez/src/whsiperscript/src/swift/.build/arm64-apple-macosx/debug/AudioService"


@pytest.mark.parametrize("audio_file", get_test_audio_files())
def test_process_audio_file(audio_file: str):
    """Test processing individual audio file."""
    import subprocess as sp

    json_response = sp.check_output([path_to_exec, audio_file], text=True)
    parsed = json.loads(json_response)
    assert parsed["text"]

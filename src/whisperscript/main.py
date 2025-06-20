"""Main CLI entry point for WhisperScript."""
import json
import subprocess
from configparser import ConfigParser
from pathlib import Path

import click
from anthropic import Anthropic


def generate_applescript_from_speech(speech_text: str, api_key: str) -> str:
    """Generate AppleScript from speech text using Anthropic's Claude API.
    Args:
        speech_text: The parsed speech text to convert to AppleScript
    Returns:
        Generated AppleScript code as a string
    Raises:
        Exception: If there's an error communicating with the Anthropic API
    """
    anthropic = Anthropic(api_key=api_key)
    # TODO this should return a better json, so I can
    # add some extra code to handle errors, installation etc
    # for example add a key for the application that will be called.
    message = anthropic.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Generate only JSON with the following keys and no other text:
            - code: AppleScript code that implements this action: {speech_text}
            - description: A description of what the AppleScript does
            - caveats: Any important caveats or limitations of the script"""
        }]
    )

    return message.content[0].text

@click.command()
@click.option("--ini-file", type=click.Path(exists=True), help="Path to INI file", default="config.ini")
@click.option("--recording", type=click.Path(exists=True), help="Path to recording file")
def cli(ini_file: Path, recording: Path) -> None:
    """Voice-controlled automation tool for macOS."""
    click.echo("WhisperScript starting...")
    click.echo(f"INI file: {ini_file}")
    config = ConfigParser()
    config.read(ini_file)
    audio_command = config["paths"]["audio_service"].split()
    anthropic_api_key = config["keys"]["ANTHROPIC_API_KEY"]
    if recording:
        click.echo(f"Recording file: {recording}")
        audio_command.append(str(recording))

    try:
        speech_json = subprocess.check_output(audio_command, text=True)
        speech_parsed = json.loads(speech_json)
        applescript = generate_applescript_from_speech(speech_parsed['text'], api_key=anthropic_api_key)
        click.echo(f"Generated AppleScript:\n{applescript}")
        # TODO: Execute the generated AppleScript

    except subprocess.CalledProcessError as e:
        click.echo(f"Error processing audio: {e}", err=True)
    except json.JSONDecodeError as e:
        click.echo(f"Error parsing speech JSON: {e}", err=True)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)

    # TODO: Implement main application logic


if __name__ == "__main__":
    cli()

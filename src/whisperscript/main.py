"""Main CLI entry point for WhisperScript."""
import os
import sys

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

def cli() -> None:
    """Voice-controlled automation tool for macOS."""
    try:
        # Read speech text from stdin
        speech_text = sys.stdin.read().strip()

        if not speech_text:
            print("Error: No speech text received from stdin", file=sys.stderr)
            sys.exit(1)

        print(f"Processing speech: {speech_text}", file=sys.stderr)

        # Get API key from environment variable
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not anthropic_api_key:
            print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
            sys.exit(1)

        # Generate AppleScript
        import json
        response = json.loads(generate_applescript_from_speech(speech_text, api_key=anthropic_api_key))
        print(f"Generated AppleScript:\n{response['code']}")

        # TODO: Execute the generated AppleScript

    except Exception as e:
        print(f"Error processing speech: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cli()

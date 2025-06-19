"""Audio capture using Apple's Speech framework."""

from typing import Protocol

import objc
from AVFoundation import (
    AVAudioEngine,
    AVAudioFile,
    AVAudioPCMBuffer,
    AVAudioSession,
)
from Foundation import NSObject, NSURL
from Speech import (
    SFSpeechAudioBufferRecognitionRequest,
    SFSpeechRecognitionTask,
    SFSpeechRecognizer,
    SFSpeechRecognizerAuthorizationStatus,
)


class SpeechRecognitionDelegate(Protocol):
    """Protocol for speech recognition callbacks."""

    def on_speech_recognized(self, text: str) -> None:
        """Called when speech is recognized."""
        ...

    def on_recognition_error(self, error: str) -> None:
        """Called when recognition fails."""
        ...


class AudioCapture(NSObject):
    """Audio capture and speech recognition using Apple frameworks."""

    def init(self):
        """Initialize the AudioCapture instance."""
        objc.super(AudioCapture, self).init()
        self.audio_engine = None
        self.speech_recognizer = None
        self.recognition_request = None
        self.recognition_task = None
        self.delegate = None
        return self

    def check_permissions(self) -> bool:
        """Check if microphone and speech recognition permissions are granted."""
        # For now, let's try to actually use the APIs instead of checking status
        # since the status values seem unreliable in our environment
        
        try:
            # Test microphone access by creating audio engine
            from AVFoundation import AVAudioEngine
            engine = AVAudioEngine.alloc().init()
            input_node = engine.inputNode()
            engine.prepare()
            success = engine.startAndReturnError_(None)
            if isinstance(success, tuple):
                mic_works = success[0]
            else:
                mic_works = bool(success)
            engine.stop()
            
            # Test speech recognition by creating recognizer
            recognizer = SFSpeechRecognizer.alloc().init()
            speech_works = recognizer is not None and recognizer.isAvailable()
            
            return mic_works and speech_works
            
        except Exception:
            return False

    def setup_audio(self, delegate: SpeechRecognitionDelegate) -> bool:
        """Setup audio capture and speech recognition."""
        self.delegate = delegate

        # Check permissions first
        if not self.check_permissions():
            delegate.on_recognition_error("Microphone or speech recognition permission denied")
            return False

        # Initialize speech recognizer
        self.speech_recognizer = SFSpeechRecognizer.alloc().init()
        if not self.speech_recognizer:
            delegate.on_recognition_error("Speech recognizer not available")
            return False

        # Initialize audio engine
        self.audio_engine = AVAudioEngine.alloc().init()
        return True

    def _start_recognition_task(self) -> bool:
        """Start the speech recognition task with current request."""
        if not self.speech_recognizer or not self.recognition_request:
            return False
            
        try:
            self.recognition_task = self.speech_recognizer.recognitionTaskWithRequest_resultHandler_(
                self.recognition_request, self._handle_recognition_result
            )
            return True
        except Exception as e:
            if self.delegate:
                self.delegate.on_recognition_error(f"Failed to start recognition task: {e}")
            return False

    def start_listening(self) -> bool:
        """Start listening for speech from microphone."""
        if not self.audio_engine or not self.speech_recognizer:
            return False

        try:
            # Create recognition request
            self.recognition_request = (
                SFSpeechAudioBufferRecognitionRequest.alloc().init()
            )

            # Start recognition task
            if not self._start_recognition_task():
                return False

            # Configure audio engine
            input_node = self.audio_engine.inputNode()
            recording_format = input_node.outputFormatForBus_(0)

            # Install tap on input node
            input_node.installTapOnBus_bufferSize_format_block_(
                0, 1024, recording_format, self._handle_audio_buffer
            )

            # Start audio engine
            self.audio_engine.prepare()
            self.audio_engine.startAndReturnError_(None)

            return True

        except Exception as e:
            if self.delegate:
                self.delegate.on_recognition_error(f"Failed to start listening: {e}")
            return False

    def process_audio_file(self, file_path: str) -> bool:
        """Process audio from a file instead of live microphone."""
        if not self.speech_recognizer:
            if self.delegate:
                self.delegate.on_recognition_error("Speech recognizer not initialized")
            return False

        try:
            # Create recognition request
            self.recognition_request = (
                SFSpeechAudioBufferRecognitionRequest.alloc().init()
            )

            # Load and process audio file
            file_url = NSURL.fileURLWithPath_(file_path)
            audio_file = AVAudioFile.alloc().initForReading_error_(file_url, None)[0]
            
            if not audio_file:
                if self.delegate:
                    self.delegate.on_recognition_error(f"Could not load audio file: {file_path}")
                return False

            # Read audio into buffer
            audio_format = audio_file.processingFormat()
            frame_count = int(audio_file.length())
            buffer = AVAudioPCMBuffer.alloc().initWithPCMFormat_frameCapacity_(
                audio_format, frame_count
            )

            success = audio_file.readIntoBuffer_error_(buffer, None)[0]
            if not success:
                if self.delegate:
                    self.delegate.on_recognition_error("Failed to read audio file")
                return False

            # Start recognition task
            if not self._start_recognition_task():
                return False

            # Feed audio buffer and end
            self.recognition_request.appendAudioPCMBuffer_(buffer)
            self.recognition_request.endAudio()

            return True

        except Exception as e:
            if self.delegate:
                self.delegate.on_recognition_error(f"Failed to process audio file: {e}")
            return False

    def _handle_audio_buffer(self, buffer: AVAudioPCMBuffer, when: objc.pyobjc_id) -> None:
        """Handle audio buffer from microphone."""
        if self.recognition_request:
            self.recognition_request.appendAudioPCMBuffer_(buffer)

    def _handle_recognition_result(self, result: objc.pyobjc_id, error: objc.pyobjc_id) -> None:
        """Handle speech recognition results."""
        if error and self.delegate:
            self.delegate.on_recognition_error(f"Recognition error: {error}")
            return

        if result and self.delegate:
            # Get the best transcription
            best_string = result.bestTranscription().formattedString()
            if best_string and result.isFinal():
                self.delegate.on_speech_recognized(best_string)

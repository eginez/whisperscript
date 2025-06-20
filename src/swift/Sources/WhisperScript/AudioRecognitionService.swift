import Foundation
import AVFoundation
import Speech

public class AudioRecognitionService: NSObject, SFSpeechRecognizerDelegate {
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))!
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    
    private var isListening = false
    private var lastSpeechTime = Date()
    private let silenceTimeout: TimeInterval = 5.0
    
    public override init() {
        super.init()
        speechRecognizer.delegate = self
    }
    
    public func requestPermissions() async -> Bool {
        return await withCheckedContinuation { continuation in
            SFSpeechRecognizer.requestAuthorization { status in
                continuation.resume(returning: status == .authorized)
            }
        }
    }
    
    public func startListening() throws {
        if audioEngine.isRunning {
            audioEngine.stop()
            recognitionRequest?.endAudio()
        }
        
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        
        let inputNode = audioEngine.inputNode
        
        guard let recognitionRequest = recognitionRequest else {
            throw NSError(domain: "AudioRecognitionService", code: 1, userInfo: [NSLocalizedDescriptionKey: "Unable to create recognition request"])
        }
        
        recognitionRequest.shouldReportPartialResults = true
        
        recognitionTask = speechRecognizer.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            guard let self = self else { return }
            
            if let result = result {
                let recognizedText = result.bestTranscription.formattedString
                self.lastSpeechTime = Date()
                
                if result.isFinal {
                    self.outputResult(recognizedText)
                    self.stopListening()
                }
            }
            
            if let error = error {
                self.outputError("Recognition error: \(error.localizedDescription)")
                self.stopListening()
            }
        }
        
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            recognitionRequest.append(buffer)
        }
        
        audioEngine.prepare()
        try audioEngine.start()
        
        isListening = true
        lastSpeechTime = Date()
        
        // Start silence detection timer
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { [weak self] timer in
            guard let self = self else {
                timer.invalidate()
                return
            }
            
            if !self.isListening {
                timer.invalidate()
                return
            }
            
            let timeSinceLastSpeech = Date().timeIntervalSince(self.lastSpeechTime)
            if timeSinceLastSpeech > self.silenceTimeout {
                timer.invalidate()
                self.recognitionRequest?.endAudio()
            }
        }
    }
    
    public func stopListening() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        
        recognitionRequest?.endAudio()
        recognitionRequest = nil
        recognitionTask?.cancel()
        recognitionTask = nil
        
        isListening = false
    }
    
    public func processAudioFile(filePath: String) async throws {
        guard FileManager.default.fileExists(atPath: filePath) else {
            outputError("Audio file not found: \(filePath)")
            return
        }
        
        let fileURL = URL(fileURLWithPath: filePath)
        let request = SFSpeechURLRecognitionRequest(url: fileURL)
        request.shouldReportPartialResults = false
        
        return try await withCheckedThrowingContinuation { continuation in
            recognitionTask = speechRecognizer.recognitionTask(with: request) { [weak self] result, error in
                guard let self = self else {
                    continuation.resume(throwing: NSError(domain: "AudioRecognitionService", code: 2, userInfo: [NSLocalizedDescriptionKey: "Service deallocated"]))
                    return
                }
                
                if let error = error {
                    self.outputError("File recognition error: \(error.localizedDescription)")
                    continuation.resume(throwing: error)
                    return
                }
                
                if let result = result, result.isFinal {
                    let recognizedText = result.bestTranscription.formattedString
                    self.outputResult(recognizedText)
                    continuation.resume()
                }
            }
        }
    }
    
    public func outputResult(_ text: String) {
        let result = [
            "status": "success",
            "text": text,
            "timestamp": ISO8601DateFormatter().string(from: Date())
        ]
        
        if let jsonData = try? JSONSerialization.data(withJSONObject: result, options: []),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString)
        }
        
        // Call Python script with the recognized text
        callPythonScript(with: text)
    }
    
    private func callPythonScript(with text: String) {
        // Get the path to the Python script in the app bundle
        let bundlePath = Bundle.main.bundlePath
        let pythonScriptPath = "\(bundlePath)/Contents/Resources/whisperscript.pex"
        
        let process = Process()
        process.executableURL = URL(fileURLWithPath: pythonScriptPath)
        
        let pipe = Pipe()
        process.standardInput = pipe
        
        do {
            try process.run()
            
            // Send the recognized text to the Python script via stdin
            let inputData = text.data(using: .utf8)!
            pipe.fileHandleForWriting.write(inputData)
            pipe.fileHandleForWriting.closeFile()
            
            process.waitUntilExit()
            
            if process.terminationStatus != 0 {
                outputError("Python script exited with status: \(process.terminationStatus)")
            }
            
        } catch {
            outputError("Failed to run Python script: \(error.localizedDescription)")
        }
    }
    
    public func outputError(_ message: String) {
        let error = [
            "status": "error",
            "message": message,
            "timestamp": ISO8601DateFormatter().string(from: Date())
        ]
        
        if let jsonData = try? JSONSerialization.data(withJSONObject: error, options: []),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString)
        }
    }
}
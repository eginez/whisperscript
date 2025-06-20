import Foundation
import AudioServiceLib

@main
struct AudioServiceApp {
    static func main() async {
        let service = AudioRecognitionService()
        let arguments = CommandLine.arguments
        
        guard await service.requestPermissions() else {
            service.outputError("Permission denied for speech recognition")
            exit(1)
        }
        
        do {
            // Check if a file path was provided as an argument
            if arguments.count > 1 {
                let filePath = arguments[1]
                try await service.processAudioFile(filePath: filePath)
            } else {
                // Use live microphone input
                try service.startListening()
                
                // Keep the service running
                while true {
                    try await Task.sleep(nanoseconds: 1_000_000_000) // Sleep for 1 second
                }
            }
            
        } catch {
            service.outputError("Failed to process audio: \(error.localizedDescription)")
            exit(1)
        }
    }
}
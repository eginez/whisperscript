import Foundation
import Cocoa


@MainActor class WhisperScriptApp: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem?
    private var service: AudioRecognitionService?
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Create status bar item
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
        
        if let button = statusItem?.button {
            button.title = "🎤"  // Microphone emoji as icon
            button.action = #selector(statusBarButtonClicked)
            button.target = self
        }
        
        // Create menu
        let menu = NSMenu()
        menu.addItem(NSMenuItem(title: "Start Listening", action: #selector(startListening), keyEquivalent: ""))
        menu.addItem(NSMenuItem(title: "Stop Listening", action: #selector(stopListening), keyEquivalent: ""))
        menu.addItem(NSMenuItem.separator())
        menu.addItem(NSMenuItem(title: "Quit", action: #selector(quit), keyEquivalent: "q"))
        
        statusItem?.menu = menu
        
        // Initialize audio service
        service = AudioRecognitionService()
        
        // Check command line arguments for file processing
        let arguments = CommandLine.arguments
        if arguments.count > 1 {
            // Process file and quit
            let filePath = arguments[1]
            Task {
                await processAudioFile(filePath: filePath)
                NSApplication.shared.terminate(nil)
            }
            return
        }
        
        // Request permissions and start listening
        Task {
            await requestPermissionsAndStart()
        }
    }
    
    @objc private func statusBarButtonClicked() {
        // Menu will be shown automatically
    }
    
    @objc private func startListening() {
        Task {
            await requestPermissionsAndStart()
        }
    }
    
    @objc private func stopListening() {
        service?.stopListening()
        statusItem?.button?.title = "🎤"
    }
    
    @objc private func quit() {
        NSApplication.shared.terminate(nil)
    }
    
    private func requestPermissionsAndStart() async {
        guard let service = service else { return }
        
        guard await service.requestPermissions() else {
            service.outputError("Permission denied for speech recognition")
            return
        }
        
        do {
            try service.startListening()
            statusItem?.button?.title = "🔴"  // Red dot when listening
        } catch {
            service.outputError("Failed to start listening: \(error.localizedDescription)")
        }
    }
    
    private func processAudioFile(filePath: String) async {
        guard let service = service else { return }
        
        guard await service.requestPermissions() else {
            service.outputError("Permission denied for speech recognition")
            return
        }
        
        do {
            try await service.processAudioFile(filePath: filePath)
        } catch {
            service.outputError("Failed to process audio file: \(error.localizedDescription)")
        }
    }
}

// Entry point
let app = NSApplication.shared
let delegate = WhisperScriptApp()
app.delegate = delegate

// Hide dock icon - run as menu bar only app
app.setActivationPolicy(.accessory)

app.run()
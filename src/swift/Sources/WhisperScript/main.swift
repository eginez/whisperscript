import Foundation
import Cocoa


@MainActor class WhisperScriptApp: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem?
    private var service: AudioRecognitionService?
    
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        print("WhisperScript app launched!")
        
        // Create status bar item with fixed length
        statusItem = NSStatusBar.system.statusItem(withLength: 30)
        
        if let button = statusItem?.button {
            button.title = "🎤"  // Microphone emoji as icon
            button.action = #selector(statusBarButtonClicked)
            button.target = self
        } else {
            print("Failed to get status bar button")
        }
        
        // Create menu
        let menu = NSMenu()
        
        let startItem = NSMenuItem(title: "Start Listening", action: #selector(startListening), keyEquivalent: "")
        startItem.target = self
        menu.addItem(startItem)
        
        let stopItem = NSMenuItem(title: "Stop Listening", action: #selector(stopListening), keyEquivalent: "")
        stopItem.target = self
        menu.addItem(stopItem)
        
        menu.addItem(NSMenuItem.separator())
        
        let quitItem = NSMenuItem(title: "Quit", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
        
        statusItem?.menu = menu
        
        print("Menu bar item created with 🎤 icon")
        print("Status item: \(statusItem?.description ?? "nil")")
        
        // Force the status item to be visible
        statusItem?.isVisible = true
        
        // Set activation policy after menu bar is set up
        NSApplication.shared.setActivationPolicy(.accessory)
        
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
NSApplication.shared.delegate = WhisperScriptApp()
NSApplication.shared.run()
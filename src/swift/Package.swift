// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "WhisperScript",
    platforms: [
        .macOS(.v12)
    ],
    products: [
        .executable(name: "WhisperScript", targets: ["WhisperScript"]),
    ],
    targets: [
        .executableTarget(
            name: "WhisperScript",
            path: "Sources/WhisperScript",
            linkerSettings: [
                .linkedFramework("AVFoundation"),
                .linkedFramework("Speech"),
                .linkedFramework("Foundation"),
                .linkedFramework("Cocoa")
            ]
        ),
    ]
)

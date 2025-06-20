// swift-tools-version: 6.1
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "AudioService",
    platforms: [
        .macOS(.v13)
    ],
    targets: [
        .target(
            name: "AudioServiceLib",
            linkerSettings: [
                .linkedFramework("AVFoundation"),
                .linkedFramework("Speech"),
                .linkedFramework("Foundation")
            ]
        ),
        .executableTarget(
            name: "AudioService",
            dependencies: ["AudioServiceLib"]
        ),
    ]
)

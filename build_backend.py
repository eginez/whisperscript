"""Custom build hook for WhisperScript hybrid Swift/Python app."""
import os
import shutil
import subprocess
import sys
from pathlib import Path


class WhisperScriptBuilder:
    """Custom builder for WhisperScript app bundle."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        self.app_name = "WhisperScript"

    def clean(self):
        """Clean previous builds."""
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        self.build_dir.mkdir(parents=True)
        self.dist_dir.mkdir(parents=True)

    def build_python_pex(self):
        """Build Python executable using Pex."""
        print("🐍 Building Python Pex executable...")
        pex_file = self.build_dir / "whisperscript.pex"

        cmd = [
            sys.executable, "-m", "pex",
            ".", "-c", "whisperscript",
            "--python-shebang", "/usr/bin/env python3",
            "--platform", "macosx_11_0_arm64-cp-39-cp39",
            "--platform", "macosx_11_0_arm64-cp-310-cp310",
            "--platform", "macosx_11_0_arm64-cp-311-cp311",
            "--platform", "macosx_11_0_arm64-cp-312-cp312",
            "--platform", "macosx_11_0_arm64-cp-313-cp313",
            "-v",  # Verbose output
            "-o", str(pex_file)
        ]

        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=self.root_dir, check=True)
        pex_file.chmod(0o755)
        return pex_file

    def build_swift_executable(self):
        """Build Swift executable using Package.swift."""
        print("🔨 Building Swift executable...")
        swift_dir = self.root_dir / "src" / "swift"

        if not swift_dir.exists():
            raise FileNotFoundError(f"Swift directory not found: {swift_dir}")

        # Build Swift package
        subprocess.run(
            ["swift", "build", "-c", "release"],
            cwd=swift_dir,
            check=True
        )

        # Copy executable to build dir
        swift_exe = swift_dir / ".build" / "release" / self.app_name
        if not swift_exe.exists():
            raise FileNotFoundError(f"Swift executable not found: {swift_exe}")

        dest_exe = self.build_dir / self.app_name
        shutil.copy2(swift_exe, dest_exe)
        return dest_exe

    def create_app_bundle(self, swift_exe: Path, pex_file: Path):
        """Create macOS app bundle."""
        print("📦 Creating app bundle...")
        app_bundle = self.dist_dir / f"{self.app_name}.app"
        contents_dir = app_bundle / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"

        # Create bundle structure
        macos_dir.mkdir(parents=True)
        resources_dir.mkdir(parents=True)

        # Copy executables
        app_exe = macos_dir / self.app_name
        shutil.copy2(swift_exe, app_exe)
        app_exe.chmod(0o755)

        pex_dest = resources_dir / "whisperscript.pex"
        shutil.copy2(pex_file, pex_dest)
        pex_dest.chmod(0o755)

        # Copy Info.plist
        info_plist = self.root_dir / "Info.plist"
        if info_plist.exists():
            shutil.copy2(info_plist, contents_dir / "Info.plist")

        # Set bundle permissions
        os.chmod(app_bundle, 0o755)

        return app_bundle

    def create_app_bundle_simple(self, swift_exe: Path):
        """Create macOS app bundle with just Swift executable."""
        print("📦 Creating app bundle...")
        app_bundle = self.dist_dir / f"{self.app_name}.app"
        contents_dir = app_bundle / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"

        # Create bundle structure
        macos_dir.mkdir(parents=True)
        resources_dir.mkdir(parents=True)

        # Copy Swift executable
        app_exe = macos_dir / self.app_name
        shutil.copy2(swift_exe, app_exe)
        app_exe.chmod(0o755)

        # Copy Info.plist
        info_plist = self.root_dir / "Info.plist"
        if info_plist.exists():
            shutil.copy2(info_plist, contents_dir / "Info.plist")

        # Set bundle permissions
        os.chmod(app_bundle, 0o755)

        return app_bundle

    def build_app(self):
        """Build complete app bundle."""
        print(f"🏗️  Building {self.app_name}.app...")

        self.clean()

        # Build components
        pex_file = self.build_python_pex()
        swift_exe = self.build_swift_executable()

        # Create app bundle with both executables
        app_bundle = self.create_app_bundle(swift_exe, pex_file)

        print(f"✅ Build complete: {app_bundle}")
        return app_bundle


def main():
    """Main entry point for build script."""
    builder = WhisperScriptBuilder(".")
    app_bundle = builder.build_app()

    print("\n🎉 App bundle created successfully!")
    print(f"📍 Location: {app_bundle}")
    print("\nTo install:")
    print(f"  cp -r {app_bundle} /Applications/")
    print("\nTo test:")
    print(f"  open {app_bundle}")


if __name__ == "__main__":
    main()

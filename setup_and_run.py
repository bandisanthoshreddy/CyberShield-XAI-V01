#!/usr/bin/env python3
"""
CyberShield — One-click setup & launcher
Run this file: python setup_and_run.py
"""
import subprocess, sys, os, webbrowser, time
from pathlib import Path

PACKAGES = ["fastapi", "uvicorn[standard]"]
PORT     = 5050

def check_python():
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 8):
        print(f"❌ Python 3.8+ required. You have {v.major}.{v.minor}")
        sys.exit(1)
    print(f"✓ Python {v.major}.{v.minor}.{v.micro}")

def install_packages():
    print("\nInstalling dependencies…")
    for pkg in PACKAGES:
        name = pkg.split("[")[0]
        try:
            __import__(name.replace("-","_"))
            print(f"  ✓ {name} already installed")
        except ImportError:
            print(f"  Installing {pkg}…")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
            print(f"  ✓ {name} installed")

def launch():
    app_file = Path(__file__).parent / "app.py"
    if not app_file.exists():
        print("❌ app.py not found. Make sure you're in the cybershield_demo folder.")
        sys.exit(1)

    print(f"\n{'='*52}")
    print("  🛡️  CyberShield Demo")
    print(f"  → http://localhost:{PORT}")
    print("  Opening browser in 2 seconds…")
    print("  Press Ctrl+C to stop the server")
    print(f"{'='*52}\n")

    # Open browser after small delay
    def open_browser():
        time.sleep(2)
        webbrowser.open(f"http://localhost:{PORT}")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    os.chdir(Path(__file__).parent)
    subprocess.run([
        sys.executable, "-m", "uvicorn", "app:app",
        "--host", "0.0.0.0", "--port", str(PORT), "--reload"
    ])

if __name__ == "__main__":
    check_python()
    install_packages()
    launch()

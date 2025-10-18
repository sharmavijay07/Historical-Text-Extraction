"""
Setup Verification Script
Checks if all required packages and dependencies are properly installed
"""

import sys
from pathlib import Path

print("=" * 80)
print("MULTI-LANGUAGE HISTORICAL TEXT EXTRACTOR - SETUP VERIFICATION")
print("=" * 80)
print()

# Check Python version
print("✓ Python Version Check")
print(f"  Python: {sys.version}")
print(f"  Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print()

# Check required packages
print("✓ Checking Required Packages")
print()

packages_to_check = {
    "streamlit": "Web UI framework",
    "cv2": "OpenCV - Image processing",
    "numpy": "Numerical computing",
    "PIL": "Pillow - Image handling",
    "pytesseract": "Tesseract OCR wrapper",
}

missing_packages = []
installed_packages = []

for package_name, description in packages_to_check.items():
    try:
        if package_name == "cv2":
            import cv2
            version = cv2.__version__
        elif package_name == "PIL":
            from PIL import Image
            version = Image.__version__ if hasattr(Image, '__version__') else "Installed"
        elif package_name == "pytesseract":
            import pytesseract
            version = pytesseract.pytesseract.__version__ if hasattr(pytesseract.pytesseract, '__version__') else "Installed"
        else:
            module = __import__(package_name)
            version = module.__version__ if hasattr(module, '__version__') else "Installed"
        
        print(f"  ✅ {package_name:20} - {description:35} [{version}]")
        installed_packages.append(package_name)
    except ImportError as e:
        print(f"  ❌ {package_name:20} - {description:35} [NOT FOUND]")
        missing_packages.append(package_name)

print()

# Check Tesseract OCR installation
print("✓ Checking Tesseract OCR Installation")
print()

try:
    import pytesseract
    import subprocess
    
    # Try to get Tesseract version
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            tesseract_version = result.stdout.split('\n')[0]
            print(f"  ✅ Tesseract OCR Found")
            print(f"     {tesseract_version}")
            print()
        else:
            print(f"  ⚠️  Tesseract found but version check failed")
            print(f"     Manual installation may be required")
            print(f"     Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            print()
    except FileNotFoundError:
        print(f"  ❌ Tesseract OCR NOT FOUND")
        print(f"     Installation required!")
        print()
        print(f"     Windows: Download installer from")
        print(f"     https://github.com/UB-Mannheim/tesseract/wiki")
        print()
        print(f"     Mac: brew install tesseract")
        print()
        print(f"     Linux: sudo apt-get install tesseract-ocr")
        print()
    except Exception as e:
        print(f"  ⚠️  Tesseract check error: {str(e)}")
        print()

except ImportError:
    print(f"  ❌ pytesseract not installed")
    print()

# Check project files
print("✓ Checking Project Files")
print()

project_root = Path(__file__).parent
required_files = [
    "app.py",
    "utils.py",
    "examples.py",
    "config.json",
    "requirements.txt",
    "README.md",
    "QUICKSTART.md",
    "LANGUAGE_REFERENCE.md",
    "PROJECT_SUMMARY.md",
]

all_files_present = True
for filename in required_files:
    filepath = project_root / filename
    if filepath.exists():
        file_size = filepath.stat().st_size
        print(f"  ✅ {filename:30} [{file_size:,} bytes]")
    else:
        print(f"  ❌ {filename:30} [NOT FOUND]")
        all_files_present = False

print()

# Summary
print("=" * 80)
print("SETUP SUMMARY")
print("=" * 80)
print()

if missing_packages:
    print(f"❌ Missing Packages: {', '.join(missing_packages)}")
    print(f"   Install with: pip install -r requirements.txt")
    print()
else:
    print(f"✅ All Python packages installed!")
    print()

if all_files_present:
    print(f"✅ All project files present!")
    print()
else:
    print(f"❌ Some project files missing!")
    print()

# Ready to run?
print("=" * 80)
if missing_packages:
    print("❌ SETUP NOT COMPLETE")
    print()
    print("Action required:")
    print("1. Install missing Python packages: pip install -r requirements.txt")
    print("2. Install Tesseract OCR (see instructions above)")
else:
    print("✅ SETUP COMPLETE - READY TO RUN!")
    print()
    print("To start the application, run:")
    print("  streamlit run app.py")
    print()

print("=" * 80)

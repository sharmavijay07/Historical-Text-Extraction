# 🪟 Windows Installation Guide

## Complete Step-by-Step Installation for Windows

### Prerequisites
- Windows 7 or later
- Python 3.8+ installed
- Internet connection

---

## Step 1: Install Python (if not already installed)

### Option A: Using Python.org
1. Visit https://www.python.org/downloads/
2. Download Python 3.11 or 3.12 (Windows 64-bit)
3. Run installer
4. **IMPORTANT:** Check "Add Python to PATH"
5. Click "Install Now"
6. Wait for completion

### Verify Python Installation
Open Command Prompt or PowerShell and run:
```powershell
python --version
```

Should show: `Python 3.11.x` or similar

---

## Step 2: Install Tesseract OCR (Critical)

### Download Tesseract
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download: `tesseract-ocr-w64-setup-v5.x.exe` (64-bit Windows)
3. Run the installer

### Installation Steps
1. Click "Next" on the welcome screen
2. Accept license → Click "Next"
3. **Choose Installation Path:**
   - Default: `C:\Program Files\Tesseract-OCR`
   - Click "Next"
4. **Language Data - IMPORTANT:**
   - Check all languages you need, especially:
     - ✅ English (default)
     - ✅ Hindi
     - ✅ Bengali
     - ✅ Sanskrit (if available)
     - ✅ Arabic
     - ✅ Chinese
   - Click "Next"
5. **Additional Components:**
   - Keep defaults checked
   - Click "Next"
6. Click "Install"
7. Wait for completion
8. Click "Finish"

### Verify Tesseract Installation
Open Command Prompt and run:
```cmd
tesseract --version
```

Should show version info like: `tesseract 5.x.x`

---

## Step 3: Add Tesseract to Python Path (if needed)

If you get `pytesseract.TesseractNotFoundError`, configure the path:

### Option A: Add to Windows PATH Environment Variable
1. Press `Windows Key + R`
2. Type: `sysdm.cpl`
3. Go to "Advanced" tab
4. Click "Environment Variables"
5. Under "System variables", click "New"
6. **Variable name:** `TESSERACT_CMD`
7. **Variable value:** `C:\Program Files\Tesseract-OCR\tesseract.exe`
8. Click OK → OK → OK
9. Restart Command Prompt

### Option B: Configure in Python Code
Edit `app.py` and add this near the top (after imports):
```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

---

## Step 4: Set Up Project Directory

### Create Virtual Environment (Optional but Recommended)

```powershell
# Navigate to project folder
cd "c:\Users\SURAJ\Documents\5clear chatapp\sai_maam\ocr_app"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

If you get execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Step 5: Install Python Packages

### Install from requirements.txt

```powershell
# Make sure you're in the project directory
cd "c:\Users\SURAJ\Documents\5clear chatapp\sai_maam\ocr_app"

# Install packages
pip install -r requirements.txt
```

### Packages being installed:
- **streamlit** - Web UI framework
- **opencv-python** - Image processing
- **pytesseract** - OCR wrapper
- **pillow** - Image handling
- **numpy** - Numerical computing

### If installation fails:
```powershell
# Update pip first
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt
```

---

## Step 6: Verify Installation

### Run Verification Script
```powershell
python verify_setup.py
```

Expected output:
```
✅ Python Version Check
✅ Checking Required Packages
  ✅ streamlit
  ✅ cv2
  ✅ numpy
  ✅ PIL
  ✅ pytesseract
✅ Checking Tesseract OCR Installation
  ✅ Tesseract OCR Found
✅ Checking Project Files
  ✅ All project files present

✅ SETUP COMPLETE - READY TO RUN!
```

---

## Step 7: Download Additional Language Data (Optional)

For historical languages like Sanskrit, Tamil, etc.:

### Option A: Automatic (during Tesseract installation)
Already done in Step 2 - you selected languages during installation.

### Option B: Manual Download

1. Go to: https://github.com/tesseract-ocr/tessdata
2. Download `.traineddata` files for languages you need:
   - `san.traineddata` (Sanskrit)
   - `tam.traineddata` (Tamil)
   - `hin.traineddata` (Hindi)
   - `ara.traineddata` (Arabic)
   - etc.
3. Copy to: `C:\Program Files\Tesseract-OCR\tessdata\`

---

## Step 8: Run the Application

### Start Streamlit App

```powershell
# Make sure virtual environment is activated (if you created one)
# .\venv\Scripts\Activate.ps1

# Navigate to project folder
cd "c:\Users\SURAJ\Documents\5clear chatapp\sai_maam\ocr_app"

# Run the app
streamlit run app.py
```

### Expected Output
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

The browser should automatically open. If not, manually visit: `http://localhost:8501`

---

## ⚠️ Troubleshooting

### Error: "pytesseract.TesseractNotFoundError"

**Solution:**
1. Verify Tesseract is installed: `tesseract --version`
2. If not, install from: https://github.com/UB-Mannheim/tesseract/wiki
3. Add to PATH or configure in Python (see Step 3)
4. Restart Command Prompt and try again

### Error: "No module named 'streamlit'"

**Solution:**
```powershell
pip install streamlit
```

### Error: "No module named 'cv2'"

**Solution:**
```powershell
pip install opencv-python
```

### Error: "Image language is not available"

**Solution:**
1. Download language file from: https://github.com/tesseract-ocr/tessdata
2. Place in: `C:\Program Files\Tesseract-OCR\tessdata\`
3. Restart app

### Streamlit app is slow

**Solution:**
- Reduce number of selected languages
- Reduce image scale factor
- Use smaller images
- Close other applications

### Can't activate virtual environment

**Solution:**
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Try activating again
.\venv\Scripts\Activate.ps1
```

---

## 📋 Quick Command Reference

```powershell
# Navigate to project
cd "c:\Users\SURAJ\Documents\5clear chatapp\sai_maam\ocr_app"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Verify setup
python verify_setup.py

# Run application
streamlit run app.py

# Run examples
python examples.py

# Deactivate virtual environment
deactivate
```

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Python added to PATH
- [ ] Tesseract OCR installed
- [ ] Tesseract path configured (or in PATH)
- [ ] Virtual environment created (optional)
- [ ] Python packages installed from requirements.txt
- [ ] Verification script runs successfully
- [ ] Streamlit app starts without errors
- [ ] Browser opens to localhost:8501

---

## 🚀 Next Steps

1. ✅ Complete this installation guide
2. ✅ Run verification script
3. ✅ Start the application
4. ✅ Upload test images
5. ✅ Extract text
6. ✅ Download results

---

## 📞 Still Having Issues?

1. Check the main `README.md` for more details
2. Review `QUICKSTART.md` for common scenarios
3. Check `LANGUAGE_REFERENCE.md` for language-specific info
4. Visit Tesseract GitHub: https://github.com/tesseract-ocr/tesseract

---

**Your setup is now ready for text extraction!** 🎉

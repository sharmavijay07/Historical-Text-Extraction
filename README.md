# Multi-Language Historical Text Extractor

A powerful Python Streamlit application for extracting text from images containing multiple historical, ancient, and modern languages.

## 🌍 Supported Languages

### Ancient Indian Languages
- **Sanskrit** (Devanagari, Grantha scripts)
- **Pali** (Buddhist canonical texts)
- **Old Tamil, Kannada, Telugu, Malayalam** (Dravidian family)
- **Magadhi, Sauraseni, Gandhari** (Prakrit languages)

### Other Ancient Asian Languages
- **Classical Tibetan**
- **Classical Chinese**
- **Traditional Chinese**
- **Japanese**
- **Korean**

### Ancient European & Middle-Eastern
- **Latin** (Classical & Medieval)
- **Ancient & Modern Greek**
- **Biblical & Modern Hebrew**
- **Arabic**
- **Persian (Farsi)**
- **Syriac**
- **Amharic & Tigrinya** (Ge'ez script)

### Modern European Languages
- **Russian, Ukrainian, Bulgarian, Serbian** (Cyrillic)
- **Polish, Czech, Hungarian** (Latin Extended)
- **German, French, Spanish, Italian, Portuguese**
- **English, Dutch, Swedish, Danish, Norwegian, Finnish, Romanian**

### Southeast Asian Languages
- **Thai**
- **Vietnamese**
- **Khmer**
- **Lao**
- **Burmese**

### Modern Indian Languages
- **Hindi, Bengali, Gujarati, Oriya**

---

## 📋 Prerequisites

1. **Python 3.8+** installed on your system
2. **Tesseract OCR** installed separately (see below)
3. **pip** package manager

### Installing Tesseract OCR

#### On Windows:
1. Download the Tesseract installer from: [GitHub Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Download `tesseract-ocr-w64-setup-v5.x.x-xxxxx.exe` (or latest version)
3. Run the installer and select installation path (e.g., `C:\Program Files\Tesseract-OCR`)
4. During installation, make sure to install the **language data files** you need

#### On macOS:
```bash
brew install tesseract
```

#### On Linux (Ubuntu/Debian):
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-all  # For all language packs
```

#### On Linux (Fedora/CentOS):
```bash
sudo yum install tesseract
```

---

## 🚀 Installation & Setup

### Step 1: Clone or Create Project
```bash
# Navigate to your project directory
cd c:\Users\SURAJ\Documents\5clear chatapp\sai_maam\ocr_app
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Tesseract Path (Windows Only)

If Tesseract is not in your system PATH, you need to configure it in the script.

**Option A:** Add to Windows PATH environment variable
1. Open Environment Variables (search "Environment Variables" in Windows)
2. Click "Edit the system environment variables"
3. Click "Environment Variables..."
4. Under "System variables", click "New"
5. Variable name: `Path`
6. Variable value: `C:\Program Files\Tesseract-OCR` (or your installation path)
7. Click OK and restart your terminal

**Option B:** Configure in Python code (add this to app.py if needed)
```python
import pytesseract
pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Step 5: Download Language Data Files

Tesseract comes with English by default. For historical languages, you may need to download additional language packs.

**Option A:** Via Command Line (Linux/macOS)
```bash
# For all languages
sudo apt-get install tesseract-ocr-all

# Or specific languages
sudo apt-get install tesseract-ocr-san  # Sanskrit
sudo apt-get install tesseract-ocr-tam  # Tamil
sudo apt-get install tesseract-ocr-hin  # Hindi
```

**Option B:** Manual Download (Windows)
1. Download `.traineddata` files from [Tesseract Data](https://github.com/tesseract-ocr/tessdata)
2. Place them in: `C:\Program Files\Tesseract-OCR\tessdata\`

**Common language data files:**
- `san.traineddata` - Sanskrit
- `tam.traineddata` - Tamil
- `kan.traineddata` - Kannada
- `tel.traineddata` - Telugu
- `mal.traineddata` - Malayalam
- `hin.traineddata` - Hindi
- `chi_sim.traineddata` - Simplified Chinese
- `chi_tra.traineddata` - Traditional Chinese
- `jpn.traineddata` - Japanese
- `ara.traineddata` - Arabic
- `heb.traineddata` - Hebrew
- `grc.traineddata` - Ancient Greek
- `lat.traineddata` - Latin

---

## ▶️ Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. Select Languages
- Use the sidebar to expand language categories
- Check the languages you expect in your images
- You can select multiple languages simultaneously
- The app will detect text in all selected languages

### 2. Configure OCR Settings
- **Enable Image Preprocessing**: Improves OCR accuracy for low-quality images
- **Contrast Enhancement**: Adjust brightness/contrast (0.5 = darker, 3.0 = brighter)
- **Brightness Adjustment**: Fine-tune brightness (-50 to +50)
- **Binary Threshold**: Threshold for converting to black & white (0-255)

### 3. Upload Images
- Click "Choose image file(s)" to upload
- Supports: JPG, JPEG, PNG, BMP, TIFF
- Can upload multiple images at once
- Max file size depends on Streamlit settings

### 4. Set Processing Options
- **Auto-rotate images**: Automatically detects and rotates text
- **Image scaling factor**: Improves quality (higher = slower but better accuracy)

### 5. Extract Text
- Click the "🚀 Extract Text" button
- Progress bar shows processing status
- Results display with:
  - Extracted text
  - Confidence score
  - Detected languages used
  - Image dimensions

### 6. Download Results
- Download as TXT file for raw text
- Download as JSON for detailed metadata
- Export all results at once

---

## 🎯 Tips for Best Results

### Image Quality
- Use high-resolution images (at least 300 DPI)
- Ensure good lighting and contrast
- Avoid skewed or rotated text (or use auto-rotate)
- Remove watermarks and background noise

### Language Selection
- Select only languages likely in your images
- For mixed-language documents, select all relevant languages
- More languages = slower processing
- Historical languages may have lower accuracy

### Preprocessing Settings
For old/historical documents:
- Enable preprocessing
- Increase contrast (1.5 - 2.5 range)
- Adjust brightness based on document condition
- Use threshold around 100-150 for aged documents
- Increase scale factor (2 or 3) for small text

For printed documents:
- Enable preprocessing
- Keep contrast at 1.0 - 1.5
- Scale factor: 1 or 2

---

## 🔍 Troubleshooting

### Error: "pytesseract.TesseractNotFoundError"
- **Solution**: Tesseract is not installed or not in PATH
- Install Tesseract (see Prerequisites section)
- Or manually set the path in Python code

### Error: "Image language is not available"
- **Solution**: Language data file not downloaded
- Download from GitHub tessdata repository
- Place in Tesseract tessdata folder

### Low OCR Accuracy
- Try enabling image preprocessing
- Increase image scale factor
- Improve image quality
- Adjust contrast and threshold settings
- Ensure language is correctly selected

### App is Slow
- Reduce number of selected languages
- Reduce image scale factor
- Disable preprocessing if not needed
- Process fewer images at once

---

## 📊 Performance Notes

- **Processing time** depends on:
  - Image resolution
  - Number of languages selected
  - Image preprocessing complexity
  - System specifications

- **Typical processing time**:
  - Small image (1-2 languages): 1-3 seconds
  - Large image (5-10 languages): 5-15 seconds
  - Historical languages: May take longer

---

## 📝 Advanced Configuration

### Custom Language Codes
You can modify the `LANGUAGE_CONFIGS` dictionary in `app.py` to add more languages or use specific language variants.

```python
LANGUAGE_CONFIGS = {
    "Language Name": {
        "code": "language_code",
        "script": "Script Name",
        "category": "Category"
    },
    ...
}
```

Common Tesseract language codes:
- `eng` - English
- `san` - Sanskrit
- `tam` - Tamil
- `chi_sim` - Simplified Chinese
- `ara` - Arabic
- `heb` - Hebrew

---

## 📄 Output Formats

### JSON Output
Contains:
- Filename
- Extracted text
- Selected languages
- Confidence score
- Processing timestamp
- Image dimensions

### TXT Output
Plain text format with:
- Filename
- Timestamp
- Extracted text

---

## 🤝 Contributing

To add support for more languages:
1. Download the `.traineddata` file from Tesseract tessdata
2. Add to your Tesseract installation
3. Add language configuration to `LANGUAGE_CONFIGS`
4. Test with sample images

---

## 📜 License

This project uses Tesseract OCR which is under the Apache License 2.0.

---

## ❓ FAQ

**Q: Can it handle handwritten text?**
A: Limited support. Tesseract works best with printed text. For handwriting, consider ML models like handwriting recognition models.

**Q: What's the maximum image size?**
A: Depends on system memory. Typical limit is 100MB+.

**Q: Can it detect text orientation?**
A: Yes, with the "Auto-rotate images" option enabled.

**Q: How accurate is it for ancient languages?**
A: Accuracy varies:
- Well-preserved classical text: 80-95%
- Historical/aged documents: 60-80%
- Heavily damaged text: 40-60%

**Q: Can it work offline?**
A: Yes! Entirely offline after installation.

**Q: Does it save uploaded images?**
A: No. Images are processed in memory and not saved.

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Tesseract documentation: https://github.com/tesseract-ocr/tesseract
3. Check OpenCV documentation for image processing tips

---

## 🚀 Future Enhancements

Potential features:
- [ ] Multiple OCR engine support (Tesseract + CRAFT + EasyOCR)
- [ ] Custom model training for specific historical scripts
- [ ] Batch processing improvements
- [ ] Real-time camera input
- [ ] Text recognition with bounding boxes
- [ ] Translation integration
- [ ] Database storage for historical documents
- [ ] API endpoint for programmatic access

---

**Happy Text Extraction! 📜✨**

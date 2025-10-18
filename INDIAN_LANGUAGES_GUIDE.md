# 🇮🇳 Indian Languages OCR Guide

## Quick Tips for Best Results with Indian Languages

### Your Image Analysis
Your test image contains text in multiple Indian scripts:
- Sanskrit (संस्कृतम्)
- Hindi (हिन्दी)  
- Marathi (मराठी)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)
- Tamil (தமிழ்)
- Malayalam (മലയാളം)
- Bengali (বাংলা)
- Punjabi (ਪੰਜਾਬੀ)
- Gujarati (ગુજરાતી)
- Odia (ଓଡ଼ିଆ)
- Urdu (اردو)

### Problem: Low Accuracy with Too Many Languages

**Issue:** When you select 10+ languages, OCR accuracy drops significantly because:
1. Tesseract tries to match characters against all language models
2. Similar-looking characters in different scripts cause confusion
3. Processing time increases dramatically

### Solution: Use Strategic Language Selection

#### Method 1: Process in Batches (RECOMMENDED)
Instead of selecting all languages at once, process the image multiple times with different language groups:

**Batch 1: Devanagari Script Languages**
```
Select: Hindi + Sanskrit + Marathi
Result: Best for हिन्दी, संस्कृतम्, मराठी text
```

**Batch 2: Dravidian Languages**
```
Select: Tamil + Telugu + Kannada + Malayalam
Result: Best for தமிழ், తెలుగు, ಕನ್ನಡ, മലയാളം text
```

**Batch 3: Other Indian Languages**
```
Select: Bengali + Gujarati + Punjabi + Odia
Result: Best for বাংলা, ગુજરાતી, ਪੰਜਾਬੀ, ଓଡ଼ିଆ text
```

**Batch 4: Arabic Script**
```
Select: Urdu + Arabic
Result: Best for اردو text
```

#### Method 2: Select Only Visible Languages
Look at your image and identify which scripts are actually present, then select only those 3-5 languages.

### Recommended Settings for Your Image

#### Preprocessing Settings:
```
✅ Enable Image Preprocessing: ON
📊 Contrast Enhancement: 1.5
🔆 Brightness Adjustment: 10
🎯 Binary Threshold: 127
📐 Image Scaling Factor: 2x
```

#### Language Selection (Try This First):
```
For Devanagari text (Hindi/Sanskrit/Marathi):
✅ Hindi
✅ Sanskrit (Devanagari)
✅ Marathi (if installed)
✅ English (for mixed text)
```

### Step-by-Step Process for Your Image

**Step 1: Extract Devanagari Text**
1. Uncheck all languages
2. Select: Hindi, Sanskrit, English
3. Enable preprocessing
4. Set contrast to 1.5, scale to 2x
5. Upload image → Extract
6. Save results

**Step 2: Extract Dravidian Text**
1. Uncheck previous languages
2. Select: Tamil, Telugu, Kannada, Malayalam
3. Keep same preprocessing settings
4. Upload same image → Extract
5. Save results

**Step 3: Extract Other Scripts**
1. Select: Bengali, Gujarati, Punjabi
2. Process again
3. Save results

**Step 4: Combine Results**
Manually combine all extracted text from different batches.

### Expected Results

**Before (All 12 languages selected):**
```
ayy ic) (அய
ಇ
ஞ்‌
```
Accuracy: ~10-20%

**After (Strategic selection - Hindi+Sanskrit+English):**
```
संस्कृतम्
हिन्दी
English Wikipedia
```
Accuracy: ~70-85%

**After (Tamil+Telugu+Kannada+Malayalam):**
```
தமிழ்
తెలుగు
ಕನ್ನಡ
മലയാളം
```
Accuracy: ~70-85%

### Advanced Tips

#### 1. Image Quality Matters
- Ensure text is at least 12pt font size
- Image resolution should be 300 DPI or higher
- No skew or rotation
- Good contrast between text and background

#### 2. Preprocessing is Critical
For Indian languages, aggressive preprocessing helps:
```python
Contrast: 1.5 - 2.0
Brightness: +5 to +15
Threshold: 120-140
Scale: 2x or 3x
```

#### 3. Use Script Detection
Instead of language codes, you can use script detection:
```
script/Devanagari - for Hindi, Sanskrit, Marathi
script/Tamil - for Tamil
script/Telugu - for Telugu
script/Kannada - for Kannada
script/Malayalam - for Malayalam
script/Bengali - for Bengali
script/Gujarati - for Gujarati
```

#### 4. Post-Processing
After extraction, you may need to:
- Fix spacing issues manually
- Correct misrecognized characters
- Use spell-check for each language
- Verify special characters (like ् ं ः in Devanagari)

### Testing Your Setup

Try this quick test:
1. Create a simple image with one line of Hindi text: "नमस्ते भारत"
2. Select only: Hindi + English
3. Enable preprocessing
4. Extract text
5. You should get close to 90%+ accuracy

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Getting random characters | Too many languages selected | Select max 3-4 languages |
| Missing diacritics (matras) | Low resolution | Increase scale factor to 3x |
| Wrong script detected | Image quality poor | Increase contrast to 2.0+ |
| Spaces between letters | Character confusion | Enable preprocessing, adjust threshold |
| Empty result | Language data not installed | Run `tesseract --list-langs` to verify |

### Language Verification

Check if languages are installed:
```powershell
tesseract --list-langs
```

Should show:
- ✅ hin (Hindi)
- ✅ san (Sanskrit)
- ✅ tam (Tamil)
- ✅ tel (Telugu)
- ✅ kan (Kannada)
- ✅ mal (Malayalam)
- ✅ ben (Bengali)
- ✅ guj (Gujarati)
- ✅ mar (Marathi)
- ✅ pan (Punjabi)
- ✅ ori (Odia)
- ✅ urd (Urdu)

### Your Specific Image

For the Wikipedia languages image you uploaded:

**Best Approach:**
1. Process 3-4 times with different language groups
2. Each time, select only related scripts
3. Use preprocessing: Contrast 1.5, Scale 2x
4. Combine results manually

**Expected Time:**
- Per batch: 5-10 seconds
- Total for 4 batches: ~1 minute
- Manual combination: 2-3 minutes
- **Total: 3-4 minutes for complete extraction**

### Quick Command Reference

**For Hindi/Sanskrit/Marathi text:**
```
Languages: Hindi, Sanskrit (Devanagari), English
Preprocessing: ON
Contrast: 1.5
Scale: 2x
```

**For Tamil/Telugu/Kannada/Malayalam text:**
```
Languages: Tamil, Telugu, Kannada, Malayalam
Preprocessing: ON
Contrast: 1.5
Scale: 2x
```

**For Bengali/Gujarati/Punjabi/Odia text:**
```
Languages: Bengali, Gujarati, Punjabi, Odia (if installed)
Preprocessing: ON
Contrast: 1.5
Scale: 2x
```

### Alternative Tools

If Tesseract doesn't give good results for your specific case, consider:
1. **Google Cloud Vision API** - Better for mixed scripts
2. **EasyOCR** - Good for Indian languages
3. **PaddleOCR** - Excellent for multilingual
4. **Manual typing** - For critical/small documents

### Summary

✅ **DO:**
- Select 3-5 related languages maximum
- Process image multiple times with different language groups
- Use strong preprocessing for Indian scripts
- Increase scale factor for small text
- Verify language data files are installed

❌ **DON'T:**
- Select 10+ languages at once
- Expect 100% accuracy (aim for 70-85%)
- Skip preprocessing for old/printed documents
- Use low-resolution images

---

**For your specific Wikipedia image, I recommend:**

Try processing it 4 separate times:
1. Hindi + Sanskrit → Save text
2. Tamil + Telugu + Kannada + Malayalam → Save text
3. Bengali + Gujarati + Punjabi → Save text
4. Urdu + Arabic → Save text

Then combine all results!

Good luck! 📜✨

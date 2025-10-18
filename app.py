import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
import io
import os
from pathlib import Path
import json
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Multi-Language Historical Text Extractor",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="auto"  # Auto-collapse on mobile
)

# Custom CSS for better UI and mobile responsiveness
st.markdown("""
    <style>
    /* Main content area */
    .main {
        padding: 1rem;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Language tags */
    .language-tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 0.3rem;
        background-color: #e0e0e0;
        font-size: 0.85rem;
    }
    
    /* Extracted text box */
    .extracted-text-box {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Mobile Responsiveness */
    @media only screen and (max-width: 768px) {
        /* Reduce padding on mobile */
        .main {
            padding: 0.5rem;
        }
        
        /* Stack columns vertically on mobile */
        .stColumn {
            width: 100% !important;
        }
        
        /* Adjust font sizes for mobile */
        h1 {
            font-size: 1.8rem !important;
        }
        
        h2 {
            font-size: 1.4rem !important;
        }
        
        h3 {
            font-size: 1.2rem !important;
        }
        
        /* Make buttons full width on mobile */
        .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
        
        /* Adjust file uploader */
        .stFileUploader {
            width: 100%;
        }
        
        /* Make images responsive */
        img {
            max-width: 100%;
            height: auto !important;
        }
        
        /* Adjust sidebar width on mobile */
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
        
        /* Reduce text box padding on mobile */
        .extracted-text-box {
            padding: 0.75rem;
            font-size: 0.9rem;
        }
        
        /* Reduce language tag size on mobile */
        .language-tag {
            font-size: 0.75rem;
            padding: 0.25rem 0.6rem;
        }
    }
    
    /* Tablet view (768px - 1024px) */
    @media only screen and (min-width: 768px) and (max-width: 1024px) {
        .main {
            padding: 1.5rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
    }
    
    /* Make text selectable and copyable */
    .extracted-text-box {
        user-select: text;
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
    }
    
    /* Improve touch targets for mobile */
    @media (hover: none) and (pointer: coarse) {
        button, a, input, select {
            min-height: 44px;
            min-width: 44px;
        }
    }
    
    /* Optimize scrolling on mobile */
    .main {
        overflow-x: hidden;
    }
    
    /* Better checkbox/radio button styling for mobile */
    [data-testid="stCheckbox"] label {
        padding: 0.5rem 0;
        font-size: 0.95rem;
    }
    
    /* Responsive container for images */
    .image-container {
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Language configuration with historical languages
LANGUAGE_CONFIGS = {
    # Ancient Indian Languages - Indo-Aryan
    "Sanskrit (Devanagari)": {"code": "san", "script": "Devanagari", "category": "Ancient Indian - Indo-Aryan"},
    "Sanskrit (Grantha)": {"code": "san_grnm", "script": "Grantha", "category": "Ancient Indian - Indo-Aryan"},
    "Pali": {"code": "pi", "script": "Multiple", "category": "Ancient Indian - Indo-Aryan"},
    
    # Ancient Indian Languages - Dravidian
    "Tamil (Old & Modern)": {"code": "tam", "script": "Tamil", "category": "Ancient Indian - Dravidian"},
    "Kannada (Old & Modern)": {"code": "kan", "script": "Kannada", "category": "Ancient Indian - Dravidian"},
    "Telugu (Old & Modern)": {"code": "tel", "script": "Telugu", "category": "Ancient Indian - Dravidian"},
    "Malayalam (Old & Modern)": {"code": "mal", "script": "Malayalam", "category": "Ancient Indian - Dravidian"},
    
    # Other Classical Asian
    "Tibetan (Classical)": {"code": "bod", "script": "Tibetan", "category": "Classical Asian"},
    "Classical Chinese": {"code": "chi_sim", "script": "Chinese Simplified", "category": "Classical Asian"},
    "Traditional Chinese": {"code": "chi_tra", "script": "Chinese Traditional", "category": "Classical Asian"},
    "Japanese": {"code": "jpn", "script": "Mixed (Hiragana/Kanji)", "category": "Classical Asian"},
    "Korean": {"code": "kor", "script": "Hangul", "category": "Classical Asian"},
    "Gujarati": {"code": "guj", "script": "Gujarati", "category": "Modern Indian"},
    "Hindi": {"code": "hin", "script": "Devanagari", "category": "Modern Indian"},
    "Bengali": {"code": "ben", "script": "Bengali", "category": "Modern Indian"},
    "Oriya": {"code": "ory", "script": "Oriya", "category": "Modern Indian"},
    
    # Ancient European & Middle-Eastern
    "Latin": {"code": "lat", "script": "Latin", "category": "Ancient European"},
    "Greek (Ancient & Modern)": {"code": "grc", "script": "Greek", "category": "Ancient European"},
    "Hebrew (Biblical & Modern)": {"code": "heb", "script": "Hebrew", "category": "Ancient Middle-Eastern"},
    "Arabic": {"code": "ara", "script": "Arabic", "category": "Ancient Middle-Eastern"},
    "Persian": {"code": "fas", "script": "Persian/Farsi", "category": "Ancient Middle-Eastern"},
    "Syriac": {"code": "syr", "script": "Syriac", "category": "Ancient Middle-Eastern"},
    "Amharic": {"code": "amh", "script": "Ge'ez", "category": "Ancient African"},
    "Tigrinya": {"code": "tir", "script": "Ge'ez", "category": "Ancient African"},
    
    # Slavic & Germanic
    "Russian": {"code": "rus", "script": "Cyrillic", "category": "European"},
    "Ukrainian": {"code": "ukr", "script": "Cyrillic", "category": "European"},
    "Bulgarian": {"code": "bul", "script": "Cyrillic", "category": "European"},
    "Serbian": {"code": "srp", "script": "Cyrillic/Latin", "category": "European"},
    "Polish": {"code": "pol", "script": "Latin Extended", "category": "European"},
    "Czech": {"code": "ces", "script": "Latin Extended", "category": "European"},
    "German": {"code": "deu", "script": "Latin", "category": "European"},
    
    # Other European
    "French": {"code": "fra", "script": "Latin", "category": "European"},
    "Spanish": {"code": "spa", "script": "Latin", "category": "European"},
    "Italian": {"code": "ita", "script": "Latin", "category": "European"},
    "Portuguese": {"code": "por", "script": "Latin", "category": "European"},
    "English": {"code": "eng", "script": "Latin", "category": "European"},
    "Dutch": {"code": "nld", "script": "Latin", "category": "European"},
    "Swedish": {"code": "swe", "script": "Latin", "category": "European"},
    "Danish": {"code": "dan", "script": "Latin", "category": "European"},
    "Norwegian": {"code": "nor", "script": "Latin", "category": "European"},
    "Finnish": {"code": "fin", "script": "Latin", "category": "European"},
    "Hungarian": {"code": "hun", "script": "Latin Extended", "category": "European"},
    "Romanian": {"code": "ron", "script": "Latin", "category": "European"},
    
    # Southeast Asian
    "Thai": {"code": "tha", "script": "Thai", "category": "Southeast Asian"},
    "Vietnamese": {"code": "vie", "script": "Latin Extended", "category": "Southeast Asian"},
    "Khmer": {"code": "khm", "script": "Khmer", "category": "Southeast Asian"},
    "Lao": {"code": "lao", "script": "Lao", "category": "Southeast Asian"},
    "Burmese": {"code": "mya", "script": "Myanmar", "category": "Southeast Asian"},
}

# ============================================================================
# FUNCTION DEFINITIONS
# ============================================================================

def preprocess_image(image, contrast=1.0, brightness=0, threshold_value=127, scale=1):
    """Preprocess image for better OCR results"""
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    # Scale image if needed
    if scale > 1:
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    # Adjust brightness
    if brightness != 0:
        gray = cv2.convertScaleAbs(gray, alpha=1.0, beta=brightness)
    
    # Adjust contrast
    if contrast != 1.0:
        gray = cv2.convertScaleAbs(gray, alpha=contrast, beta=0)
    
    # Apply binary threshold
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    
    # Denoise
    denoised = cv2.medianBlur(thresh, 3)
    
    return denoised


def extract_text_from_images(uploaded_files, languages, preprocess, contrast, brightness, threshold, rotate, scale):
    """Extract text from uploaded images using Tesseract OCR"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_results = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing image {idx + 1}/{len(uploaded_files)}: {uploaded_file.name}")
        
        try:
            # Read image
            image = Image.open(uploaded_file)
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocess if enabled
            if preprocess:
                image_cv = preprocess_image(image_cv, contrast, brightness, threshold, scale)
                image = Image.fromarray(image_cv)
            
            # Get language codes
            lang_codes = [LANGUAGE_CONFIGS[lang]["code"] for lang in languages]
            lang_string = "+".join(lang_codes)
            
            # For better accuracy with many languages, try script detection first
            # Then use specific language models
            config_str = '--psm 6 --oem 3'  # PSM 6 = Uniform block of text, OEM 3 = Default
            
            # Extract text
            extracted_text = pytesseract.image_to_string(image, lang=lang_string, config=config_str)
            
            # Get detailed results
            data = pytesseract.image_to_data(image, lang=lang_string, output_type=pytesseract.Output.DICT)
            
            # Calculate confidence safely
            confidence_scores = []
            if 'confidence' in data and data['confidence']:
                try:
                    confidence_scores = [float(conf) for conf in data['confidence'] if str(conf) != '-1' and float(conf) > 0]
                except (ValueError, TypeError):
                    pass
            avg_confidence = float(np.mean(confidence_scores)) if confidence_scores else 0.0
            
            result = {
                "filename": uploaded_file.name,
                "text": extracted_text,
                "languages": languages,
                "confidence": avg_confidence,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "image_shape": (image_cv.shape[0], image_cv.shape[1]) if preprocess else (image.size[1], image.size[0]),
            }
            
            all_results.append(result)
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    status_text.text("✅ Processing complete!")
    
    return all_results


def display_results(all_results):
    """Display extraction results"""
    if not all_results:
        return
    
    # Display results
    st.divider()
    st.header("📋 Extraction Results")
    
    for result in all_results:
        with st.container(border=True):
            # Mobile-friendly: Stack columns on small screens
            cols = st.columns([2, 1, 1])
            
            with cols[0]:
                st.subheader(f"📄 {result['filename']}")
            
            with cols[1]:
                st.metric("Confidence", f"{result['confidence']:.1f}%")
            
            with cols[2]:
                st.metric("Size", f"{result['image_shape'][0]}x{result['image_shape'][1]}")
            
            st.markdown("**Detected Languages:**")
            for lang in result['languages']:
                st.markdown(f"<span class='language-tag'>{lang}</span>", unsafe_allow_html=True)
            
            st.markdown(f"**Timestamp:** {result['timestamp']}")
            
            st.markdown("---")
            st.markdown("**Extracted Text:**")
            st.markdown(f"""<div class="extracted-text-box">
                {result['text'].replace(chr(10), '<br>')}
            </div>""", unsafe_allow_html=True)
            
            # Copy button with mobile-friendly textarea
            st.text_area(
                "📋 Tap to select and copy text:",
                value=result['text'],
                height=150,
                disabled=False,
                key=f"textarea_{result['filename']}"
            )
            
            # Download options - Mobile friendly: Use expander for download options
            with st.expander("💾 Download Options"):
                col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "📥 Download as TXT",
                    result['text'],
                    file_name=f"{Path(result['filename']).stem}_extracted.txt",
                    mime="text/plain",
                    key=f"download_txt_{result['filename']}"
                )
            
            with col2:
                json_data = json.dumps(result, indent=2, ensure_ascii=False)
                st.download_button(
                    "📥 Download as JSON",
                    json_data,
                    file_name=f"{Path(result['filename']).stem}_result.json",
                    mime="application/json",
                    key=f"download_json_{result['filename']}"
                )
    
    # Export all results
    if all_results:
        st.divider()
        st.subheader("💾 Export All Results")
        
        all_text = "\n\n" + "="*80 + "\n\n".join([
            f"File: {r['filename']}\nLanguages: {', '.join(r['languages'])}\n\n{r['text']}"
            for r in all_results
        ])
        
        st.download_button(
            "📥 Download All Extracted Text",
            all_text,
            file_name="all_extracted_text.txt",
            mime="text/plain"
        )
        
        all_json = json.dumps(all_results, indent=2, ensure_ascii=False)
        st.download_button(
            "📥 Download All Results as JSON",
            all_json,
            file_name="all_results.json",
            mime="application/json"
        )


# ============================================================================
# MAIN UI
# ============================================================================

# Title and description
st.markdown("""
    <div class="header">
        <h1>📜 Multi-Language Historical Text Extractor</h1>
        <p>Extract text from images containing modern and ancient/historical languages</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Language selection
    st.subheader("🌍 Select Languages")
    
    # Group languages by category
    categories = {}
    for lang, config in LANGUAGE_CONFIGS.items():
        cat = config["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(lang)
    
    selected_languages = []
    
    for category in sorted(categories.keys()):
        with st.expander(f"📌 {category}", expanded=(category == "Modern Indian")):
            for lang in categories[category]:
                if st.checkbox(lang, value=(lang == "English")):
                    selected_languages.append(lang)
    
    if not selected_languages:
        st.warning("⚠️ Please select at least one language!")
        selected_languages = ["English"]  # Default
    
    st.divider()
    
    # OCR preprocessing options
    st.subheader("🔧 OCR Preprocessing")
    
    enable_preprocessing = st.checkbox("Enable Image Preprocessing", value=True)
    
    if enable_preprocessing:
        contrast = st.slider("Contrast Enhancement", 0.5, 3.0, 1.0, 0.1)
        brightness = st.slider("Brightness Adjustment", -50, 50, 0, 5)
        threshold_value = st.slider("Binary Threshold", 0, 255, 127, 5)
    else:
        contrast = 1.0
        brightness = 0
        threshold_value = 127
    
    st.divider()
    
    # Display info
    st.subheader("ℹ️ Selected Languages")
    st.info(f"**Total Languages:** {len(selected_languages)}\n\n" + 
            "\n".join([f"• {lang}" for lang in selected_languages[:10]]) +
            (f"\n• ... and {len(selected_languages) - 10} more" if len(selected_languages) > 10 else ""))
    
    # Tip for Indian languages
    if len(selected_languages) > 5:
        st.warning("⚠️ **Tip:** Selecting too many languages can reduce accuracy. For best results with Indian languages, select only 3-5 relevant languages.")

# Main content area - Mobile friendly layout
st.subheader("📤 Upload Images")

uploaded_files = st.file_uploader(
    "Choose image file(s)",
    type=["jpg", "jpeg", "png", "bmp", "tiff"],
    accept_multiple_files=True,
    help="Upload one or more images containing text in various languages"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    
    # Preview uploaded images in a mobile-friendly grid
    if len(uploaded_files) <= 4:
        preview_cols = st.columns(min(len(uploaded_files), 2))
        for idx, file in enumerate(uploaded_files):
            with preview_cols[idx % 2]:
                img = Image.open(file)
                st.image(img, caption=file.name, use_container_width=True)
                file.seek(0)  # Reset file pointer

st.divider()

# Processing options
st.subheader("⚡ Processing Options")

col1, col2 = st.columns([1, 1])

with col1:
    auto_rotate = st.checkbox("Auto-rotate images", value=True)

with col2:
    scale_factor = st.slider("Image scaling", 1, 3, 1)

# Extract button - full width for mobile
if st.button("🚀 Extract Text", type="primary", use_container_width=True):
    if not uploaded_files:
        st.error("❌ Please upload at least one image first!")
    else:
        results = extract_text_from_images(uploaded_files, selected_languages, enable_preprocessing, 
                    contrast, brightness, threshold_value, auto_rotate, scale_factor)
        display_results(results)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; padding: 1rem 0;">
        <small>
            🔤 **Supported Languages:** 50+ including ancient Sanskrit, Pali, Old Tamil, Classical Latin, Ancient Greek, 
            Hebrew, Arabic, and many more historical languages
            <br>
            ⚡ **Powered by:** Tesseract OCR Engine
            <br>
            📜 **Note:** Accuracy depends on image quality, language selection, and preprocessing settings
        </small>
    </div>
""", unsafe_allow_html=True)

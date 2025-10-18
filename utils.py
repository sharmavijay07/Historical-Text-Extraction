"""
Utility functions for the Multi-Language Historical Text Extractor
"""

import cv2
import numpy as np
from PIL import Image
import pytesseract
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path


class ImageProcessor:
    """Handle image preprocessing and enhancement"""
    
    @staticmethod
    def grayscale(image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale"""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image
    
    @staticmethod
    def scale_image(image: np.ndarray, scale_factor: float) -> np.ndarray:
        """Scale image by factor"""
        if scale_factor != 1:
            return cv2.resize(
                image,
                None,
                fx=scale_factor,
                fy=scale_factor,
                interpolation=cv2.INTER_CUBIC
            )
        return image
    
    @staticmethod
    def adjust_brightness(image: np.ndarray, brightness: int) -> np.ndarray:
        """Adjust image brightness"""
        if brightness == 0:
            return image
        return cv2.convertScaleAbs(image, alpha=1.0, beta=brightness)
    
    @staticmethod
    def adjust_contrast(image: np.ndarray, contrast: float) -> np.ndarray:
        """Adjust image contrast"""
        if contrast == 1.0:
            return image
        return cv2.convertScaleAbs(image, alpha=contrast, beta=0)
    
    @staticmethod
    def binary_threshold(image: np.ndarray, threshold: int) -> np.ndarray:
        """Apply binary threshold"""
        _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        return binary
    
    @staticmethod
    def denoise(image: np.ndarray, strength: int = 3) -> np.ndarray:
        """Denoise image using median blur"""
        return cv2.medianBlur(image, strength)
    
    @staticmethod
    def auto_rotate(image: np.ndarray) -> np.ndarray:
        """Auto-rotate image based on text orientation"""
        # Placeholder for auto-rotation logic
        # Can be implemented using OpenCV or specialized libraries
        return image
    
    @staticmethod
    def full_preprocessing(
        image: np.ndarray,
        contrast: float = 1.0,
        brightness: int = 0,
        threshold: int = 127,
        scale: float = 1.0,
        denoise_strength: int = 3
    ) -> np.ndarray:
        """Apply full preprocessing pipeline"""
        # Convert to grayscale
        gray = ImageProcessor.grayscale(image)
        
        # Scale
        gray = ImageProcessor.scale_image(gray, scale)
        
        # Adjust brightness
        gray = ImageProcessor.adjust_brightness(gray, brightness)
        
        # Adjust contrast
        gray = ImageProcessor.adjust_contrast(gray, contrast)
        
        # Binary threshold
        gray = ImageProcessor.binary_threshold(gray, threshold)
        
        # Denoise
        gray = ImageProcessor.denoise(gray, denoise_strength)
        
        return gray


class TextExtractor:
    """Handle text extraction using Tesseract OCR"""
    
    @staticmethod
    def extract_text(
        image: Image.Image,
        languages: List[str],
        config: str = ""
    ) -> str:
        """Extract text from image"""
        return pytesseract.image_to_string(image, lang=languages, config=config)
    
    @staticmethod
    def extract_text_with_confidence(
        image: Image.Image,
        languages: List[str]
    ) -> Dict:
        """Extract text with confidence scores"""
        data = pytesseract.image_to_data(
            image,
            lang=languages,
            output_type=pytesseract.Output.DICT
        )
        return data
    
    @staticmethod
    def get_average_confidence(data: Dict) -> float:
        """Calculate average confidence from OCR data"""
        confidences = [int(conf) for conf in data['confidence'] if int(conf) > 0]
        if confidences:
            return np.mean(confidences)
        return 0.0
    
    @staticmethod
    def extract_text_with_boxes(
        image: Image.Image,
        languages: List[str]
    ) -> Tuple[str, List[Dict]]:
        """Extract text with bounding boxes"""
        data = pytesseract.image_to_data(
            image,
            lang=languages,
            output_type=pytesseract.Output.DICT
        )
        
        text = pytesseract.image_to_string(image, lang=languages)
        
        boxes = []
        for i, word in enumerate(data['text']):
            if word.strip():
                boxes.append({
                    'text': word,
                    'confidence': int(data['confidence'][i]),
                    'x': int(data['left'][i]),
                    'y': int(data['top'][i]),
                    'width': int(data['width'][i]),
                    'height': int(data['height'][i])
                })
        
        return text, boxes


class LanguageConfig:
    """Manage language configurations"""
    
    LANGUAGE_MAP = {
        # Ancient Indian - Indo-Aryan
        "Sanskrit (Devanagari)": "san",
        "Sanskrit (Grantha)": "san_grnm",
        "Pali": "pi",
        
        # Ancient Indian - Dravidian
        "Tamil": "tam",
        "Kannada": "kan",
        "Telugu": "tel",
        "Malayalam": "mal",
        
        # Modern Indian
        "Hindi": "hin",
        "Bengali": "ben",
        "Gujarati": "guj",
        "Oriya": "ory",
        
        # Classical Asian
        "Tibetan": "bod",
        "Chinese (Simplified)": "chi_sim",
        "Chinese (Traditional)": "chi_tra",
        "Japanese": "jpn",
        "Korean": "kor",
        
        # European
        "English": "eng",
        "French": "fra",
        "German": "deu",
        "Spanish": "spa",
        "Italian": "ita",
        "Portuguese": "por",
        "Russian": "rus",
        "Polish": "pol",
        "Czech": "ces",
        "Dutch": "nld",
        "Swedish": "swe",
        "Danish": "dan",
        "Norwegian": "nor",
        "Finnish": "fin",
        "Hungarian": "hun",
        "Romanian": "ron",
        
        # Ancient European
        "Latin": "lat",
        "Greek (Ancient)": "grc",
        "Greek (Modern)": "ell",
        
        # Middle Eastern
        "Hebrew": "heb",
        "Arabic": "ara",
        "Persian": "fas",
        "Syriac": "syr",
        
        # African
        "Amharic": "amh",
        "Tigrinya": "tir",
        
        # Southeast Asian
        "Thai": "tha",
        "Vietnamese": "vie",
        "Khmer": "khm",
        "Lao": "lao",
        "Burmese": "mya",
    }
    
    @staticmethod
    def get_language_code(language_name: str) -> Optional[str]:
        """Get Tesseract language code"""
        return LanguageConfig.LANGUAGE_MAP.get(language_name)
    
    @staticmethod
    def get_language_codes(language_names: List[str]) -> List[str]:
        """Get multiple language codes"""
        codes = []
        for name in language_names:
            code = LanguageConfig.get_language_code(name)
            if code:
                codes.append(code)
        return codes
    
    @staticmethod
    def get_language_string(language_names: List[str]) -> str:
        """Get Tesseract-compatible language string"""
        codes = LanguageConfig.get_language_codes(language_names)
        return "+".join(codes) if codes else "eng"


class ResultFormatter:
    """Format and export OCR results"""
    
    @staticmethod
    def to_dict(
        filename: str,
        text: str,
        languages: List[str],
        confidence: float,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Format result as dictionary"""
        result = {
            "filename": filename,
            "text": text,
            "languages": languages,
            "confidence": confidence,
            "metadata": metadata or {}
        }
        return result
    
    @staticmethod
    def to_json(results: List[Dict], indent: int = 2) -> str:
        """Format results as JSON"""
        return json.dumps(results, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def to_text(results: List[Dict]) -> str:
        """Format results as plain text"""
        output = []
        for result in results:
            output.append(f"File: {result['filename']}")
            output.append(f"Languages: {', '.join(result['languages'])}")
            output.append(f"Confidence: {result['confidence']:.1f}%")
            output.append("-" * 80)
            output.append(result['text'])
            output.append("\n\n")
        return "\n".join(output)
    
    @staticmethod
    def to_csv(results: List[Dict]) -> str:
        """Format results as CSV"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["Filename", "Languages", "Confidence", "Text"])
        for result in results:
            writer.writerow([
                result['filename'],
                "; ".join(result['languages']),
                f"{result['confidence']:.1f}",
                result['text'].replace("\n", " ")
            ])
        
        return output.getvalue()


class LanguageDetector:
    """Detect languages in extracted text"""
    
    # Simple keyword detection for historical languages
    LANGUAGE_KEYWORDS = {
        "Sanskrit": ["ॐ", "ः", "ं"],  # Sanskrit specific characters
        "Tamil": ["ற", "ள", "ன"],  # Tamil specific characters
        "Kannada": ["ಹ", "ಖ", "ಗ"],  # Kannada specific characters
        "Telugu": ["ఆ", "ఇ", "ఉ"],  # Telugu specific characters
        "Malayalam": ["ഹ", "ഖ", "ഗ"],  # Malayalam specific characters
        "Greek": ["α", "β", "γ"],  # Greek characters
        "Hebrew": ["א", "ב", "ג"],  # Hebrew characters
        "Arabic": ["ا", "ب", "ت"],  # Arabic characters
        "Cyrillic": ["а", "б", "в"],  # Russian/Cyrillic
        "Chinese": ["中", "国", "文"],  # Chinese characters
    }
    
    @staticmethod
    def detect_potential_languages(text: str) -> List[str]:
        """Detect potential languages in text based on character analysis"""
        detected = []
        for lang, keywords in LanguageDetector.LANGUAGE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    detected.append(lang)
                    break
        return list(set(detected)) if detected else ["Unknown"]


# Example usage functions

def process_image_simple(
    image_path: str,
    languages: List[str],
    enable_preprocessing: bool = True
) -> str:
    """Simple function to process image and extract text"""
    image = Image.open(image_path)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    if enable_preprocessing:
        image_cv = ImageProcessor.full_preprocessing(image_cv)
        image = Image.fromarray(image_cv)
    
    lang_string = LanguageConfig.get_language_string(languages)
    text = TextExtractor.extract_text(image, lang_string)
    
    return text


def batch_process_images(
    image_paths: List[str],
    languages: List[str],
    enable_preprocessing: bool = True
) -> List[Dict]:
    """Process multiple images and return results"""
    results = []
    lang_string = LanguageConfig.get_language_string(languages)
    
    for image_path in image_paths:
        try:
            image = Image.open(image_path)
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            if enable_preprocessing:
                image_cv = ImageProcessor.full_preprocessing(image_cv)
                image = Image.fromarray(image_cv)
            
            text = TextExtractor.extract_text(image, lang_string)
            data = TextExtractor.extract_text_with_confidence(image, lang_string)
            confidence = TextExtractor.get_average_confidence(data)
            
            result = ResultFormatter.to_dict(
                filename=Path(image_path).name,
                text=text,
                languages=languages,
                confidence=confidence
            )
            results.append(result)
        
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
    
    return results

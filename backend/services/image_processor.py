"""
Image processing service - Validates and prepares images for analysis
"""

import logging
import hashlib
from typing import Tuple
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

MIN_WIDTH = 200
MIN_HEIGHT = 200
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_FORMATS = ('PNG', 'JPEG')


class ImageProcessor:
    """Handles image validation and processing"""

    @staticmethod
    def validate_image(image_bytes: bytes) -> Tuple[bool, str]:
        """
        Validate image file.
        
        Checks:
        - File size <= 5MB
        - Format is PNG or JPEG
        - Dimensions >= 200x200
        
        Returns: (is_valid, error_message)
        """
        # Check file size
        if len(image_bytes) > MAX_FILE_SIZE:
            return False, f"Image too large: {len(image_bytes) / 1024 / 1024:.1f}MB (max 5MB)"

        try:
            # Verify image format
            image = Image.open(BytesIO(image_bytes))
            
            # Check format
            if image.format not in ALLOWED_FORMATS:
                return False, f"Invalid format: {image.format}. Only PNG and JPEG allowed."
            
            # Check dimensions
            width, height = image.size
            if width < MIN_WIDTH or height < MIN_HEIGHT:
                return False, f"Image too small: {width}x{height}px (min 200x200px)"
            
            return True, ""
        
        except Exception as e:
            logger.error(f"Image validation error: {e}")
            return False, f"Invalid image file: {str(e)}"

    @staticmethod
    def get_image_hash(image_bytes: bytes) -> str:
        """
        Generate SHA256 hash of image for caching.
        
        PERF-04: Image hash cache (48h TTL)
        """
        return hashlib.sha256(image_bytes).hexdigest()

    @staticmethod
    def get_image_dimensions(image_bytes: bytes) -> Tuple[int, int]:
        """Get image width and height"""
        try:
            image = Image.open(BytesIO(image_bytes))
            return image.size
        except Exception as e:
            logger.error(f"Error reading image dimensions: {e}")
            return 0, 0

    @staticmethod
    def convert_to_base64(image_bytes: bytes) -> str:
        """Convert image bytes to base64 for Claude Vision API"""
        import base64
        return base64.standard_b64encode(image_bytes).decode('utf-8')

"""
Preprocessing service based on model_references/funtional_scripts/01_data_preparation/advanced_preprocessor.py

This module provides image preprocessing functions:
- Crop by bounding box
- Extract mask
- Remove background
- Resize image
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List
import base64
from io import BytesIO
from PIL import Image


def decode_base64_image(image_data: str) -> np.ndarray:
    """Decode base64 image string to numpy array"""
    image_bytes = base64.b64decode(image_data.split(',')[1] if ',' in image_data else image_data)
    image = Image.open(BytesIO(image_bytes))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def encode_image_to_base64(image: np.ndarray) -> str:
    """Encode numpy array to base64 string"""
    is_success, buffer = cv2.imencode(".png", image)
    if not is_success:
        raise ValueError("Failed to encode image")
    return base64.b64encode(buffer).decode('utf-8')


def crop_by_box(image: np.ndarray, box: Tuple[int, int, int, int], padding: int = 0) -> np.ndarray:
    """
    Crop image by bounding box with optional padding
    
    Args:
        image: Input image (H, W, 3)
        box: Bounding box coordinates (x1, y1, x2, y2)
        padding: Padding pixels around the box
        
    Returns:
        Cropped image
    """
    x1, y1, x2, y2 = map(int, box)
    height, width = image.shape[:2]
    
    # Apply padding
    x1_pad = max(0, x1 - padding)
    y1_pad = max(0, y1 - padding)
    x2_pad = min(width, x2 + padding)
    y2_pad = min(height, y2 + padding)
    
    if y1_pad >= y2_pad or x1_pad >= x2_pad:
        raise ValueError(f"Invalid crop dimensions: ({x1_pad}, {y1_pad}, {x2_pad}, {y2_pad})")
    
    return image[y1_pad:y2_pad, x1_pad:x2_pad].copy()


def create_mask_from_polygon(image_shape: Tuple[int, int], polygon_coords: List[float]) -> np.ndarray:
    """
    Create binary mask from normalized polygon coordinates
    
    Args:
        image_shape: (height, width)
        polygon_coords: Normalized coordinates [x1, y1, x2, y2, ...]
        
    Returns:
        Binary mask (H, W) with 255 for mask area, 0 for background
    """
    height, width = image_shape
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # Convert normalized coords to absolute pixel coords
    points = []
    for i in range(0, len(polygon_coords), 2):
        if i + 1 < len(polygon_coords):
            x = int(polygon_coords[i] * width)
            y = int(polygon_coords[i + 1] * height)
            points.append([x, y])
    
    if points:
        pts_array = np.array(points, dtype=np.int32)
        cv2.fillPoly(mask, [pts_array], 255)
    
    return mask


def extract_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Apply binary mask to image (keep only masked area)
    
    Args:
        image: Input image (H, W, 3)
        mask: Binary mask (H, W) with 255 for object, 0 for background
        
    Returns:
        Masked image
    """
    if mask.shape[:2] != image.shape[:2]:
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    
    # Create 3-channel mask
    mask_3ch = cv2.merge([mask, mask, mask])
    return cv2.bitwise_and(image, mask_3ch)


def remove_background(image: np.ndarray, mask: np.ndarray, bg_mode: str = "black") -> np.ndarray:
    """
    Remove background from image using mask
    
    Args:
        image: Input image (H, W, 3)
        mask: Binary mask (H, W)
        bg_mode: Background mode - "black", "white", "gray", "transparent", "blur", "mean"
        
    Returns:
        Image with background removed (RGB or RGBA)
    """
    if mask.shape[:2] != image.shape[:2]:
        mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    
    mask_binary = (mask > 0).astype(np.uint8)
    
    if bg_mode == "transparent":
        # Create RGBA image
        rgba = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
        rgba[:, :, :3] = image
        rgba[:, :, 3] = mask_binary * 255
        return rgba
    
    elif bg_mode == "blur":
        # Blur the background
        blurred = cv2.GaussianBlur(image, (21, 21), 0)
        result = image.copy()
        inverse_mask = (mask_binary == 0)
        result[inverse_mask] = blurred[inverse_mask]
        return result
    
    else:
        # Solid color background
        result = image.copy()
        inverse_mask = (mask_binary == 0)
        
        if bg_mode == "black":
            bg_color = [0, 0, 0]
        elif bg_mode == "white":
            bg_color = [255, 255, 255]
        elif bg_mode == "gray":
            bg_color = [128, 128, 128]
        elif bg_mode == "mean":
            masked_pixels = image[mask_binary == 1]
            bg_color = np.mean(masked_pixels, axis=0).astype(int).tolist() if len(masked_pixels) > 0 else [128, 128, 128]
        else:
            bg_color = [0, 0, 0]
        
        result[inverse_mask] = bg_color
        return result


def resize_image(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    """
    Resize image to target size
    
    Args:
        image: Input image
        target_size: (width, height)
        
    Returns:
        Resized image
    """
    return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)


def preprocess_image(
    image: np.ndarray,
    box: Optional[Tuple[int, int, int, int]] = None,
    mask: Optional[np.ndarray] = None,
    bg_mode: str = "black",
    target_size: Tuple[int, int] = (640, 480),
    padding: int = 0
) -> np.ndarray:
    """
    Complete preprocessing pipeline
    
    Args:
        image: Input image
        box: Bounding box (x1, y1, x2, y2), optional
        mask: Binary mask, optional
        bg_mode: Background mode
        target_size: Output size (width, height)
        padding: Padding around box
        
    Returns:
        Preprocessed image
    """
    result = image.copy()
    
    # Apply mask if provided
    if mask is not None:
        result = remove_background(result, mask, bg_mode)
    
    # Crop by box if provided
    if box is not None:
        result = crop_by_box(result, box, padding)
    
    # Resize
    result = resize_image(result, target_size)
    
    return result

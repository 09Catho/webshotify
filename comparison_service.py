"""
Screenshot Comparison Service
Handles visual regression testing and screenshot diff
"""

from PIL import Image, ImageChops, ImageDraw, ImageFont
from pathlib import Path
import hashlib
from datetime import datetime


class ComparisonService:
    """Service for comparing screenshots and detecting visual differences"""
    
    def __init__(self):
        self.comparisons_dir = Path('comparisons')
        self.comparisons_dir.mkdir(exist_ok=True)
    
    def compare_images(self, image1_path, image2_path, threshold=0.1, 
                      highlight_color=(255, 0, 0), create_diff_image=True):
        """
        Compare two images and detect differences
        
        Args:
            image1_path (str): Path to first image (baseline)
            image2_path (str): Path to second image (current)
            threshold (float): Difference threshold (0.0 - 1.0)
            highlight_color (tuple): RGB color for highlighting differences
            create_diff_image (bool): Create a visual diff image
        
        Returns:
            dict: Comparison results with diff percentage and diff image path
        """
        try:
            # Load images
            img1 = Image.open(image1_path).convert('RGB')
            img2 = Image.open(image2_path).convert('RGB')
            
            # Resize images to match if needed
            if img1.size != img2.size:
                # Resize img2 to match img1
                img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
            
            # Calculate difference
            diff_img = ImageChops.difference(img1, img2)
            
            # Calculate diff percentage
            diff_pixels = 0
            total_pixels = img1.width * img1.height
            
            for pixel in diff_img.getdata():
                if sum(pixel) > 30:  # Threshold for considering a pixel different
                    diff_pixels += 1
            
            diff_percentage = (diff_pixels / total_pixels) * 100
            
            # Determine if test passed
            passed = diff_percentage <= (threshold * 100)
            
            result = {
                'passed': passed,
                'diff_percentage': round(diff_percentage, 2),
                'threshold': threshold * 100,
                'total_pixels': total_pixels,
                'different_pixels': diff_pixels,
                'image1_size': img1.size,
                'image2_size': img2.size
            }
            
            # Create diff visualization if requested
            if create_diff_image and diff_percentage > 0:
                diff_image_path = self._create_diff_visualization(
                    img1, img2, diff_img, highlight_color, diff_percentage
                )
                result['diff_image'] = str(diff_image_path)
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to compare images: {str(e)}")
    
    def _create_diff_visualization(self, img1, img2, diff_img, highlight_color, diff_percentage):
        """
        Create a visual diff image with side-by-side comparison
        
        Args:
            img1: PIL Image (baseline)
            img2: PIL Image (current)
            diff_img: PIL Image (difference)
            highlight_color: RGB tuple for highlights
            diff_percentage: Percentage difference
        
        Returns:
            str: Path to diff visualization image
        """
        # Create side-by-side comparison
        width, height = img1.size
        
        # Create canvas for 3 images side by side
        comparison = Image.new('RGB', (width * 3 + 60, height + 80), 'white')
        
        # Add images
        comparison.paste(img1, (10, 60))
        comparison.paste(img2, (width + 30, 60))
        
        # Create highlighted diff
        diff_highlighted = img2.copy()
        diff_pixels = diff_img.load()
        highlighted_pixels = diff_highlighted.load()
        
        for y in range(height):
            for x in range(width):
                if sum(diff_pixels[x, y]) > 30:
                    highlighted_pixels[x, y] = highlight_color
        
        comparison.paste(diff_highlighted, (width * 2 + 50, 60))
        
        # Add labels
        draw = ImageDraw.Draw(comparison)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), "Baseline", fill='black', font=font)
        draw.text((width + 30, 10), "Current", fill='black', font=font)
        draw.text((width * 2 + 50, 10), f"Diff: {diff_percentage:.2f}%", fill='red', font=font)
        
        # Add pass/fail indicator
        status_text = "✓ PASSED" if diff_percentage < 2.0 else "✗ FAILED"
        status_color = 'green' if diff_percentage < 2.0 else 'red'
        draw.text((10, height + 65), status_text, fill=status_color, font=font)
        
        # Save comparison image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'diff_{timestamp}.png'
        filepath = self.comparisons_dir / filename
        comparison.save(filepath)
        
        return filepath
    
    def compare_by_url(self, url, baseline_path, screenshot_service, **capture_params):
        """
        Capture a new screenshot and compare with baseline
        
        Args:
            url (str): URL to capture
            baseline_path (str): Path to baseline screenshot
            screenshot_service: ScreenshotService instance
            **capture_params: Parameters for screenshot capture
        
        Returns:
            dict: Comparison results
        """
        try:
            # Capture new screenshot
            current_screenshot = screenshot_service.capture_screenshot(url, **capture_params)
            
            # Compare with baseline
            result = self.compare_images(baseline_path, current_screenshot)
            result['current_screenshot'] = current_screenshot
            result['baseline_screenshot'] = baseline_path
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to compare by URL: {str(e)}")
    
    def create_baseline(self, screenshot_path, baseline_name=None):
        """
        Save a screenshot as a baseline for future comparisons
        
        Args:
            screenshot_path (str): Path to screenshot
            baseline_name (str): Name for the baseline
        
        Returns:
            str: Path to saved baseline
        """
        baselines_dir = Path('baselines')
        baselines_dir.mkdir(exist_ok=True)
        
        if not baseline_name:
            baseline_name = hashlib.md5(screenshot_path.encode()).hexdigest()
        
        baseline_path = baselines_dir / f"{baseline_name}.png"
        
        # Copy screenshot to baselines
        import shutil
        shutil.copy2(screenshot_path, baseline_path)
        
        return str(baseline_path)
    
    def get_baseline(self, baseline_name):
        """
        Get path to a saved baseline
        
        Args:
            baseline_name (str): Name of the baseline
        
        Returns:
            str or None: Path to baseline if exists
        """
        baselines_dir = Path('baselines')
        baseline_path = baselines_dir / f"{baseline_name}.png"
        
        if baseline_path.exists():
            return str(baseline_path)
        return None

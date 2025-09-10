"""
Screenshot utility for test evidence and debugging.
Provides enhanced screenshot functionality with annotations and metadata.
"""

import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from selenium.webdriver.common.by import By


class ScreenshotHelper:
    """
    Enhanced screenshot functionality for test automation.
    Supports annotated screenshots, element highlighting, and organized storage.
    """
    
    def __init__(self, driver, logger, base_path="screenshots"):
        """
        Initialize screenshot helper.
        
        Args:
            driver: WebDriver instance
            logger: Logger instance
            base_path (str): Base directory for screenshots
        """
        self.driver = driver
        self.logger = logger
        self.base_path = base_path
        
        # Create screenshots directory
        os.makedirs(base_path, exist_ok=True)
        
    def take_screenshot(self, filename=None, description=""):
        """
        Take a basic screenshot with timestamp.
        
        Args:
            filename (str): Custom filename (optional)
            description (str): Description for the screenshot
            
        Returns:
            str: Path to the saved screenshot
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"screenshot_{timestamp}.png"
            
        filepath = os.path.join(self.base_path, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            if description:
                self.logger.info(f"Screenshot description: {description}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return None
            
    def take_element_screenshot(self, element, filename=None, description=""):
        """
        Take a screenshot of a specific element.
        
        Args:
            element: WebElement to capture
            filename (str): Custom filename (optional)
            description (str): Description for the screenshot
            
        Returns:
            str: Path to the saved screenshot
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"element_screenshot_{timestamp}.png"
            
        filepath = os.path.join(self.base_path, filename)
        
        try:
            element.screenshot(filepath)
            self.logger.info(f"Element screenshot saved: {filepath}")
            if description:
                self.logger.info(f"Element screenshot description: {description}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to take element screenshot: {str(e)}")
            return None
            
    def take_annotated_screenshot(self, filename=None, annotations=None, description=""):
        """
        Take a screenshot with annotations highlighting specific elements.
        
        Args:
            filename (str): Custom filename (optional)
            annotations (list): List of annotation dictionaries with 'element', 'color', 'text'
            description (str): Description for the screenshot
            
        Returns:
            str: Path to the saved annotated screenshot
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"annotated_screenshot_{timestamp}.png"
            
        filepath = os.path.join(self.base_path, filename)
        
        try:
            # Take base screenshot
            temp_path = os.path.join(self.base_path, "temp_screenshot.png")
            self.driver.save_screenshot(temp_path)
            
            # Open image for annotation
            image = Image.open(temp_path)
            draw = ImageDraw.Draw(image)
            
            if annotations:
                for annotation in annotations:
                    try:
                        element = annotation.get('element')
                        color = annotation.get('color', 'red')
                        text = annotation.get('text', '')
                        
                        if element:
                            # Get element location and size
                            location = element.location
                            size = element.size
                            
                            # Draw rectangle around element
                            x1, y1 = location['x'], location['y']
                            x2, y2 = x1 + size['width'], y1 + size['height']
                            
                            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
                            
                            # Add text annotation
                            if text:
                                # Try to use a default font, fallback to default if not available
                                try:
                                    font = ImageFont.truetype("arial.ttf", 16)
                                except:
                                    font = ImageFont.load_default()
                                    
                                draw.text((x1, y1 - 20), text, fill=color, font=font)
                                
                    except Exception as e:
                        self.logger.warning(f"Failed to annotate element: {str(e)}")
            
            # Save annotated image
            image.save(filepath)
            
            # Cleanup temp file
            os.remove(temp_path)
            
            self.logger.info(f"Annotated screenshot saved: {filepath}")
            if description:
                self.logger.info(f"Annotated screenshot description: {description}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to take annotated screenshot: {str(e)}")
            return None
            
    def take_comparison_screenshot(self, before_element, after_element, filename=None):
        """
        Take side-by-side comparison screenshots of elements.
        
        Args:
            before_element: Element in before state
            after_element: Element in after state  
            filename (str): Custom filename (optional)
            
        Returns:
            str: Path to the saved comparison screenshot
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"comparison_screenshot_{timestamp}.png"
            
        filepath = os.path.join(self.base_path, filename)
        
        try:
            # Take before screenshot
            before_path = os.path.join(self.base_path, "temp_before.png")
            before_element.screenshot(before_path)
            
            # Take after screenshot
            after_path = os.path.join(self.base_path, "temp_after.png")
            after_element.screenshot(after_path)
            
            # Create side-by-side comparison
            before_img = Image.open(before_path)
            after_img = Image.open(after_path)
            
            # Create new image with combined width
            total_width = before_img.width + after_img.width + 10  # 10px separator
            max_height = max(before_img.height, after_img.height)
            
            comparison_img = Image.new('RGB', (total_width, max_height), 'white')
            comparison_img.paste(before_img, (0, 0))
            comparison_img.paste(after_img, (before_img.width + 10, 0))
            
            # Add labels
            draw = ImageDraw.Draw(comparison_img)
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
                
            draw.text((10, 10), "BEFORE", fill="red", font=font)
            draw.text((before_img.width + 20, 10), "AFTER", fill="green", font=font)
            
            comparison_img.save(filepath)
            
            # Cleanup temp files
            os.remove(before_path)
            os.remove(after_path)
            
            self.logger.info(f"Comparison screenshot saved: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Failed to take comparison screenshot: {str(e)}")
            return None
            
    def capture_page_state(self, test_name, step_description=""):
        """
        Capture comprehensive page state for debugging.
        
        Args:
            test_name (str): Name of the test
            step_description (str): Description of the current step
            
        Returns:
            dict: Dictionary containing screenshot paths and metadata
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_test_name = test_name.replace(" ", "_").replace(":", "")
        safe_step = step_description.replace(" ", "_").replace(":", "")
        
        results = {
            'timestamp': timestamp,
            'test_name': test_name,
            'step': step_description,
            'screenshots': {}
        }
        
        # Full page screenshot
        full_page_filename = f"{safe_test_name}_{safe_step}_full_page_{timestamp}.png"
        full_path = self.take_screenshot(full_page_filename, f"Full page - {step_description}")
        results['screenshots']['full_page'] = full_path
        
        # Browser info
        results['browser_info'] = {
            'url': self.driver.current_url,
            'title': self.driver.title,
            'window_size': self.driver.get_window_size()
        }
        
        self.logger.info(f"Page state captured for test: {test_name}, step: {step_description}")
        return results
        
    def create_test_evidence_folder(self, test_name):
        """
        Create organized folder structure for test evidence.
        
        Args:
            test_name (str): Name of the test
            
        Returns:
            str: Path to the test evidence folder
        """
        safe_test_name = test_name.replace(" ", "_").replace(":", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{safe_test_name}_{timestamp}"
        folder_path = os.path.join(self.base_path, folder_name)
        
        os.makedirs(folder_path, exist_ok=True)
        self.logger.info(f"Test evidence folder created: {folder_path}")
        
        return folder_path
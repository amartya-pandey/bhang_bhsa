#!/usr/bin/env python3
"""
Image Text Extraction Script for bhang_bhsa Repository

This script extracts text from images in the repository using OCR (Optical Character Recognition).
It supports processing individual images or batch processing all images in the repository.

Requirements:
- pytesseract: Python wrapper for Tesseract OCR engine
- Pillow: Python Imaging Library for image processing
- Tesseract OCR engine must be installed on the system

Usage:
    python3 extract_text.py [options]
    
Examples:
    python3 extract_text.py --help
    python3 extract_text.py --single path/to/image.jpg
    python3 extract_text.py --batch --output-dir ./extracted_text/
    python3 extract_text.py --batch --format json --output-file results.json
"""

import argparse
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import pytesseract
    from PIL import Image
except ImportError as e:
    logger.error(f"Required dependencies not installed: {e}")
    logger.error("Please install dependencies with: pip install pytesseract Pillow")
    sys.exit(1)


class ImageTextExtractor:
    """Extract text from images using OCR technology."""
    
    def __init__(self, tesseract_config: str = '--oem 3 --psm 6'):
        """
        Initialize the text extractor.
        
        Args:
            tesseract_config: Tesseract configuration string
        """
        self.tesseract_config = tesseract_config
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif'}
        
    def extract_text_from_image(self, image_path: Union[str, Path]) -> Dict[str, Union[str, bool]]:
        """
        Extract text from a single image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        image_path = Path(image_path)
        result = {
            'file_path': str(image_path),
            'file_name': image_path.name,
            'success': False,
            'text': '',
            'error': None
        }
        
        try:
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            if image_path.suffix.lower() not in self.supported_formats:
                raise ValueError(f"Unsupported image format: {image_path.suffix}")
            
            # Open and process image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Extract text using Tesseract
                extracted_text = pytesseract.image_to_string(img, config=self.tesseract_config)
                
                result.update({
                    'success': True,
                    'text': extracted_text.strip(),
                    'image_size': img.size,
                    'image_mode': img.mode
                })
                
                logger.info(f"Successfully extracted text from {image_path.name}")
                
        except Exception as e:
            error_msg = f"Error processing {image_path.name}: {str(e)}"
            logger.error(error_msg)
            result['error'] = error_msg
            
        return result
    
    def find_images_in_directory(self, directory: Union[str, Path], recursive: bool = True) -> List[Path]:
        """
        Find all image files in a directory.
        
        Args:
            directory: Directory path to search
            recursive: Whether to search subdirectories
            
        Returns:
            List of image file paths
        """
        directory = Path(directory)
        pattern = "**/*" if recursive else "*"
        
        image_files = []
        for suffix in self.supported_formats:
            image_files.extend(directory.glob(f"{pattern}{suffix}"))
            image_files.extend(directory.glob(f"{pattern}{suffix.upper()}"))
            
        return sorted(image_files)
    
    def batch_extract_text(self, source_path: Union[str, Path]) -> List[Dict[str, Union[str, bool]]]:
        """
        Extract text from multiple images in a directory.
        
        Args:
            source_path: Directory containing images
            
        Returns:
            List of results for each image
        """
        source_path = Path(source_path)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source path not found: {source_path}")
            
        if source_path.is_file():
            # Single file processing
            return [self.extract_text_from_image(source_path)]
        
        # Directory processing
        image_files = self.find_images_in_directory(source_path)
        
        if not image_files:
            logger.warning(f"No image files found in {source_path}")
            return []
            
        logger.info(f"Found {len(image_files)} image files to process")
        
        results = []
        for i, image_file in enumerate(image_files, 1):
            logger.info(f"Processing {i}/{len(image_files)}: {image_file.name}")
            result = self.extract_text_from_image(image_file)
            results.append(result)
            
        return results


def save_results(results: List[Dict], output_format: str, output_path: Optional[Path] = None):
    """
    Save extraction results in the specified format.
    
    Args:
        results: List of extraction results
        output_format: Output format ('text', 'json', or 'console')
        output_path: Output file or directory path
    """
    if output_format == 'console':
        # Print results to console
        for result in results:
            print(f"\n{'='*50}")
            print(f"File: {result['file_name']}")
            print(f"{'='*50}")
            if result['success']:
                print(result['text'])
                if not result['text']:
                    print("(No text found)")
            else:
                print(f"ERROR: {result['error']}")
                
    elif output_format == 'json':
        # Save as JSON file
        if not output_path:
            output_path = Path('extracted_text_results.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to {output_path}")
        
    elif output_format == 'text':
        # Save individual text files
        if not output_path:
            output_path = Path('extracted_text')
        
        output_path.mkdir(exist_ok=True)
        
        for result in results:
            if result['success'] and result['text']:
                # Create filename from original image name
                text_filename = Path(result['file_name']).stem + '.txt'
                text_filepath = output_path / text_filename
                
                with open(text_filepath, 'w', encoding='utf-8') as f:
                    f.write(result['text'])
                    
        logger.info(f"Text files saved to {output_path}")


def main():
    """Main function to handle command line arguments and execute text extraction."""
    parser = argparse.ArgumentParser(
        description='Extract text from images using OCR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --single 1/f1_png.rf.029996f845fcea2f1e17351ad88ed765.jpg
  %(prog)s --batch --source-dir 1/ --format console
  %(prog)s --batch --source-dir . --format json --output-file results.json
  %(prog)s --batch --source-dir . --format text --output-dir ./extracted_text/
        """
    )
    
    # Processing mode
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--single', metavar='IMAGE_PATH',
                           help='Extract text from a single image')
    mode_group.add_argument('--batch', action='store_true',
                           help='Extract text from multiple images')
    
    # Source options
    parser.add_argument('--source-dir', default='.',
                       help='Source directory for batch processing (default: current directory)')
    
    # Output options
    parser.add_argument('--format', choices=['console', 'json', 'text'], default='console',
                       help='Output format (default: console)')
    parser.add_argument('--output-file', type=Path,
                       help='Output file path (for json format)')
    parser.add_argument('--output-dir', type=Path,
                       help='Output directory path (for text format)')
    
    # OCR options
    parser.add_argument('--tesseract-config', default='--oem 3 --psm 6',
                       help='Tesseract configuration string (default: --oem 3 --psm 6)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize extractor
    extractor = ImageTextExtractor(tesseract_config=args.tesseract_config)
    
    try:
        if args.single:
            # Single image processing
            results = [extractor.extract_text_from_image(args.single)]
        else:
            # Batch processing
            results = extractor.batch_extract_text(args.source_dir)
        
        if not results:
            logger.warning("No results to save")
            return
        
        # Determine output path
        output_path = None
        if args.format == 'json':
            output_path = args.output_file
        elif args.format == 'text':
            output_path = args.output_dir
        
        # Save results
        save_results(results, args.format, output_path)
        
        # Print summary
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        print(f"\nSummary:")
        print(f"Total images processed: {len(results)}")
        print(f"Successful extractions: {successful}")
        print(f"Failed extractions: {failed}")
        
        if failed > 0:
            print(f"\nFailed files:")
            for result in results:
                if not result['success']:
                    print(f"  - {result['file_name']}: {result['error']}")
    
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
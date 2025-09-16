#!/usr/bin/env python3
"""
Example usage of the ImageTextExtractor class for programmatic text extraction.

This script demonstrates how to use the OCR functionality in your own Python programs.
"""

import sys
import json
from pathlib import Path

# Import the extractor class from our main script
sys.path.append(str(Path(__file__).parent))
try:
    from extract_text import ImageTextExtractor
except ImportError:
    print("Error: extract_text.py not found. Make sure it's in the same directory.")
    sys.exit(1)


def example_single_image():
    """Example: Extract text from a single image."""
    print("=== Single Image Extraction Example ===")
    
    # Initialize the extractor
    extractor = ImageTextExtractor()
    
    # Extract text from a sample image
    image_path = "1/f1_png.rf.029996f845fcea2f1e17351ad88ed765.jpg"
    
    if not Path(image_path).exists():
        print(f"Sample image {image_path} not found. Using first available image...")
        # Find first available image
        images = extractor.find_images_in_directory(".")
        if images:
            image_path = images[0]
        else:
            print("No images found in current directory!")
            return
    
    result = extractor.extract_text_from_image(image_path)
    
    if result['success']:
        print(f"Successfully extracted text from: {result['file_name']}")
        print(f"Image size: {result['image_size']}")
        print(f"Text preview (first 200 chars):")
        print("-" * 50)
        print(result['text'][:200] + "..." if len(result['text']) > 200 else result['text'])
    else:
        print(f"Failed to extract text: {result['error']}")


def example_batch_processing():
    """Example: Batch process multiple images."""
    print("\n=== Batch Processing Example ===")
    
    # Initialize the extractor
    extractor = ImageTextExtractor()
    
    # Process images in directory 1 (limit to first 3 for this example)
    source_dir = "1"
    if Path(source_dir).exists():
        print(f"Processing images in directory: {source_dir}")
        
        # Get list of images
        images = extractor.find_images_in_directory(source_dir)
        
        # Process only first 3 images for this example
        sample_images = images[:3] if len(images) >= 3 else images
        
        for i, image_path in enumerate(sample_images, 1):
            print(f"\nProcessing {i}/{len(sample_images)}: {image_path.name}")
            result = extractor.extract_text_from_image(image_path)
            
            if result['success']:
                word_count = len(result['text'].split())
                print(f"  ✓ Extracted {word_count} words")
            else:
                print(f"  ✗ Failed: {result['error']}")
    else:
        print(f"Directory {source_dir} not found!")


def example_custom_configuration():
    """Example: Using custom Tesseract configuration."""
    print("\n=== Custom Configuration Example ===")
    
    # Initialize with custom Tesseract configuration
    # PSM modes: 3=Fully automatic page segmentation, 6=Uniform block of text
    custom_config = "--oem 3 --psm 3"
    extractor = ImageTextExtractor(tesseract_config=custom_config)
    
    print(f"Using custom config: {custom_config}")
    
    # Find first available image
    images = extractor.find_images_in_directory(".")
    if images:
        result = extractor.extract_text_from_image(images[0])
        if result['success']:
            print(f"Extracted text with custom config: {len(result['text'])} characters")
        else:
            print(f"Extraction failed: {result['error']}")
    else:
        print("No images found!")


def example_save_results():
    """Example: Process images and save results in different formats."""
    print("\n=== Save Results Example ===")
    
    extractor = ImageTextExtractor()
    
    # Process a few images
    source_dir = "."
    results = extractor.batch_extract_text(source_dir)
    
    # Limit results for this example
    results = results[:2] if len(results) >= 2 else results
    
    print(f"Processed {len(results)} images")
    
    # Save as JSON
    output_file = Path("example_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to: {output_file}")
    
    # Save as individual text files
    output_dir = Path("example_text_output")
    output_dir.mkdir(exist_ok=True)
    
    text_files_created = 0
    for result in results:
        if result['success'] and result['text'].strip():
            text_filename = Path(result['file_name']).stem + '.txt'
            text_filepath = output_dir / text_filename
            
            with open(text_filepath, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            text_files_created += 1
    
    print(f"Created {text_files_created} text files in: {output_dir}")


def main():
    """Run all examples."""
    print("Image Text Extraction Examples")
    print("=" * 50)
    
    try:
        example_single_image()
        example_batch_processing()
        example_custom_configuration()
        example_save_results()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("\nNote: Example output files have been created in the current directory.")
        print("Check: example_results.json and example_text_output/ directory")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip3 install -r requirements.txt")


if __name__ == "__main__":
    main()
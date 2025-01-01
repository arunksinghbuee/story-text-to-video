import os
from utility.image.background_image_generator import download_pollinations_image

def test_image_generation():
    # Test prompts
    test_prompts = [
        "a hungry fox moving in a dense jungle in search of food",
    ]
    
    # Create output directory if it doesn't exist
    output_dir = "test_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Test each prompt
    for i, prompt in enumerate(test_prompts):
        print(f"\nTesting prompt {i+1}: {prompt}")
        output_path = os.path.join(output_dir, f"test_image_{i+1}.jpg")
        
        success = download_pollinations_image(prompt, output_path)
        
        if success:
            print(f"✅ Successfully generated image: {output_path}")
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"   Image size: {size/1024:.2f} KB")
        else:
            print(f"❌ Failed to generate image for prompt: {prompt}")

if __name__ == "__main__":
    print("Starting image generation test...")
    test_image_generation()
    print("\nTest completed!") 
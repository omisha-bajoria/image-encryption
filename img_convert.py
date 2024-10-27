from PIL import Image
import numpy as np

def prepare_image_for_encryption(image_path, block_size=16, output_path="image_output.jpg"):
    # Load and convert image to RGB
    image = Image.open(image_path).convert("RGB")
    # image.save("step1.jpg")
    
    width, height = image.size
    
    # Calculate required new dimensions that are multiples of the block size
    new_width = (width + block_size - 1) // block_size * block_size
    new_height = (height + block_size - 1) // block_size * block_size
    resized_image = image.resize((new_width, new_height))
    
    # Convert resized image to a byte array
    pixel_matrix = np.array(resized_image)
    byte_array = pixel_matrix.tobytes()
    
    # Calculate the exact byte length needed for reshaping to (new_height, new_width, 3)
    required_size = new_height * new_width * 3
    
    # Calculate padding length
    padding_len = required_size - len(byte_array)
    
    # Manually pad the byte array
    padded_byte_array = byte_array + bytes([0] * padding_len)
    
    # Convert back to an array and reshape based on new dimensions
    encrypted_pixel_matrix = np.frombuffer(padded_byte_array, dtype=np.uint8).reshape((new_height, new_width, 3))
    
    # Create and save the processed image
    encrypted_image = Image.fromarray(encrypted_pixel_matrix, "RGB")
    encrypted_image.save(output_path)
    print(f"Image saved as {output_path}")

# Example usage
image_path = "D:\\cse materials\\sem 5\\FC\\image encryption\\gymkhana_logo.png"  # Update with actual path
prepare_image_for_encryption(image_path, block_size=16, output_path="image_output.jpg")





# from PIL import Image
# import numpy as np

# # Load image
# image = Image.open("gymkhana_logo.png")

# # Convert to grayscale or RGB (depending on encryption requirements)
# # Grayscale: Each pixel is a single intensity value (0–255)
# image = image.convert("L")  # 'L' for grayscale, or use 'RGB' for color

# # Convert image to pixel matrix
# pixel_matrix = np.array(image)

# # Convert pixel matrix to a byte array
# byte_array = pixel_matrix.tobytes()

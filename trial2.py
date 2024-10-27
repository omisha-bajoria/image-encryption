from PIL import Image
import numpy as np
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

def encrypt_channel(channel_data, key):
    # Initialize DES cipher in ECB mode
    cipher = DES.new(key, DES.MODE_ECB)
    # Pad the channel data to make it a multiple of the DES block size (8 bytes)
    padded_data = pad(channel_data.tobytes(), DES.block_size)
    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

def save_color_channel_image(channel, color, filename):
    # Create a zero matrix for the other two channels
    zero_channel = np.zeros_like(channel)
    if color == "R":
        color_image = np.stack((channel, zero_channel, zero_channel), axis=2)
    elif color == "G":
        color_image = np.stack((zero_channel, channel, zero_channel), axis=2)
    elif color == "B":
        color_image = np.stack((zero_channel, zero_channel, channel), axis=2)
    Image.fromarray(color_image, "RGB").save(filename)

def process_image(image_path):
    # Load and convert image to RGB
    image = Image.open(image_path).convert("RGB")
    pixel_matrix = np.array(image)
    
    # Split image into R, G, and B channels
    r_channel, g_channel, b_channel = pixel_matrix[:, :, 0], pixel_matrix[:, :, 1], pixel_matrix[:, :, 2]
    
    # Save the original channels in color
    save_color_channel_image(r_channel, "R", "original_R_channel.jpg")
    save_color_channel_image(g_channel, "G", "original_G_channel.jpg")
    save_color_channel_image(b_channel, "B", "original_B_channel.jpg")
    
    # Generate three DES keys for R, G, and B channels
    key_r = get_random_bytes(8)
    key_g = get_random_bytes(8)
    key_b = get_random_bytes(8)
    
    # Encrypt each channel separately and store encrypted images as bytes
    encrypted_r = encrypt_channel(r_channel, key_r)
    encrypted_g = encrypt_channel(g_channel, key_g)
    encrypted_b = encrypt_channel(b_channel, key_b)
    
    # Get the size of the original image
    original_height, original_width = r_channel.shape
    
    # Convert encrypted byte arrays back to numpy arrays with original dimensions
    encrypted_r_array = np.frombuffer(encrypted_r, dtype=np.uint8)[:original_height * original_width].reshape(original_height, original_width)
    encrypted_g_array = np.frombuffer(encrypted_g, dtype=np.uint8)[:original_height * original_width].reshape(original_height, original_width)
    encrypted_b_array = np.frombuffer(encrypted_b, dtype=np.uint8)[:original_height * original_width].reshape(original_height, original_width)
    
    # Save the encrypted channels as images in color
    save_color_channel_image(encrypted_r_array, "R", "encrypted_R_channel.jpg")
    save_color_channel_image(encrypted_g_array, "G", "encrypted_G_channel.jpg")
    save_color_channel_image(encrypted_b_array, "B", "encrypted_B_channel.jpg")
    
    # Combine encrypted channels to form the final encrypted image
    encrypted_image_matrix = np.stack((encrypted_r_array, encrypted_g_array, encrypted_b_array), axis=2)
    encrypted_image = Image.fromarray(encrypted_image_matrix, "RGB")
    encrypted_image.save("final_encrypted_image.jpg")
    
    print("Images saved: original channels, encrypted channels, and final encrypted image.")

# Example usage
image_path = "D:\\cse materials\\sem 5\\FC\\image encryption\\gymkhana_logo.png"  # Update with actual path
process_image(image_path)

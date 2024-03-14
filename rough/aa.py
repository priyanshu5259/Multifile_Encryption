from PIL import Image
import numpy as np

def encrypt_image(image_path, key, num_iterations):
    img = Image.open(image_path)
    img_array = np.array(img, dtype=np.uint8)
    
    for _ in range(num_iterations):
        img_array = img_array.astype(np.uint32) ^ key
    
    encrypted_img = Image.fromarray(img_array.astype(np.uint8))
    encrypted_img.save("encrypted_image.png")

def decrypt_image(encrypted_path, key, num_iterations):
    encrypted_img = Image.open(encrypted_path)
    encrypted_array = np.array(encrypted_img, dtype=np.uint8)
    
    for _ in range(num_iterations):
        encrypted_array = encrypted_array.astype(np.uint32) ^ key
    
    decrypted_img = Image.fromarray(encrypted_array.astype(np.uint8))
    decrypted_img.save("decrypted_image.png")

# Example usage
image_path = r"C:\Users\Priyanshu\Desktop\Multilevel Encryption(Crypto)\img.png"

encryption_key = 8800096496
num_iterations = 3

# Encrypt the image multiple times
encrypt_image(image_path, encryption_key, num_iterations)

# Decrypt the image multiple times
decrypt_image("encrypted_image.png", encryption_key, num_iterations)

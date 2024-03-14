from flask import Flask, render_template, request, flash, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image

import PyPDF2

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secret key

# Directory for uploading files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def encrypt_image(input_file, output_file, key):
    # Open the input image
    img = Image.open(input_file)
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Get dimensions of the image
    height, width, channels = img_array.shape
    
    # Flatten the image array
    flat_img_array = img_array.reshape(-1, channels)
    
    # Generate permutation based on the key
    np.random.seed(key)
    permutation = np.random.permutation(flat_img_array.shape[0])
    
    # Shuffle the flattened array based on the permutation
    shuffled_img_array = flat_img_array[permutation]
    
    # Reshape the shuffled array back to image dimensions
    shuffled_img_array = shuffled_img_array.reshape(height, width, channels)
    
    # Save the encrypted image
    encrypted_img = Image.fromarray(shuffled_img_array.astype('uint8'))
    encrypted_img.save(output_file)

def decrypt_image(input_file, output_file, key):
    # Open the encrypted image
    img_encrypted = Image.open(input_file)
    
    # Convert image to numpy array
    img_encrypted_array = np.array(img_encrypted)
    
    # Get dimensions of the image
    height, width, channels = img_encrypted_array.shape
    
    # Flatten the image array
    flat_img_encrypted_array = img_encrypted_array.reshape(-1, channels)
    
    # Generate permutation based on the key
    np.random.seed(key)
    permutation = np.random.permutation(flat_img_encrypted_array.shape[0])
    
    # Reverse the permutation
    inverse_permutation = np.argsort(permutation)
    
    # Shuffle the flattened array back to original order based on inverse permutation
    flat_img_decrypted_array = flat_img_encrypted_array[inverse_permutation]
    
    # Reshape the decrypted array back to image dimensions
    img_decrypted_array = flat_img_decrypted_array.reshape(height, width, channels)
    
    # Save the decrypted image
    decrypted_img = Image.fromarray(img_decrypted_array.astype('uint8'))
    decrypted_img.save(output_file)

def encrypt_text(text, key1, key2, key3):
    result1 = caesar_cipher(text, key1)
    result2 = multiplicative_cipher(result1, key2)
    result = vigenere_cipher(result2, str(key3))
    return result

def decrypt_text(text, key1, key2, key3):
    result3 = vigenere_decipher(text, str(key3))
    result2 = multiplicative_decipher(result3, key2)
    result1 = caesar_decipher(result2, key1)
    return result1

def caesar_cipher(text, key):
    result1 = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + key
            if char.isupper():
                result1 += chr((shifted - 65) % 26 + 65)
            else:
                result1 += chr((shifted - 97) % 26 + 97)
        else:
            result1 += char
    return result1

def multiplicative_cipher(text, key):
    result2 = ""
    for char in text:
        if char.isalpha():
            result2 += chr(((ord(char) - 65) * key) % 26 + 65) if char.isupper() else chr(((ord(char) - 97) * key) % 26 + 97)
        else:
            result2 += char
    return result2

def vigenere_cipher(text, key):
    result = ""  # Initialize the variable before using it
    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]
    for i in range(len(text)):
        if text[i].isalpha():
            shift = ord(key[i].upper()) - 65
            result += chr((ord(text[i]) + shift - 65) % 26 + 65) if text[i].isupper() else chr((ord(text[i]) + shift - 97) % 26 + 97)
        else:
            result += text[i]
    return result

def caesar_decipher(text, key):
    result1 = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) - key  # Use subtraction for decryption
            if char.isupper():
                result1 += chr((shifted - 65) % 26 + 65)
            else:
                result1 += chr((shifted - 97) % 26 + 97)
        else:
            result1 += char
    return result1

def multiplicative_decipher(text, key):
    result2 = ""
    mod_inverse = 0
    for i in range(26):
        if (i * key) % 26 == 1:
            mod_inverse = i
    for char in text:
        if char.isalpha():
            result2 += chr(((ord(char) - 65) * mod_inverse) % 26 + 65) if char.isupper() else chr(((ord(char) - 97) * mod_inverse) % 26 + 97)
        else:
            result2 += char
    return result2

def vigenere_decipher(text, key):
    result = ""
    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]
    for i in range(len(text)):
        if text[i].isalpha():
            shift = ord(key[i].upper()) - 65
            result += chr((ord(text[i]) - shift - 65) % 26 + 65) if text[i].isupper() else chr((ord(text[i]) - shift - 97) % 26 + 97)
        else:
            result += text[i]
    return result

def encrypt_pdf(input_file, output_file, password):
    # Open the PDF file to encrypt
    with open(input_file, "rb") as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Create a PDF writer object
        pdf_writer = PyPDF2.PdfFileWriter()

        # Copy all the pages from the reader to the writer
        for page in range(pdf_reader.numPages):
            pdf_writer.addPage(pdf_reader.getPage(page))

        # Encrypt the PDF file with the password
        pdf_writer.encrypt(password)

        # Open a new PDF file to write the encrypted content
        with open(output_file, "wb") as encrypted_file:
            # Write the encrypted content to the new file
            pdf_writer.write(encrypted_file)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file_type = request.form.get("file_type")
        if file_type == "text":
            return redirect("/text")
        elif file_type == "image":
            return redirect("/image")
        elif file_type == "pdf":
            return redirect("/pdf_encrypt")
    return render_template("index.html")

@app.route("/text", methods=["GET", "POST"])
def text_index():
    if request.method == "POST":
        plaintext = request.form.get("plaintext")
        if plaintext:
            key1 = int(request.form.get("key1"))
            key2 = int(request.form.get("key2"))
            key3 = int(request.form.get("key3"))
            encrypted_text1 = caesar_cipher(plaintext, key1)
            encrypted_text2 = multiplicative_cipher(encrypted_text1, key2)
            encrypted_text = vigenere_cipher(encrypted_text2, str(key3))
            decrypted_text3 = vigenere_decipher(encrypted_text, str(key3))
            decrypted_text2 = multiplicative_decipher(decrypted_text3, key2)
            decrypted_text1 = caesar_decipher(decrypted_text2, key1)
            return render_template("text_result.html",  
                                   
                                   encrypted_text=encrypted_text,
                                   decrypted_text1=decrypted_text1,
                                   )
        else:
            flash("Please enter some text")
            return redirect("/text")  # Redirect back to the text input page if no text is provided
    return render_template("text_index.html")

@app.route("/image", methods=["GET", "POST"])
def image_index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            key = request.form.get("key")
            key = int(key) if key else None
            if not key:
                flash("Please enter a valid key")
                return redirect(request.url)
            encrypted_file = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_' + filename)
            decrypted_file = os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted_' + filename)
            encrypt_image(filepath, encrypted_file, key)
            decrypt_image(encrypted_file, decrypted_file, key)
            return render_template("image_result.html", encrypted_file='encrypted_' + filename, decrypted_file='decrypted_' + filename)
    return render_template("image_index.html")

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

# Route for PDF encryption form
@app.route("/pdf_encrypt", methods=["GET", "POST"])
def pdf_index():
    if request.method == "POST":
        # Check if a file and password were provided
        if "pdf_file" not in request.files:
            flash("No PDF file provided")
            return redirect(url_for("pdf_index"))
        file = request.files["pdf_file"]
        password = request.form.get("password")
        if not file:
            flash("No file selected")
            return redirect(url_for("pdf_index"))
        if not password:
            flash("Please enter a password")
            return redirect(url_for("pdf_index"))
        
        # Save the uploaded PDF file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Encrypt the PDF file
        encrypted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_' + filename)
        encrypt_pdf(filepath, encrypted_filepath, password)
        
        # Redirect to the result page
        return redirect(url_for("pdf_result", encrypted_file=os.path.basename(encrypted_filepath)))

    return render_template("pdf_index.html")

# Route for PDF encryption result
@app.route("/pdf_result", methods=["GET"])
def pdf_result():
    encrypted_file = request.args.get("encrypted_file")
    if encrypted_file:
        filename = os.path.basename(encrypted_file)
        return render_template("pdf_result.html", encrypted_file=encrypted_file, filename=filename)
    else:
        flash("Encrypted file not found")
        return redirect(url_for("pdf_index"))
    
# Route for downloading encrypted PDF file
@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

# Import PyPDF2 library
import PyPDF2

# Open the PDF file to encrypt
pdf_file = open("Priyanshu Dayaramani_21BCE5259_Lab-8.pdf", "rb")

# Create a PDF reader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Create a PDF writer object
pdf_writer = PyPDF2.PdfFileWriter()

# Copy all the pages from the reader to the writer
for page in range(pdf_reader.numPages):
    pdf_writer.addPage(pdf_reader.getPage(page))

# Set the password for the PDF file
password = "secret"

# Encrypt the PDF file with the password
pdf_writer.encrypt(password)

# Open a new PDF file to write the encrypted content
encrypted_file = open("encrypted_sample.pdf", "wb")

# Write the encrypted content to the new file
pdf_writer.write(encrypted_file)

# Close the files
pdf_file.close()
encrypted_file.close()

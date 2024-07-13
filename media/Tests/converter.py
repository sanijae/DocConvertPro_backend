# import os
# import jpype
# jpype.startJVM()
# from asposecells.api import Workbook, FileFormatType, PdfSaveOptions
# import pandas as pd
# from tabula import read_pdf
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# import tabula
# import zipfile


# def excelToPdf():

#         inputFile = "file_example_XLSX_5000_Qf8SSZv.xlsx"
#         outputFile = "FexcelPdf.pdf"

#         workbook = Workbook(inputFile)
#         saveOptions = PdfSaveOptions()
#         #saveOptions.setOnePagePerSheet(True)
#         workbook.save(outputFile)

#         jpype.shutdownJVM()

# def pdfToCsv():

#         inputFile = "file_example_XLSX_5000_Qf8SSZv.xlsx"
#         outputFile = "ToPDF.pdf"

#         # # convert all PDFs in a directory
#         # tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')

#         data = tabula.convert_into('ToPDF.pdf','demo.csv',pages='all',output_format='csv')
#         return data

# def pdfToExcel():

#         inputFile = "ToPDF.pdf"
#         tables = read_pdf(inputFile, pages='all', multiple_tables=True)
#         combined_df = pd.concat(tables)
        
#         return combined_df.to_excel('excel_path.xlsx', index=False)

#         # data = tabula.convert_into('ToPDF.pdf','demo.xlsx', output_format="xlsx")
#         # return data

# def csvToPdf():

#     df = pd.read_csv('demo.csv')
#     doc = SimpleDocTemplate('demo.pdf', pagesize=letter)
#     data = [df.columns.tolist()] + df.values.tolist()
#     # Convert DataFrame to list of lists for Table creation
#     data = [df.columns.tolist()] + df.values.tolist()

#     # Create Table object
#     table = Table(data)

#     # Style the table
#     style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                         ('GRID', (0, 0), (-1, -1), 1, colors.black)])

#     #table.setStyle(style)

#     # Add table to PDF document
#     return doc.build([table])

# from pdf2image import convert_from_path
# from pptx import Presentation

# def pdfToPpt():
#     # Convert each page of the PDF to an image
#     images = convert_from_path('ToPDF.pdf')
#     prs = Presentation()

#     # Insert each image as a slide in the presentation
#     for img in images:
#         slide = prs.slides.add_slide(prs.slide_layouts[5])  # Use a blank layout
#         left = top = 0
#         slide.shapes.add_picture(img, left, top)

#     # Save the PowerPoint presentation
#     return prs.save('demo.ppt')

# import fitz

# def pdf_to_images(pdf_path, image_folder):
#     # Open the PDF
#     pdf_document = fitz.open(pdf_path)
#     for page_number in range(len(pdf_document)):
#         # Get the page
#         page = pdf_document.load_page(page_number)
        
#         # Convert the page to a pixmap
#         pixmap = page.get_pixmap()
        
#         # Save the pixmap as an image
#         image_path = f"{image_folder}/page_{page_number + 1}.bmp"  # or png, or other image formats
#         pixmap.save(image_path)  # or writeJPEG, or other image formats
        
#         print(f"Page {page_number + 1} saved as {image_path}")
    
#     # Close the PDF
#     pdf_document.close()


# # Usage
# pdf_path = "myfile.pdf"  # Path to your PDF file
# image_folder = "BMP/"  # Folder where the images will be saved
# #pdf_to_images(pdf_path, image_folder)

# from PIL import Image

# def pdf_to_bmp(pdf_path, image_folder,bmp_folder):
#     # Open the PDF
#     pdf_document = fitz.open(pdf_path)
    
#     # Iterate through each page
#     for page_number in range(len(pdf_document)):
#         # Get the page
#         page = pdf_document.load_page(page_number)
        
#         # Convert the page to a pixmap
#         pixmap = page.get_pixmap()
        
#         # Save the pixmap as a PNG or JPEG image first
#         temp_image_path = f"{image_folder}/temp_page_{page_number + 1}.png"
#         pixmap.save(temp_image_path)
        
#         # Open the image and convert it to BMP
#         with Image.open(temp_image_path) as image:
#             bmp_image_path = f"{bmp_folder}/page_{page_number + 1}.bmp"
#             image.save(bmp_image_path)
        
#         print(f"Page {page_number + 1} saved as {bmp_image_path}")
    
#     # Close the PDF
#     pdf_document.close()

#     # Create a zip file
#     zip_file_path = f"{image_folder}.zip"
#     with zipfile.ZipFile(zip_file_path, 'w') as zipf:
#         # Add all files in the image folder to the zip file
#         for root, _, files in os.walk(image_folder):
#             for file in files:
#                 zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), image_folder))

#     print(f"Images zipped and saved as {zip_file_path}")

# # Usage
# pdf_path = "myfile.pdf"  # Path to your PDF file
# image_folder = "Image_BMP/"
# bmp_folder = "BMP"  # Folder where the images will be saved
# #pdf_to_bmp(pdf_path, image_folder,bmp_folder)

# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from PIL import Image

# def images_to_pdf(image_paths, output_pdf):
#     # Get a list of all files in the directory
#     files = os.listdir(image_paths)
    
#     # Filter only image files
#     image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
#     c = canvas.Canvas(output_pdf, pagesize=letter)
#     width, height = letter
    
#     for image_file in image_files:
#         # Construct the full path to the image
#         image_path = os.path.join(image_folder, image_file)
        
#         img = Image.open(image_path)
#         img_width, img_height = img.size
        
#         # Calculate aspect ratio
#         aspect_ratio = img_width / img_height
        
#         # Scale the image to fit the page
#         if aspect_ratio >= 1:
#             img_width = width
#             img_height = width / aspect_ratio
#         else:
#             img_height = height
#             img_width = height * aspect_ratio
        
#         c.drawImage(image_path, 0, 0, width=img_width, height=img_height)
#         c.showPage()

#     c.save()
#     print(f"Images converted to PDF: {output_pdf}")

# # Usage
# image_paths = 'BMP'  # List of image paths
# output_pdf = "jpg_to_pdf.pdf"  # Output PDF file path
# #images_to_pdf(image_paths, output_pdf)

# import PyPDF2

# def split_pdf(input_pdf, output_folder):
#     # Open the PDF file
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
        
#         # Iterate through each page
#         for page_number in range(len(reader.pages)):
#             writer = PyPDF2.PdfWriter()
#             writer.add_page(reader.pages[page_number])
            
#             # Create a new PDF file for each page
#             output_pdf = f"{output_folder}/page_{page_number + 1}.pdf"
#             with open(output_pdf, 'wb') as output_file:
#                 writer.write(output_file)
            
#             print(f"Page {page_number + 1} saved as {output_pdf}")

# # Usage
# input_pdf = "myfile.pdf"  # Path to your input PDF file
# output_folder = "split_pdf/"  # Folder where the split PDF pages will be saved
# #split_pdf(input_pdf, output_folder)

# import PyPDF2

# def merge_pdfs(input_pdfs, output_pdf):
#     # Create a PDF writer object
#     pdf_writer = PyPDF2.PdfWriter()
#      # Iterate through each file in the input folder
#     for filename in os.listdir(input_pdfs):
#         # Check if the file is a PDF
#         if filename.endswith('.pdf'):
#             # Construct the full path to the PDF file
#             input_pdf = os.path.join(input_pdfs, filename)
            
#             # Open the PDF file
#             with open(input_pdf, 'rb') as file:
#                 # Create a PDF reader object
#                 pdf_reader = PyPDF2.PdfReader(file)
                
#                 # Iterate through each page and add it to the writer object
#                 for page_number in range(len(pdf_reader.pages)):
#                     page = pdf_reader.pages[page_number]
#                     pdf_writer.add_page(page)
    
#     # Write the merged PDF to the output file
#     with open(output_pdf, 'wb') as output_file:
#         pdf_writer.write(output_file)

# # Usage
# input_pdfs = 'split_pdf/'  # List of input PDF files
# output_pdf = "merged_pdf.pdf"  # Output PDF file path
# # merge_pdfs(input_pdfs, output_pdf)

# import subprocess

# def compress_pdf_with_ghostscript(input_pdf_path, output_pdf_path):
#     # Command to compress PDF using ghostscript
#     command = [
#         'gs',  # Ghostscript command
#         '-sDEVICE=pdfwrite',  # Output device
#         '-dCompatibilityLevel=1.4',
#         '-dNOPAUSE',
#         '-dQUIET',
#         '-dBATCH',
#         '-dPDFSETTINGS=/printer',  # Compression level (change as needed)
#         '-o', output_pdf_path,  # Output file
#         input_pdf_path  # Input file
#     ]

#     # Execute the ghostscript command
#     subprocess.run(command)

# # Example usage
# input_pdf_path = "file.pdf"
# output_pdf_path = "d_file.pdf"

# #compress_pdf_with_ghostscript(input_pdf_path, output_pdf_path)


# # Usage
# input_pdf = "myfile.pdf"  # Input PDF file path
# output_pdf = "compress-file.pdf"  # Output PDF file path
# #compress_pdf(input_pdf, output_pdf)
# import PyPDF2

# def fill_pdf_with_text(input_pdf, output_pdf, field_data):
#     # Open the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Iterate through each page of the PDF
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]

#             # Create a new PDF page
#             new_page = writer.add_page(page)

#             # Get the PDF page's dimensions
#             page_width = page.mediaBox[2]
#             page_height = page.mediaBox[3]

#             # Get the form field data for the current page
#             page_field_data = field_data.get(page_number + 1, {})

#             # Overlay text on the PDF for each form field
#             for field_name, field_value in page_field_data.items():
#                 writer.add_text(
#                     new_page,
#                     x=page_width / 2,  # Adjust position as needed
#                     y=page_height / 2,  # Adjust position as needed
#                     text=field_value,
#                     fontname="Helvetica",  # Choose a font
#                     fontsize=12,  # Choose font size
#                     align="center"  # Align text
#                 )

#         # Write the filled PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "input_form.pdf"  # Input PDF form file path
# output_pdf = "filled_output.pdf"  # Output filled PDF file path
# field_data = {
#     1: {"Field1": "Value1"},
#     2: {"Field2": "Value2"}
#     # Add more pages and fields as needed
# }
# #fill_pdf_with_text(input_pdf, output_pdf, field_data)

# import PyPDF2

# def extract_pages(input_pdf, output_pdf, start_page, end_page):
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         for page_number in range(start_page - 1, end_page):
#             writer.add_page(reader.pages[page_number])

#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "myfile.pdf"  # Input PDF file path
# output_pdf = "extracted_pages.pdf"  # Output extracted PDF file path
# start_page = 3  # Start page number (inclusive)
# end_page = 9  # End page number (inclusive)
# #extract_pages(input_pdf, output_pdf, start_page, end_page)

# import PyPDF2

# def remove_pages(input_pdf, output_pdf, pages_to_remove):
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         for page_number in range(len(reader.pages)):
#             if page_number + 1 not in pages_to_remove:
#                 writer.add_page(reader.pages[page_number])

#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "myfile.pdf"  # Input PDF file path
# output_pdf = "remove_pages.pdf"  # Output PDF file path
# pages_to_remove = [2, 5, 7]  # List of page numbers to remove
# #remove_pages(input_pdf, output_pdf, pages_to_remove)

# import PyPDF2

# import PyPDF2

# def add_pages_between(input_pdf, output_pdf, page_to_add, insert_after_page):
#     # Open the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Add existing pages to the writer until the insertion point
#         for page_number in range(insert_after_page):
#             writer.add_page(reader.pages[page_number])

#         # Open the PDF containing the page to add
#         with open(page_to_add, 'rb') as page_file:
#             page_reader = PyPDF2.PdfReader(page_file)
#             #page = page_reader.pages[0]  # Assuming you want to add the first page
#             #writer.add_page(page)
#             for page in page_reader.pages:
#                 writer.add_page(page)

#         # Add remaining existing pages after the insertion point
#         for page_number in range(insert_after_page, len(reader.pages)):
#             writer.add_page(reader.pages[page_number])

#         # Write the modified PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "pdf.pdf"  # Input PDF file path
# output_pdf = "added_pages.pdf"  # Output PDF file path
# page_to_add = "myfile.pdf"  # PDF file containing the page to add
# insert_after_page = 1  # Insert pages after this page number (0-indexed)
# #add_pages_between(input_pdf, output_pdf, page_to_add, insert_after_page)

# import PyPDF2

# def reorder_pages(input_pdf, output_pdf, page_order):
#     # Open the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Reorder pages according to the specified page order
#         for page_number in page_order:
#             writer.add_page(reader.pages[page_number])

#         # Write the reordered PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "bmp_to_pdf.pdf"  # Input PDF file path
# output_pdf = "reordered_output.pdf"  # Output PDF file path
# page_order = [2, 0,]  # Desired page order (0-indexed)
# #reorder_pages(input_pdf, output_pdf, page_order)

# import PyPDF2

# def repair_pdf(input_pdf, output_pdf):
#     # Open the input PDF in read-binary mode
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
        
#         # Create a new PDF writer
#         writer = PyPDF2.PdfWriter()

#         # Iterate through each page of the input PDF
#         for page_number in range(len(reader.pages)):
#             try:
#                 # Try to read the page
#                 page = reader.pages[page_number]
#                 # Add the page to the writer
#                 writer.add_page(page)
#             except Exception as e:
#                 # If there's an error reading the page, skip it and continue
#                 print(f"Error reading page {page_number + 1}: {e}")
#                 continue

#         # Write the repaired PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "pdf.pdf"  # Input PDF file path
# output_pdf = "repaired.pdf"  # Output PDF file path
# #repair_pdf(input_pdf, output_pdf)

# import PyPDF2

# def rotate_pdf(input_pdf, output_pdf, rotation_angle):
#     # Open the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Rotate each page and add it to the writer
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]
#             page.rotate(rotation_angle)  # Rotate the page
#             writer.add_page(page)

#         # Write the modified PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "pdf.pdf"  # Input PDF file path
# output_pdf = "rotated_output.pdf"  # Output PDF file path
# rotation_angle = 90  # Rotation angle in degrees (clockwise)
# #rotate_pdf(input_pdf, output_pdf, rotation_angle)

# import PyPDF2

# def add_watermark(input_pdf, watermark_pdf, output_pdf):
#     # Open the input PDF and watermark PDF
#     with open(input_pdf, 'rb') as input_file, open(watermark_pdf, 'rb') as watermark_file:
#         reader = PyPDF2.PdfReader(input_file)
#         watermark_reader = PyPDF2.PdfReader(watermark_file)
#         watermark_page = watermark_reader.pages[0]

#         # Create a new PDF writer
#         writer = PyPDF2.PdfWriter()

#         # Overlay the watermark on each page of the input PDF
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]
#             page.merge_page(watermark_page)  # Merge the watermark onto the page
#             writer.add_page(page)

#         # Write the modified PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "pdf.pdf"  # Input PDF file path
# watermark_pdf = "page_1.pdf"  # Watermark PDF file path
# output_pdf = "watermarked_output.pdf"  # Output PDF file path
# #add_watermark(input_pdf, watermark_pdf, output_pdf)

# import PyPDF2

# def remove_watermarks(input_pdf, output_pdf):
#     # Open the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Iterate through each page
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]
            
#             # Check for annotations (watermarks) and exclude them
#             annotations = page.get('/Annots')
#             if annotations:
#                 for annotation in annotations:
#                     annotation_object = reader.get_object(annotation)
#                     subtype = annotation_object.get('/Subtype')
#                     if subtype and subtype.lower() == '/stamp':
#                         continue  # Skip stamp annotations (potentially watermarks)
            
#             # Add the page to the writer
#             writer.add_page(page)

#         # Write the modified PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# import PyPDF2

# def remove_watermark(input_pdf, output_pdf):
#     # Open the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Iterate through each page
#         for page_number in range(len(reader.pages)):
#             page = reader.pages[page_number]
            
#             # Check for annotations (watermarks) and exclude them
#             annotations = page.get('/Annots')
#             if annotations:
#                 for annotation in annotations:
#                     annotation_object = reader.get_object(annotation)
#                     subtype = annotation_object.get('/Subtype')
#                     print(f"Annotation Subtype: {subtype}")
#                     if subtype and subtype.lower() == '/stamp':
#                         print("Skipping stamp annotation (potential watermark)")
#                         continue  # Skip stamp annotations (potentially watermarks)
            
#             # Add the page to the writer
#             writer.add_page(page)

#         # Write the modified PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "watermarked_output.pdf"  # Input PDF file path
# output_pdf = "remove_watermarked_output.pdf"  # Output PDF file path
# #remove_watermark(input_pdf, output_pdf)

# import PyPDF4

# def protect_pdf(input_pdf, output_pdf, user_password=None, owner_password=None):
#     # Open the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF4.PdfFileReader(file)
        
#         # Create a PDF writer object
#         writer = PyPDF4.PdfFileWriter()
        
#         # Add each page to the writer
#         for page in reader.pages:
#             writer.addPage(page)
        
#         # Set encryption options
#         encryption_kwargs = {
#             'user_pwd': user_password,
#             'owner_pwd': owner_password,
#             'use_128bit': False  # Use AES-256 encryption
#         }
#         writer.encrypt(**encryption_kwargs)
        
#         # Write the protected PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "pdf.pdf"  # Input PDF file path
# output_pdf = "protected_output.pdf"  # Output PDF file path
# user_password = "user_password"  # Password required to open the PDF (optional)
# owner_password = "owner_password"  # Password required to modify permissions (optional)
# #protect_pdf(input_pdf, output_pdf, user_password, owner_password)

# import fitz

# def unlock_pdf(input_pdf, output_pdf, password):
#     # Open the input PDF
#     pdf_document = fitz.open(input_pdf)
    
#     # Attempt to unlock the PDF with the provided password
#     if pdf_document.is_encrypted:
#         try:
#             pdf_document.authenticate(password)
#             pdf_document.save(output_pdf)
#             pdf_document.close()
#             print("PDF successfully unlocked.")
#         except:
#             print("Incorrect password. Unable to unlock PDF.")
#     else:
#         print("PDF is not encrypted. No password required.")

# # Usage
# input_pdf = "protected_output.pdf"  # Input PDF file path
# output_pdf = "unlocked_output.pdf"  # Output PDF file path
# password = "user_password"  # Password required to open the PDF
# #unlock_pdf(input_pdf, output_pdf, password)

# import PyPDF2
# import hashlib
# import OpenSSL.crypto
# import os

# def signs_pdf(input_pdf, output_pdf, signature_field_name, pfx_file, pfx_password):
#     # Read the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Copy pages from input PDF to output PDF
#         for page in reader.pages:
#             writer.add_page(page)

#         # Load the PKCS#12 file (PFX/P12) containing the certificate and private key
#         pfx = OpenSSL.crypto.load_pkcs12_data(open(pfx_file, 'rb').read(), pfx_password)

#         # Get the certificate and private key
#         cert = pfx.get_certificate()
#         key = pfx.get_privatekey()

#         # Create a signature field
#         signature_field = PyPDF2.generic.DictionaryObject()
#         signature_field.update({
#             '/Type': '/Annot',
#             '/Subtype': '/Widget',
#             '/FT': '/Sig',
#             '/Rect': [0, 0, 0, 0],
#             '/T': signature_field_name,
#             '/V': PyPDF2.generic.NameObject('/Signature' + signature_field_name),
#             '/P': writer.pages[0].indirectRef,
#             '/F': 4,
#             '/AP': PyPDF2.generic.DictionaryObject({
#                 '/N': writer.pages[0].indirectRef
#             })
#         })

#         # Add the signature field to each page
#         for page in writer.pages:
#             page['/Annots'] = page.get('/Annots', PyPDF2.generic.ArrayObject())
#             page['/Annots'].append(signature_field)

#         # Create the signature object
#         signature = OpenSSL.crypto.sign(key, reader.stream.getvalue(), 'sha256')

#         # Create the signature dictionary
#         signature_dict = PyPDF2.generic.DictionaryObject({
#             '/Type': '/Sig',
#             '/Filter': '/Adobe.PPKLite',
#             '/SubFilter': '/adbe.pkcs7.detached',
#             '/ByteRange': [0, 0, 0, 0],
#             '/Contents': signature
#         })

#         # Add the signature dictionary to each page
#         for page in writer.pages:
#             page[PyPDF2.generic.NameObject('/' + signature_field_name)] = signature_dict

#         # Write the signed PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# from cryptography.hazmat.primitives import serialization, hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives.serialization import pkcs12
# from cryptography.hazmat.backends import default_backend
# import PyPDF2
# from PyPDF2.generic import NameObject, DictionaryObject, ArrayObject, ByteStringObject

# def sign_pdf(input_pdf, output_pdf, signature_field_name, pfx_data, pfx_password):
#     # Read the input PDF
#     with open(input_pdf, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         writer = PyPDF2.PdfWriter()

#         # Copy pages from input PDF to output PDF
#         for page in reader.pages:
#             writer.add_page(page)

#         # Load the PKCS#12 file from binary data
#         pfx = pkcs12.load_key_and_certificates(pfx_data, pfx_password)

#         # Get the certificate and private key
#         private_key = pfx[0]

#         # Create the signature object
#         pdf_content = b"".join(page.extract_text().encode() for page in reader.pages)
#         signature = private_key.sign(pdf_content, padding.PKCS1v15(), hashes.SHA256())

#         # Create the signature dictionary
#         signature_dict = DictionaryObject({
#             NameObject('/Type'): NameObject('/Sig'),
#             NameObject('/Filter'): NameObject('/Adobe.PPKLite'),
#             NameObject('/SubFilter'): NameObject('/adbe.pkcs7.detached'),
#             NameObject('/ByteRange'): ArrayObject([ByteStringObject(b'0'), ByteStringObject(b'0'), ByteStringObject(b'0'), ByteStringObject(b'0')]),
#             NameObject('/Contents'): ByteStringObject(signature)
#         })

#         # Add the signature dictionary to each page
#         for page in writer.pages:
#             if '/Annots' not in page:
#                 page[NameObject('/Annots')] = ArrayObject()
#             annots = page[NameObject('/Annots')]
#             annots.append(signature_dict)
#             page[NameObject('/Annots')] = annots
#             page[NameObject('/' + signature_field_name)] = signature_dict

#         # Write the signed PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             writer.write(output_file)

# # Usage
# input_pdf = "pdf.pdf"  # Input PDF file path
# output_pdf = "signed.pdf"  # Output PDF file path
# signature_field_name = "SignatureField"  # Name of the signature field
# # pfx_file = "../PKS#12/certificate.pfx"  # Path to the PKCS#12 file containing the certificate and private key
# pfx_data = open("../PKS#12/certificate.pfx", "rb").read()  # PKCS#12 binary data
# pfx_password = b"password"  # Password for the PKCS#12 file
# #pfx_password_bytes = pfx_password.encode()  # Convert string to bytes
# #sign_pdf(input_pdf, output_pdf, signature_field_name, pfx_data, pfx_password_bytes)
# import fitz  # PyMuPDF
# from PIL import Image
# import io

# def sign_pdf(input_pdf_path, output_pdf_path, signature_image_path):
#     # Open the input PDF
#     pdf = fitz.open(input_pdf_path)

#     # Open the signature image
#     signature_img = Image.open(signature_image_path)

#     # Convert the signature image to bytes
#     img_bytes = io.BytesIO()
#     signature_img.save(img_bytes, format='PNG')
#     img_bytes.seek(0)

#     # Get the first page of the PDF
#     page = pdf[0]

#     # Get the size of the page
#     page_rect = page.rect

#     # Add the signature image as an overlay
#     page.insert_image(page_rect, stream=img_bytes.read(), overlay=True)

#     # Save the modified PDF
#     pdf.save(output_pdf_path)

#     # Close the PDFs
#     pdf.close()
#     img_bytes.close()

# # Example usage
# input_pdf = "pdf.pdf"
# output_pdf = "signed_output.pdf"
# signature_image = "sign.jpg"
# # sign_pdf(input_pdf, output_pdf, signature_image)

# import PyPDF2

# def is_signed(pdf_path):
#     # Open the PDF file
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
        
#         # Check if any page has a signature field
#         for page in reader.pages:
#             if '/Annots' in page:
#                 annots = page['/Annots']
#                 if annots and isinstance(annots, PyPDF2.generic.ArrayObject):
#                     for annot in annots:
#                         if isinstance(annot, PyPDF2.generic.DictionaryObject):
#                             if annot.get('/FT') == '/Sig':
#                                 return True
#     return False

# # # Usage
# # pdf_path = "pdf.pdf"
# # if is_signed(pdf_path):
# #     print("The PDF is signed.")
# # else:
# #     print("The PDF is not signed.")

# import fitz  # PyMuPDF

# def compare_pdf_texts(pdf1_path, pdf2_path):
#     pdf1 = fitz.open(pdf1_path)
#     pdf2 = fitz.open(pdf2_path)

#     diff_found = False

#     for page_num in range(min(len(pdf1), len(pdf2))):
#         page1_text = pdf1[page_num].get_text()
#         page2_text = pdf2[page_num].get_text()

#         if page1_text != page2_text:
#             print(f"Differences found on page {page_num + 1}:")
#             # Perform more detailed text comparison if needed
#             diff_found = True

#     if not diff_found:
#         print("No differences found.")

#     pdf1.close()
#     pdf2.close()

# # Example usage
# pdf1_path = "pdf.pdf"
# pdf2_path = "signed.pdf"

# #import fitz  # PyMuPDF

# def compare_pdfs(pdf1_path, pdf2_path):
#     # Open the PDF files
#     pdf1 = fitz.open(pdf1_path)
#     pdf2 = fitz.open(pdf2_path)

#     # Initialize a variable to store the comparison result
#     are_equal = True

#     # Iterate through each page of both PDFs
#     for page_number in range(min(len(pdf1), len(pdf2))):
#         # Extract text from each page of both PDFs
#         text1 = pdf1[page_number].get_text()
#         text2 = pdf2[page_number].get_text()

#         # Compare the text from both PDFs
#         if text1 != text2:
#             are_equal = False
#             print(f"Page {page_number + 1} is different")

#     # Close the PDF files
#     pdf1.close()
#     pdf2.close()

#     # Print the overall comparison result
#     if are_equal:
#         print("Both PDFs are identical")
#     else:
#         print("PDFs are different")


# # Example usage
# pdf1_path = "myfile.pdf"
# pdf2_path = "pdf.pdf"
# #compare_pdfs(pdf1_path, pdf2_path)

# import fitz  # PyMuPDF

# def scan_pdf(pdf_path):
#     # Open the PDF file
#     pdf = fitz.open(pdf_path)

#     # Initialize an empty string to store the scanned text
#     scanned_text = ""

#     # Iterate through each page of the PDF
#     for page_number in range(len(pdf)):
#         # Get the text from the current page
#         page = pdf.load_page(page_number)
#         text = page.get_text()

#         # Append the text from the current page to the scanned_text string
#         scanned_text += text

#     # Close the PDF file
#     pdf.close()

#     # Print or return the scanned text
#     return scanned_text

# # Usage
# pdf_path = "myfile.pdf"
# # scanned_text = scan_pdf(pdf_path)
# # print(scanned_text)

# #excelToPdf()
# #pdfToExcel()
# # csvToPdf()
# #pdfToPpt()

# import os

# import fitz

# def pdf_to_images_and_zip(pdf_path, image_folder):
#     # Open the PDF
#     pdf_document = fitz.open(pdf_path)
    
#     # Create the image folder if it doesn't exist
#     os.makedirs(image_folder, exist_ok=True)

#     for page_number in range(len(pdf_document)):
#         # Get the page
#         page = pdf_document.load_page(page_number)
        
#         # Convert the page to a pixmap
#         pixmap = page.get_pixmap()
        
#         # Save the pixmap as an image
#         image_path = f"{image_folder}/page_{page_number + 1}.png"  # Save as PNG format
#         pixmap.save(image_path)
        
#         print(f"Page {page_number + 1} saved as {image_path}")
    
#     # Close the PDF
#     pdf_document.close()
    
#     # Create a zip file
#     zip_file_path = f"{image_folder}.zip"
#     with zipfile.ZipFile(zip_file_path, 'w') as zipf:
#         # Add all files in the image folder to the zip file
#         for root, _, files in os.walk(image_folder):
#             for file in files:
#                 zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), image_folder))

#     print(f"Images zipped and saved as {zip_file_path}")

# # Usage
# pdf_path = "myfile.pdf"  # Path to your PDF file
# image_folder = "images"  # Folder where the images will be saved
# #pdf_to_images_and_zip(pdf_path, image_folder)

# import PyPDF2
# from pptx import Presentation
# from pptx.util import Inches,Pt
# from pptx.dml.color import RGBColor
# from pptx.enum.text import PP_ALIGN

# def pdf_to_pptx(pdf_file,ppt_file):
#     ppt = Presentation()

#     slide_layout = ppt.slide_layouts[5]
#     reader = PyPDF2.PdfReader(pdf_file)
#     for page_number in range(len(reader.pages)):
#         slide = ppt.slides.add_slide(slide_layout)
#         page = reader.pages[page_number]
#         text = page.extract_text()

#         left = Inches(0.5)
#         top = Inches(0.5)
#         width = Inches(8)
#         height = Inches(5)

#         text_box = slide.shapes.add_textbox(left,top,width,height)
#         text_frame = text_box.text_frame
#         p = text_frame.add_paragraph()
#         p.alignment= PP_ALIGN.CENTER

#         run = p.add_run()
#         run.text = text
#         fonts = run.font
#         fonts.name = 'Times New Roman'
#         fonts.size = Pt(12)
#         fonts.color.rgb = RGBColor(0,0,0)
#         text_box.fill.solid()
#         text_box.fill.fore_color.rgb = RGBColor(255,255,255)
    
#     ppt.save(ppt_file)
#     print(f'Pdf converted to PPTX: {ppt_file}')


# # Usage
# pdf_path = "myfile.pdf"  # Path to the input PowerPoint presentation
# ppt_path = "myfile_new.pptx"  # Path to save the output PDF file
# # pdf_to_pptx(pdf_path, ppt_path)

# from pptx import Presentation
# from fpdf import FPDF

# def convert_ppt_to_pdf(ppt_file, pdf_file):
#     # Load the PowerPoint presentation
#     prs = Presentation(ppt_file)
    
#     # Initialize the PDF object
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
    
#     # Specify the path to the DejaVuSans font file
#     font_path = "dejavu-sans/DejaVuSans.ttf"  # Replace with the correct path to the font file
    
#     # Add the font to the PDF object
#     pdf.add_font("DejaVuSans", "", font_path, uni=True)
#     pdf.set_font("DejaVuSans", size=12)
    
#     # Iterate through each slide in the presentation
#     for slide in prs.slides:
#         # Iterate through each shape in the slide
#         for shape in slide.shapes:
#             if hasattr(shape, "text"):
#                 # If the shape is a text box, extract its text and add it to the PDF
#                 text = shape.text
#                 # Add the text to the PDF
#                 pdf.multi_cell(0, 10, text=text, border=0, align='C')
#                 pdf.ln()  # Move to the next line
        
#         # Add a page break after each slide
#         pdf.add_page()
    
#     # Save the PDF file
#     pdf.output(pdf_file)

# # Usage
# ppt_path = "myfile.pptx"  # Path to the input PowerPoint presentation
# pdf_path = "myfile_ppt.pdf"   # Path to save the output PDF file
# #convert_ppt_to_pdf(ppt_path, pdf_path)

# def excelToPdf(excel,pdf):

#     df = pd.read_excel(excel)
#     doc = SimpleDocTemplate(pdf, pagesize=letter)
#     data = [df.columns.tolist()] + df.values.tolist()
#     # Convert DataFrame to list of lists for Table creation
#     data = [df.columns.tolist()] + df.values.tolist()

#     # Create Table object
#     table = Table(data)

#     # Add table to PDF document
#     return doc.build([table])

# #Usage
# inputFile = "file_example_XLSX_5000_Qf8SSZv.xlsx"
# outputFile = "excelToPDF.pdf"
# #excelToPdf(inputFile, outputFile)
# #excelToPdf()
# from docx import Document
# from fpdf import FPDF

# def convert_docx_to_pdfs(docx_file, pdf_file):
#     # Load the Word document
#     doc = Document(docx_file)

#     # Initialize the PDF object
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # Specify the path to the DejaVuSans font file
#     font_path = "dejavu-sans/DejaVuSans.ttf"  # Replace with the correct path to the font file
    
#     # Add the font to the PDF object
#     pdf.add_font("DejaVuSans", "", font_path, uni=True)
#     pdf.set_font("DejaVuSans", size=12)
#      # Extract text from each paragraph in the DOCX file and add it to the PDF
#     for para in doc.paragraphs:
#         pdf.cell(200, 10, txt=para.text, ln=True)

#     # Save the PDF file
#     pdf.output(pdf_file)

#     # # Iterate through each paragraph in the Word document
#     # for paragraph in doc.paragraphs:
#     #     # Add each paragraph as a new cell in the PDF
#     #     #pdf.set_font("Arial", size=12)
#     #     pdf.multi_cell(0, 10, txt=paragraph.text, border=0, align='L')
#     #     pdf.ln()  # Move to the next line

#     # # Save the PDF file
#     # pdf.output(pdf_file)

# from docx2pdf import convert

# def doctopdf(docx_file, pdf_file):
#     # Convert DOCX to PDF
#     convert(docx_file, pdf_file)

# # Usage
# inputFile = "word.docx"
# outputFile = "w_To_pdf.pdf"
# #doctopdf(inputFile, outputFile)


# import os
# from pptx import Presentation
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate

# def convert_ppt_to_pdf(ppt_file, pdf_file):
#     if not os.path.exists(ppt_file):
#         raise FileNotFoundError(f"PowerPoint file '{ppt_file}' not found.")

#     prs = Presentation(ppt_file)
#     pdf = SimpleDocTemplate(pdf_file, pagesize=letter)

#     for slide in prs.slides:
#         for shape in slide.shapes:
#             if hasattr(shape, "text"):
#                 pdf.add_paragraph(shape.text)

#         pdf.add_page()

#     pdf.build()

# # Example usage:
# #convert_ppt_to_pdf("pptfile.pptx", "output_pptx.pdf")

# print('hello')

import os
import subprocess

def convert_to_pdf(input_file):
    output_file = os.path.splitext(input_file)[0] + '.pdf'
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--invisible', '--convert-to', 'pdf', input_file, output_file])
    # return output_file

def convert_to_docx(input_file):
    output_file = os.path.splitext(input_file)[0] + '.docx'
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--invisible', '--convert-to', 'docx', input_file])
    return output_file

# Example usage:
# pdf_file = convert_to_pdf('word.pdf')
# print(f'PDF file generated: {pdf_file}')

import os
import subprocess

def convert_to_pdf(input_file):
    output_file = os.path.splitext(input_file)[0] + '.pdf'
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--invisible', '--convert-to', 'pdf', input_file])
    return output_file

def convert_to_ppt(input_file):
    output_file = os.path.splitext(input_file)[0] + '.ppt'
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--invisible', '--convert-to', 'ppt', input_file])
    return output_file

# Example usage:
# pdf_file = convert_to_pdf('pptfile.pptx')
# print(f'PDF file generated: {pdf_file}')

# ppt_file = convert_to_ppt('pptpdf.pdf')
# print(f'PPT file generated: {ppt_file}')

import os
import subprocess

def convert_to_pdf(input_file):
    output_file = os.path.splitext(input_file)[0] + '.pdf'
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--invisible', '--convert-to', 'pdf', input_file])
    return output_file

def convert_to_excel(input_file):
    output_file = os.path.splitext(input_file)[0] + '.xlsx'
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice', '--headless', '--invisible', '--convert-to', 'xlsx', input_file])
    return output_file

# Example usage:
# pdf_file = convert_to_pdf('file_example_XLSX_5000_Qf8SSZv.xlsx')
# print(f'PDF file generated: {pdf_file}')

# excel_file = convert_to_excel('pdfxlsx.pdf')
# print(f'Excel file generated: {excel_file}')

import subprocess

def convert_pdf_to_pptx(pdf_file):
    subprocess.run(['pdf2pptx', pdf_file])

# Example usage:
# pdf_file = 'pptpdf.pdf'
# convert_pdf_to_pptx(pdf_file)

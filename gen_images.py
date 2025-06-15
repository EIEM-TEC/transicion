from pdf2image import convert_from_path
# Path to the uploaded PDF file
año = "2025"
pdf_path = f"./malla_EM_{año}.pdf"


images = convert_from_path(pdf_path, dpi=900, first_page=1, last_page=4)

# Save images as PNG files
image_paths = []
for i, image in enumerate(images):
    image_path = f"./malla_EM_{año}{i+1}.jpg"
    image.save(image_path, "JPEG")
    image_paths.append(image_path)
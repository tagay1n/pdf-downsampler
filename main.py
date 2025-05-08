import os
import fitz  # PyMuPDF
from PIL import Image
import io
import pymupdf
from rich.progress import track


def _convert(input_path, output_path, zoom=0.75, quality=60):
    with pymupdf.open(input_path) as input_pdf, pymupdf.open() as output_pdf:
        for page in input_pdf.pages():
            pix = page.get_pixmap(dpi=int(300 * zoom))
            
            # Convert pixmap to PIL image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Compress image using JPEG
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="JPEG", quality=quality)
            img_bytes.seek(0)
            
            # Create a new page with same size and insert compressed image
            rect = pymupdf.Rect(0, 0, pix.width, pix.height)
            new_page = output_pdf.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(rect, stream=img_bytes)
            
        output_pdf.save(output_path, garbage=4, deflate=True, deflate_images=True)
        
        input_size_bytes = os.stat(input_path).st_size
        input_size_mbytes = round(input_size_bytes  / (1024 * 1024), 1)
        output_size_bytes = os.stat(output_path).st_size
        output_size_mbytes = round(output_size_bytes  / (1024 * 1024), 1)
        compression = round((input_size_bytes / output_size_bytes), 2)
        print(f"original size: {input_size_mbytes}, result size: {output_size_mbytes}, compression ratio: {compression}, file: {os.path.basename(input_path)}")
        os.remove(input_path)       
             
def main(input = 'input', output = 'output'):
    os.makedirs(input, exist_ok=True) 
    os.makedirs(output, exist_ok=True)
    for f_path in track(os.listdir(input), "Converting books"):
        input_path = os.path.join(input, f_path)
        output_path = os.path.join(output, f_path)
        _convert(input_path, output_path)
    
if __name__ == '__main__':
    main()
    
    
    
# 📉 pdf-downsampler

**Compress high-resolution scanned PDFs into smaller, OCR-ready files using Python.**

This tool uses [PyMuPDF](https://github.com/pymupdf/PyMuPDF) and [Pillow](https://python-pillow.org/) to rasterize, resize, and recompress image-based PDFs, reducing file size while keeping enough quality for OCR or archive.

⚠️ Notes
- This tool rasterizes pages, so text and vector layers are removed.
- It's best suited for scanned image PDFs, not text-based documents.
- Use zoom to control resolution (e.g. 0.5 for 150 DPI from 300 DPI).
- Output is ready for OCR via tools like Tesseract or OCRmyPDF.

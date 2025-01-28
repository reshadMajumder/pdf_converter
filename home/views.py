from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image as PilImage
from io import BytesIO

def convert_to_pdf(images):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    for img in images:
        try:
            if img is None:
                print("Skipping NoneType image")
                continue

            pil_img = PilImage.open(img)
            image_width, image_height = pil_img.size
            if image_width > width or image_height > height:
                pil_img.thumbnail((width, height))
            pdf.drawInlineImage(pil_img, 0, 0, width=width, height=height)
            pdf.showPage()
        except Exception as e:
            print(f"Error processing image: {e}")
        finally:
            if pil_img:
                pil_img.close()  
    pdf.save()
    buffer.seek(0)
    return buffer





def upload_images(request):
    if request.method == 'POST' and request.FILES.getlist('image'):
        images = request.FILES.getlist('image')
        pdf_buffer = convert_to_pdf(images)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        return response
    return render(request, 'upload_image.html')

from django.shortcuts import  get_object_or_404, render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime
from .models import Profile
from django.views.generic import ListView


# Create your views here.
def index(request):
    """
    Render the index page of the PDF application.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered index page.
    """
    return render(request, "index.html")


def generate_pdf(request):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="example.pdf"'

    c = canvas.Canvas(response)

    # Title

    c.setFont("Helvetica", 24)
    c.drawString(200, 800, "Hello, PDF World!")

    # TimeStamp
    c.setFont("Helvetica", 12)
    c.drawString(
        100, 780, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Example Text
    c.setFont("Helvetica", 8)
    c.drawString(100, 750, "This is an example PDF generated using ReportLab.")
    c.drawString(100, 730, "You can add more contents as needed.")

    # Finalize the PDF
    c.showPage()
    c.save()

    return response



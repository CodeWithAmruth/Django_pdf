from django.shortcuts import  get_object_or_404, render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime
from django.views.generic import ListView

from pdf_app.models import Profile


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

class ProfileListView(ListView):
    model = Profile
    template_name = 'pdf_app/profile_list.html'
    context_object_name = 'profile_list'

def generate_profile_pdf(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{profile.name}.pdf"'
    
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    p.drawString(50, 750, f"Report for {profile.name}")

    p.setFont("Helvetica", 8)

    p.drawString(100, 730, "first name: " + profile.name)
    p.drawString(100, 710, "age: " + str(profile.age))
    p.drawString(100, 690, "gender: " + profile.gender)
    p.drawString(100, 670, "address: " + profile.address)
    p.drawString(100, 650, "email: " + profile.email)
    
    p.showPage()
    p.save()

    return response
    
    
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


# Create a view for the profile list page.
class ProfileListView(ListView):
    model = Profile 
    template_name = "pdf_app/profile_list.html"
    context_object_name = "profile_list"

def generate_profile_pdf(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{profile.name}_profile.pdf"'

    c = canvas.Canvas(response)

    # Title

    c.setFont("Helvetica", 24)  
    c.drawString(200, 800, f"{profile.name}'s Profile")

    # Content
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"Name: {profile.name}")
    c.drawString(100, 760, f"Email: {profile.email}")   
    c.drawString(100, 740, f"Age: {profile.age}")
    c.drawString(100,720,f"Bio : {profile.bio}")

    # TimeStamp
    c.setFont("Helvetica", 12)
    c.drawString(
        100, 700, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Finalize the PDF
    c.showPage()
    c.save()
    return response

    
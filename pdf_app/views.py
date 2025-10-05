from django.shortcuts import  get_object_or_404, render
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime
from django.views.generic import ListView
from weasyprint import HTML
from django.template.loader import render_to_string
from pdf_app.models import Profile
import plutoprint
import tempfile


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
    
def generate_all_profiles_pdf(request):
    profiles = Profile.objects.all()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="all_profiles.pdf"'

    p = canvas.Canvas(response)

    y = 750

    p.setFont("Helvetica", 16)
    p.drawString(50, 800, "All Profiles Report")
    p.setFont("Helvetica", 8)
    p.drawString(100, 780, "Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    for index, profile in enumerate(profiles):

        if index >0 and y < 150:
            p.showPage()
            y = 750
            p.setFont("Helvetica", 12)

        p.setFont("Helvetica", 12)
        p.drawString(50, y, f"Profile: {index+1}:{profile.name}")
        y -= 20

        p.setFont("Helvetica", 10)
        p.drawString(50,y,f"Name:{profile.name}")
        y-=15
        p.drawString(50,y,f"Age:{profile.age}")
        y-=15
        p.drawString(50,y,f"Gender:{profile.gender}")
        y-=15
        p.drawString(50,y,f"Address:{profile.address}")
        y-=15
        p.drawString(50,y,f"Email:{profile.email}")
        y-=30

    p.showPage()
    p.save()

    return response

def generate_single_profile_pdf(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    html_string = render_to_string('weasyprint/single_profile_pdf.html', {'profile': profile, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{profile.name}.pdf"'

    HTML(string=html_string).write_pdf(response)

    return response

def generate_all_profiles_pdf(request):
    profiles = Profile.objects.all()

    html_string = render_to_string('weasyprint/all_profiles.pdf.html', {'profiles': profiles, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="all_profiles.pdf"'

    HTML(string=html_string).write_pdf(response)

    return response

# Pluto print

def generate_profile_output(request,pk,output_format = "pdf"):
    profile = get_object_or_404(Profile, pk=pk)

    # render to html
    html_string = render_to_string('weasyprint/single_profile_pdf.html', {'profile': profile, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    # create book 
    book = plutoprint.Book(plutoprint.PAGE_SIZE_A4)
    book.load_html(html_string)

    # create the temp file
    with tempfile.NamedTemporaryFile(suffix=f".{output_format},delete = False") as tmpfile:
        filepath = tmpfile.name

    # write output to file
    if output_format == "pdf":
        book.write_to_pdf(filepath)
        content_type = "application/pdf"
    else:
        book.write_to_png(filepath,width=800)
        content_type = "image/png"

    # Read back the file
    with open(filepath, "rb") as f:
        file_data = f.read()

    # Build the response
    response = HttpResponse(file_data, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{profile.name}.{output_format}"'

    return response

def generate_all_profiles_output(request,output_format = "pdf"):
    profiles = Profile.objects.all()

    # Combine all profiles HTML into one doc

    combined_html = ""
    for idx, profile in enumerate(profiles):
        html_string = render_to_string('weasyprint/single_profile_pdf.html', {'profile': profile, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        # Add page break after each profile
        if idx < len(profiles)-1:
            combined_html += html_string + "<div style='page-break-after: always;'></div>"
        else:
            combined_html += html_string

    # create book
    book = plutoprint.Book(plutoprint.PAGE_SIZE_A4)
    book.load_html(combined_html)

    # create the temp file
    with tempfile.NamedTemporaryFile(suffix=f".{output_format},delete = False") as tmpfile:
        filepath = tmpfile.name

    # write output to file
    if output_format == "pdf":
        book.write_to_pdf(filepath)
        content_type = "application/pdf"
    else:
        book.write_to_png(filepath,width=800)
        content_type = "image/png"

    # Read back the file
    with open(filepath, "rb") as f:
        file_data = f.read()

    # Build the response
    response = HttpResponse(file_data, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="all_profiles.{output_format}"'

    return response
from django.contrib import admin

from pdf_app.models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'address', 'email')
from django.contrib import admin
from .models import ReceiptFile



@admin.register(ReceiptFile)
class ReceiptFileAdmin(admin.ModelAdmin):
    list_display = ("id", 'file', 'uploaded_at', 'converted_csv')




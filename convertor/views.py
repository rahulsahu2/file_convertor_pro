# views.py

from django.shortcuts import render, redirect
from .forms import ReceiptFileForm
from .models import ReceiptFile

def upload_receipt_file(request):
    if request.method == 'POST':
        form = ReceiptFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # You can perform additional actions here if needed
            receipt_files = ReceiptFile.objects.all()
            print(receipt_files.first().converted_csv)
            return render(request, 'convert.html', {'form': form, 'receipt_files': receipt_files})
    else:
        form = ReceiptFileForm()
    receipt_files = ReceiptFile.objects.all()
    print(receipt_files.first().converted_csv)
    return render(request, 'convert.html', {'form': form, 'receipt_files': receipt_files})

def success_page(request):
    receipt_files = ReceiptFile.objects.all()
    return render(request, 'success_page.html', {'receipt_files': receipt_files})
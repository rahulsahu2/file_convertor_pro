from django.urls import path
from .views import upload_receipt_file, success_page

urlpatterns = [
    path("upload/", upload_receipt_file, name="convert"),
     path('success/', success_page, name='success_page'),
]
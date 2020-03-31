from django.urls import path

from . import views

urlpatterns = [
    path('transcribe', views.viewIndex, name ="transcribe"),
    path('transcribe/save', views.saveTranscribe, name ="save_transcribe")
    ]

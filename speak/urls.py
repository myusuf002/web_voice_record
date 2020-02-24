from django.urls import path

from . import views

urlpatterns = [
    path('', views.viewIndex, name ="speak"),
    path('record', views.viewRecord, name ="record"),
    path('record/save', views.saveRecord, name ="save_record"),
    path('record/done', views.doneRecord, name ="done_record"),
    ]

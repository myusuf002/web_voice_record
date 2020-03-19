from random import randint

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms

from .models import Utterance, Gender, Age, Ethnic, Dialect
from .forms import speakForm

# Create your views here.

def viewIndex(request):  
    if 'response' in request.session: del request.session['response']
    if 'recorded' in request.session: del request.session['recorded']
    request.session['count_record'] = 0
    
    form = speakForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session['response'] = form.cleaned_data
            return redirect('record')
        
    context = {
        'title': "Speak",
        'page': "speak",
        'form': form
    }
    return render(request, 'speak/index.html', context)

def viewRecord(request):
    if 'response' in request.session:
        utterance = Utterance.objects.filter(active=True).order_by('count').first()
        # utterance = Utterance.objects.filter(active=True).order_by('count')[:4]
        context = {
            'title': "Record",
            'page': "speak",
            'count_record': request.session['count_record'],
            'response': request.session['response'],
            'utterance': utterance #[randint(0, len(Utterances)-1)]
        }
        return render(request, 'speak/record.html', context)
    else: return redirect('speak')

def saveRecord(request):
    request.session['recorded'] = 1
    request.session['count_record'] += 1
    print("... save record ...")
    audio_data = request.FILES['audio']
    audio_name = request.POST['name']
    
    default_storage.save('audio/'+audio_name, ContentFile(audio_data.read()))
    
    if Utterance.objects.filter(code=request.POST['utterance']).exists():
        print('Utterance exist!')
        utterance = Utterance.objects.get(code=request.POST['utterance'])
        utterance.count += 1
        utterance.save()

    data = {
        'name': request.POST['name'],
        'utterance': request.POST['utterance'],
        'genders': request.POST['gender'],
        'age': request.POST['age'],
        'ethnic': request.POST['ethnic'],
        'dialect': request.POST['dialect'],
        'status': "saved"
    }
    return JsonResponse(data)

def doneRecord(request):
    if Gender.objects.filter(category=request.POST['gender']).exists():
        print('Gender exist!')
        gender = Gender.objects.get(category=request.POST['gender'])
        gender.count += 1
        gender.save()
    
    if Age.objects.filter(category=request.POST['age']).exists():
        print('Age exist!')
        age = Age.objects.get(category=request.POST['age'])
        age.count += 1
        age.save()

    if Ethnic.objects.filter(category=request.POST['ethnic']).exists():
        print('Ethnic exist!')
        ethnic = Ethnic.objects.get(category=request.POST['ethnic'])
        ethnic.count += 1
        ethnic.save()

    if Dialect.objects.filter(category=request.POST['dialect']).exists():
        print('Dialect exist!')
        dialect = Dialect.objects.get(category=request.POST['dialect'])
        dialect.count += 1
        dialect.save()

    del request.session['count_record']
    del request.session['response']
    del request.session['recorded']
    return redirect('speak')

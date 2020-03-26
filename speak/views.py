import os
from random import randint
from django.conf import settings
from django.core.files import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django import forms

from .models import Record, Configuration, Utterance, Gender, Age, Ethnic, Dialect
from .forms import speakForm

if Configuration.objects.filter(code='min_record').exists(): 
    conf_min = Configuration.objects.filter(code='min_record').first()
    min_record = int(conf_min.text)
else: min_record = 10

if Configuration.objects.filter(code='instructions').exists(): 
    conf_ins = Configuration.objects.filter(code='instructions').first()
    instructions = conf_ins.text
else: instructions = "Nothing Here"

# Create your views here.
def viewIndex(request):  
    if 'response' in request.session: del request.session['response']
    if 'recorded' in request.session: del request.session['recorded']
    request.session['count_record'] = 0
    
    form = speakForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            request.session['response'] = form.cleaned_data
            return redirect('instructions')
        
    context = {
        'title': "Speak",
        'page': "speak",
        'instructions': instructions,
        'form': form
    }
    return render(request, 'speak/index.html', context)

def viewInstructions(request):     
    context = {
        'title': "Speak",
        'page': "speak",
        'instructions': instructions,
    }
    return render(request, 'speak/instructions.html', context)

def viewRecord(request):
    if 'response' in request.session:
        utterance = Utterance.objects.filter(active=True).order_by('count').first()
        # utterance = Utterance.objects.filter(active=True).order_by('count')[:4]
        context = {
            'title': "Record",
            'page': "speak",
            'min_record': min_record,
            'instructions': instructions,
            'count_record': request.session['count_record'],
            'recorded': 'recorded' in request.session,
            'response': request.session['response'],
            'utterance': utterance #[randint(0, len(Utterances)-1)]
        }
        return render(request, 'speak/record.html', context)
    else: return redirect('speak')

def saveRecord(request):
    if 'response' in request.session:
        request.session['recorded'] = 1
        request.session['count_record'] += 1
        print("... save record ...")
        audio_data = request.FILES['audio']
        audio_name = request.POST['name']
        
        record = Record(code=audio_name,
                        utterance=request.POST['utterance'],
                        gender=request.POST['gender'],
                        age=request.POST['age'],
                        ethnic=request.POST['ethnic'],
                        dialect=request.POST['dialect'],
                        audio=File(audio_data),
                        count_good=0, count_bad=0)
        record.audio.name = audio_name
        record.save()
            
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
    else: return redirect('speak')
    
def doneRecord(request):
    if 'response' in request.session:
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
        context = {
            'title': "Thanks",
            'page': "speak",
            'instructions': instructions,
        }
        return render(request, 'speak/thanks.html', context)

    else: return redirect('speak')

@login_required
def viewAudio(request):    
    records = Record.objects.order_by('id')
    page = request.GET.get('page', 1)

    paginator = Paginator(records, 6)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)  
    context = {
        'title': "Speak",
        'page': "speak",
        'records': records
    }
    return render(request, 'speak/audio.html', context)

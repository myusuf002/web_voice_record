import os
from django.shortcuts import render
from django.conf import settings

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.http import HttpResponse, JsonResponse

from .audio import convert_audio, info_audio
from .models import Language
from timeit import default_timer as timer
import scipy.io.wavfile as wav

import deepspeech


ds_models = {}
# ds_models['id-ID'] = deepspeech.Model(settings.MEDIA_ROOT+'/model/output_graph.pbmm', 500)
# ds_models['id-ID'].enableDecoderWithLM(settings.MEDIA_ROOT+'/lm/lm.binary', settings.MEDIA_ROOT+'/trie/trie', 1.50, 2.10)

# Create your views here.

def viewIndex(request):         
    languages = Language.objects.filter(active=True)

    context = {
        'title': "Transcribe",
        'page': "transcribe",
        'languages': languages
    }
    return render(request, 'transcribe/index.html', context)

def saveTranscribe(request):
    print("... save record ...")
    audio_lang = request.POST['lang']
    audio_data = request.FILES['audio']
    audio_name = request.POST['name']
    audio_rate = int(request.POST['rate'])
    default_storage.save('transcribe/'+audio_name, ContentFile(audio_data.read()))
    info_audio(settings.MEDIA_ROOT+'/transcribe/'+audio_name)
    
    lang = Language.objects.filter(code=audio_lang, active=True).first()
    model_load_start = timer()
    model = deepspeech.Model(settings.BASE_DIR+lang.model.url, lang.beam_width)
    model_load_end = timer() - model_load_start
    print('Loaded model in %0.3fs.' % (model_load_end))
    if(lang.lm and lang.trie):
        lm_load_start = timer()
        model.enableDecoderWithLM(settings.BASE_DIR+lang.lm.url, settings.BASE_DIR+lang.trie.url, lang.lm_alpha, lang.lm_beta)
        lm_load_end = timer() - lm_load_start
        print('Loaded language model in %0.3fs.' % (lm_load_end))

    # Preprocessing
    if(model.sampleRate() != audio_rate):
        print("... preprocessing ...")
        convert_audio(settings.MEDIA_ROOT+'/transcribe/'+audio_name, audio_name)
        default_storage.delete('transcribe/'+audio_name)
        info_audio(audio_name)
        print()
    
    # Transcribing 
    print("... transcribing ...")
    if(model.sampleRate() != audio_rate):
        fs, audio = wav.read(audio_name)
    else:
        fs, audio = wav.read(settings.MEDIA_ROOT+'/transcribe/'+audio_name)
    
    audio_length = len(audio) * ( 1 / 16000)

    print('Running inference.')
    inference_start = timer()
    audio_text = model.stt(audio)
    print('audio:', audio_name)
    print('rate :', audio_rate)
    print('lang :', audio_lang)
    print('text :', audio_text)
    inference_end = timer() - inference_start
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))
    
    print()
    print("... clean record ...")
    
    if(model.sampleRate() != audio_rate):
        os.remove(audio_name)
    
    data = {
        'name': audio_name,
        'language': audio_lang,
        'transcribe': audio_text+' ',
        'length': audio_length,
        'time': inference_end,
        'status': "saved"
    }
    return JsonResponse(data)


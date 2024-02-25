from django.shortcuts import render
from Deepgram import STT

def index(request):
    output_data = STT()
    context = {'output': output_data}
    return render(request, 'myapp/index.html', context)

from django.shortcuts import render
from .Deepgram import STT  # Import your function

def basic(request):
    output_data = STT()
    context = {'output': output_data}
    return render(request, 'basic.html', context)
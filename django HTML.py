from django.shortcuts import render
from .utils import generate_program_output  # Import your function

def index(request):
    output_data = generate_program_output()
    context = {'output': output_data}
    return render(request, 'myapp/index.html', context)

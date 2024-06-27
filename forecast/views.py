from django.shortcuts import render

# forecast homepage view
def home(request):
    return render(request, 'forecast/index.html')

from django.shortcuts import render

# forecast homepage view
def home(request):
    # return render(request, 'forecast/home.html')
    return render(request, 'base.html')

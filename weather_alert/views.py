from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WeatherAlertForm, WeatherAlertFileForm
from .models import WeatherAlert, WeatherAlertFile, AlertSubscription
from community.models import Region


# List of counties in Kenya
counties = [
    "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo-Marakwet",
    "Embu", "Garissa", "Homa Bay", "Isiolo", "Kajiado",
    "Kakamega", "Kericho", "Kiambu", "Kilifi", "Kirinyaga",
    "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia",
    "Lamu", "Machakos", "Makueni", "Mandera", "Marsabit",
    "Meru", "Migori", "Mombasa", "Murang'a", "Nairobi",
    "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua",
    "Nyeri", "Samburu", "Siaya", "Taita-Taveta", "Tana River",
    "Tharaka-Nithi", "Trans Nzoia", "Turkana", "Uasin Gishu", "Vihiga",
    "Wajir", "West Pokot"
]

# weather alert view
@login_required
def add_alert(request):
    form = WeatherAlertForm()
    region_choice = counties

    if request.method == 'POST':
        title = request.POST.get('title')
        region_name = request.POST.get('region').capitalize()
        description = request.POST.get('description')
        posted_by = request.user
        file = request.FILES.get('file')

        region, created = Region.objects.get_or_create(name=region_name)
        if file:
            new_file = WeatherAlertFile.objects.create(
                file=file
            )

        new_alert = WeatherAlert.objects.create(
            title=title,
            region=region,
            description=description,
            media=new_file,
            posted_by=posted_by
        )

        messages.success(request, 'Alert added successfully')
        return redirect('weather-alert')
    else:
        form = WeatherAlertForm()

    alerts = WeatherAlert.objects.all()
    context = {
        'form': form,
        'alerts': alerts,
        'region_choice': region_choice
    }
    return render(request, 'weather_alert/weather_alert.html', context)


# Manage weather alerts Subscription
@login_required
def manage_subscription(request):
    user_subscripiton, created = AlertSubscription.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        reg_selected = request.POST.getlist('regions').capitalize()
        region_obj = []

        for region in reg_selected:
            region, created = Region.objects.get_or_create(name=region)
            region_obj.append(region)

        user_subscripiton.regions.set(region_obj)
        messages.success(request, 'Subscription updated successfully')
        return redirect('profile')

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Region, Forum, Media, Message
from .forms import CreateForumForm
from weather_alert.models import WeatherAlert

# Community home view
@login_required
def community_home(request):
    form = CreateForumForm()
    # regions = Region.objects.all()
    # forums = Forum.objects.all()
    q = request.GET.get('q') if request.GET.get('q') else ''
    regions = Region.objects.filter(name__icontains=q)
    forums = Forum.objects.filter(
        Q(region__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    weather_alerts = WeatherAlert.objects.all()
    context = {
        'regions': regions,
        'forums': forums,
        'weather_alerts': weather_alerts,
        'form': form,
    }

    return render(request, 'community/index.html', context)

# Create forum view
@login_required
def create_forum(request):
    form = CreateForumForm()
    regions = Region.objects.all()
    
    if request.method == 'POST':
        region_name = request.POST.get('region').capitalize()
        region, created = Region.objects.get_or_create(name=region_name)

        new_forum = Forum.objects.create(
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            region = region,
            owner = request.user,
        )
        new_forum.members.add(request.user)
        return redirect('community-home')

    context = {
        'regions': regions,
        'form': form,
    }
    return redirect('community-home', context)


# forum view
@login_required
def forum(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    region = forum.region
    region_forums = Forum.objects.filter(region=region)
    forum_messages = Message.objects.filter(forum=forum)
    context = {
        'forum': forum,
        'region_forums': region_forums,
        'forum_messages': forum_messages,
    }
    return render(request, 'community/forum.html', context)

# Handle media upload from websocket
@login_required
def upload_media(request):
    if request.method == 'POST':
        media = Media(file=request.FILES['file'])
        media.save()
        return JsonResponse({'media_url': media.file.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Region, Forum
from .forms import CreateForumForm

# Community home view
@login_required
def community_home(request):
    form = CreateForumForm()
    regions = Region.objects.all()
    forums = Forum.objects.all()
    context = {
        'regions': regions,
        'forums': forums,
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
def forum(request):
    return render(request, 'community/forum.html')
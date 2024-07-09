from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Region, Forum

# Community home view
@login_required
def community_home(request):
    regions = Region.objects.all()
    forums = Forum.objects.all()
    context = {
        'regions': regions,
        'forums': forums
    }

    return render(request, 'community/index.html', context)

# forum view
def forum(request):
    return render(request, 'community/forum.html')
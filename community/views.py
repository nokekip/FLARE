from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Community home view
@login_required
def community_home(request):
    return render(request, 'community/index.html')


from django.shortcuts import render
from user.models import Request
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    user_requests = Request.objects.filter(user=request.user).order_by('-created_at')[:4]

    return render(request, 'main/index.html', {'completed_requests': user_requests})
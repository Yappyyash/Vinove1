from django.shortcuts import render, redirect
from django.http import HttpResponse
from .activity_tracker import activity_data
import subprocess

def save_name(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        request.session['user_name'] = name
        return redirect('activity_view')

    return HttpResponse("Invalid request method", status=405)

def activity_view(request):
    # Get the user name from the session
    user_name = request.session.get('user_name', 'Guest')
    # Prepare the context with the latest activity data
    context = {
        'status': activity_data.get('status', 'No data'),
        'active_time': activity_data.get('active_time', 'No data'),
        'screenshot_path': activity_data.get('screenshot_path', 'No data'),
        'user_name': user_name, 
        'finaldata':activity_data.get('finaldata', 'nodata'), 
        'mousecount':activity_data.get('mousecount', 'nodata'),
        'keycount':activity_data.get('keycount', 'nodata')
    }
    return render(request, 'working.html', context)

def dashboard(request):
    return render(request, 'dashboard.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import AccessLog
from django.contrib.auth.models import User

@csrf_exempt
def employee_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Log successful login
            AccessLog.objects.create(
                user=user, 
                status="Success", 
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return redirect('employee_dashboard')
        else:
            # Log failed attempt
            try:
                user_obj = User.objects.get(username=username)
                AccessLog.objects.create(
                    user=user_obj, 
                    status="Failure", 
                    ip_address=request.META.get('REMOTE_ADDR')
                )
            except User.DoesNotExist:
                # Create a log entry even if user doesn't exist
                AccessLog.objects.create(
                    user=None, 
                    status="Failure - User not found", 
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
            return render(request, 'portal/login.html', {
                'error': 'Invalid credentials'
            })
    
    return render(request, 'portal/login.html')

@login_required
def employee_dashboard(request):
    # Display some fake sensitive data
    employees = [
        {'name': 'John Doe', 'department': 'Engineering', 'salary': '$85,000'},
        {'name': 'Jane Smith', 'department': 'Marketing', 'salary': '$75,000'},
        {'name': 'Mike Johnson', 'department': 'Sales', 'salary': '$90,000'},
        {'name': 'Sarah Williams', 'department': 'HR', 'salary': '$65,000'},
    ]
    
    return render(request, 'portal/dashboard.html', {'employees': employees})

def logout_view(request):
    logout(request)
    return redirect('employee_login')
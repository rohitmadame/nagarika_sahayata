from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .models import Complaint, ComplaintImage

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(f"Authentication result: {user}")  # Debug line
            
            if user is not None:
                login(request, user)
                print(f"User {username} logged in successfully")  # Debug line
                print(f"Is staff: {user.is_staff}")  # Debug line
                return redirect('admin_dashboard' if user.is_staff else 'user_dashboard')
        
        # Add more detailed error messages
        messages.error(request, "Authentication failed. Please check your credentials.")
        return render(request, 'user_login.html', {'form': form})
    
    return render(request, 'user_login.html', {'form': AuthenticationForm()})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('user_login')
        return render(request, 'user_register.html', {'form': form})
    return render(request, 'user_register.html', {'form': UserCreationForm()})

@login_required
def user_dashboard(request):
    complaints = Complaint.objects.filter(user=request.user)
    return render(request, 'user_dashboard.html', {'complaints': complaints})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')
    
    complaints = Complaint.objects.select_related('user').all().order_by('-created_at')
    status_counts = {status: Complaint.objects.filter(status=status).count() 
                    for status in ['pending', 'in_progress', 'resolved']}
    
    return render(request, 'admin_dashboard.html', {
        'complaints': complaints,
        'status_counts': status_counts,
        'total_complaints': sum(status_counts.values())
    })

@login_required
def add_complaint(request):
    if request.method == 'POST':
        complaint = Complaint.objects.create(
            user=request.user,
            complaint_type=request.POST.get('complaint_type'),
            city=request.POST.get('city'),
            ward_number=request.POST.get('ward_number'),
            landmark=request.POST.get('landmark'),
            description=request.POST.get('description')
        )
        for file in request.FILES.getlist('images'):
            ComplaintImage.objects.create(complaint=complaint, image=file)
        messages.success(request, 'Complaint submitted successfully!')
        return redirect('user_dashboard')
    return render(request, 'add_complaint.html')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            messages.error(request, 'You are not authorized as admin')
        return render(request, 'admin_login.html', {'form': form})
    return render(request, 'admin_login.html', {'form': AuthenticationForm()})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('user_login')

@require_POST
@login_required
def update_status(request, complaint_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    new_status = request.POST.get('status')
    
    if new_status not in dict(Complaint.STATUS_CHOICES):
        return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
        
    complaint.status = new_status
    complaint.save()
    
    return JsonResponse({
        'success': True,
        'new_status': complaint.get_status_display(),
        'status_class': {
            'pending': 'bg-warning',
            'in_progress': 'bg-primary',
            'resolved': 'bg-success'
        }[new_status]
    })

@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    return render(request, 'complaint_detail.html', {'complaint': complaint})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import UserProfile, UserLink
from .forms import UserProfileForm, UserLinkForm
import qrcode
from io import BytesIO
import base64


# Public profile view (Linktree-style page)
def public_profile(request, username):
    """Public view of user's Linktree-style profile"""
    profile = get_object_or_404(UserProfile, username=username, is_active=True)
    links = profile.links.filter(is_active=True).order_by('display_order')
    
    # Generate QR code for profile URL
    qr_code_base64 = None
    if profile.qr_code_enabled:
        profile_url = request.build_absolute_uri(profile.get_public_url())
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(profile_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'profile': profile,
        'links': links,
        'qr_code': qr_code_base64,
        'profile_url': request.build_absolute_uri(profile.get_public_url()),
    }
    return render(request, 'user_profile/public_profile.html', context)


# Dashboard views
@login_required
def profile_dashboard(request):
    """Dashboard for managing user profile"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    links = profile.links.all().order_by('display_order') if profile else []
    
    context = {
        'profile': profile,
        'links': links,
    }
    return render(request, 'user_profile/dashboard.html', context)


@login_required
def create_profile(request):
    """Create a new user profile"""
    if hasattr(request.user, 'profile'):
        messages.info(request, 'You already have a profile. You can edit it below.')
        return redirect('edit_profile')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('profile_dashboard')
    else:
        # Pre-populate with user data
        initial_data = {
            'username': request.user.username,
            'display_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        }
        form = UserProfileForm(initial=initial_data)
    
    return render(request, 'user_profile/create_profile.html', {'form': form})


@login_required
def edit_profile(request):
    """Edit existing user profile"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'user_profile/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def add_link(request):
    """Add a new link to profile"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserLinkForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = profile
            link.save()
            messages.success(request, 'Link added successfully!')
            return redirect('profile_dashboard')
    else:
        form = UserLinkForm()
    
    return render(request, 'user_profile/add_link.html', {'form': form, 'profile': profile})


@login_required
def edit_link(request, link_id):
    """Edit an existing link"""
    link = get_object_or_404(UserLink, id=link_id, profile__user=request.user)
    
    if request.method == 'POST':
        form = UserLinkForm(request.POST, request.FILES, instance=link)
        if form.is_valid():
            form.save()
            messages.success(request, 'Link updated successfully!')
            return redirect('profile_dashboard')
    else:
        form = UserLinkForm(instance=link)
    
    return render(request, 'user_profile/edit_link.html', {'form': form, 'link': link})


@login_required
def delete_link(request, link_id):
    """Delete a link"""
    link = get_object_or_404(UserLink, id=link_id, profile__user=request.user)
    
    if request.method == 'POST':
        link.delete()
        messages.success(request, 'Link deleted successfully!')
        return redirect('profile_dashboard')
    
    return render(request, 'user_profile/delete_link.html', {'link': link})


@login_required
def toggle_link_status(request, link_id):
    """Toggle link active/inactive status"""
    link = get_object_or_404(UserLink, id=link_id, profile__user=request.user)
    link.is_active = not link.is_active
    link.save()
    
    status = 'activated' if link.is_active else 'deactivated'
    messages.success(request, f'Link {status} successfully!')
    return redirect('profile_dashboard')


# Link click tracking
def track_link_click(request, link_id):
    """Track link clicks and redirect"""
    link = get_object_or_404(UserLink, id=link_id, is_active=True)
    link.increment_clicks()
    return redirect(link.url)


# Preview profile
@login_required
def preview_profile(request):
    """Preview profile before publishing"""
    profile = get_object_or_404(UserProfile, user=request.user)
    links = profile.links.filter(is_active=True).order_by('display_order')
    
    # Generate QR code
    qr_code_base64 = None
    if profile.qr_code_enabled:
        profile_url = request.build_absolute_uri(profile.get_public_url())
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(profile_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'profile': profile,
        'links': links,
        'qr_code': qr_code_base64,
        'profile_url': request.build_absolute_uri(profile.get_public_url()),
        'is_preview': True,
    }
    return render(request, 'user_profile/public_profile.html', context)

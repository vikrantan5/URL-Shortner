from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Theme choices for customization
THEME_CHOICES = [
    ('dark', 'Dark Theme'),
    ('light', 'Light Theme'),
    ('gradient_purple', 'Purple Gradient'),
    ('gradient_blue', 'Blue Gradient'),
    ('gradient_pink', 'Pink Gradient'),
    ('neon_cyan', 'Neon Cyan'),
    ('sunset', 'Sunset'),
    ('ocean', 'Ocean'),
]

# Layout choices
LAYOUT_CHOICES = [
    ('minimal', 'Minimal'),
    ('classic', 'Classic'),
    ('modern', 'Modern'),
    ('glassmorphism', 'Glassmorphism'),
]

# Link type choices
LINK_TYPE_CHOICES = [
    ('youtube', 'YouTube'),
    ('instagram', 'Instagram'),
    ('whatsapp', 'WhatsApp'),
    ('website', 'Website'),
    ('twitter', 'Twitter/X'),
    ('github', 'GitHub'),
    ('linkedin', 'LinkedIn'),
    ('facebook', 'Facebook'),
    ('tiktok', 'TikTok'),
    ('spotify', 'Spotify'),
    ('custom', 'Custom Link'),
]


class UserProfile(models.Model):
    """User profile for Linktree-style page"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=50, unique=True, help_text="Unique username for public profile URL")
    display_name = models.CharField(max_length=100, help_text="Name displayed on profile")
    bio = models.TextField(max_length=500, blank=True, help_text="Short bio/description")
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    # Customization options
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='dark')
    layout = models.CharField(max_length=50, choices=LAYOUT_CHOICES, default='glassmorphism')
    primary_color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color code")
    secondary_color = models.CharField(max_length=7, default='#8B5CF6', help_text="Hex color code")
    background_color = models.CharField(max_length=7, default='#000000', help_text="Hex color code")
    text_color = models.CharField(max_length=7, default='#FFFFFF', help_text="Hex color code")
    
    # QR Code
    qr_code_enabled = models.BooleanField(default=True)
    
    # SEO
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.display_name} (@{self.username})"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = slugify(self.user.username)
        super().save(*args, **kwargs)

    def get_public_url(self):
        return f"/{self.username}/"


class UserLink(models.Model):
    """Individual links for user profile"""
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='links')
    link_type = models.CharField(max_length=50, choices=LINK_TYPE_CHOICES)
    title = models.CharField(max_length=100, help_text="Display title for the link")
    url = models.URLField(max_length=500)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    description = models.CharField(max_length=200, blank=True)
    
    # Customization for individual link
    custom_color = models.CharField(max_length=7, blank=True, help_text="Custom color for this link")
    thumbnail = models.ImageField(upload_to='link_thumbnails/', blank=True, null=True)
    
    # Display settings
    display_order = models.IntegerField(default=0, help_text="Order in which link appears (lower first)")
    is_active = models.BooleanField(default=True)
    
    # Analytics
    click_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.profile.username} - {self.title}"

    def increment_clicks(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])

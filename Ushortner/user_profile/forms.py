from django import forms
from .models import UserProfile, UserLink


class UserProfileForm(forms.ModelForm):
    """Form for creating/editing user profile"""
    
    class Meta:
        model = UserProfile
        fields = [
            'username', 'display_name', 'bio', 'profile_image',
            'theme', 'layout', 'primary_color', 'secondary_color',
            'background_color', 'text_color', 'qr_code_enabled',
            'meta_title', 'meta_description'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'your-username'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your Name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Tell people about yourself...',
                'rows': 4
            }),
            'theme': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'layout': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'primary_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-12 px-2 py-1 border border-gray-300 rounded-lg cursor-pointer'
            }),
            'secondary_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-12 px-2 py-1 border border-gray-300 rounded-lg cursor-pointer'
            }),
            'background_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-12 px-2 py-1 border border-gray-300 rounded-lg cursor-pointer'
            }),
            'text_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-12 px-2 py-1 border border-gray-300 rounded-lg cursor-pointer'
            }),
            'qr_code_enabled': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'SEO Title'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'SEO Description',
                'rows': 3
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower().strip()
            if not username.replace('-', '').replace('_', '').isalnum():
                raise forms.ValidationError('Username can only contain letters, numbers, hyphens, and underscores.')
        return username


class UserLinkForm(forms.ModelForm):
    """Form for creating/editing user links"""
    
    class Meta:
        model = UserLink
        fields = [
            'link_type', 'title', 'url', 'icon', 'description',
            'custom_color', 'thumbnail', 'display_order', 'is_active'
        ]
        widgets = {
            'link_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Link Title'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://example.com'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '🔗 or icon-name'
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Optional description'
            }),
            'custom_color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'w-full h-12 px-2 py-1 border border-gray-300 rounded-lg cursor-pointer'
            }),
            'display_order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

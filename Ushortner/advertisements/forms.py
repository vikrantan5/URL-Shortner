from django import forms
from .models import Campaign, Reel, Comment


# Shared dark-theme input styling so form fields match the NeuraSafe design system
_DARK_INPUT_CLASSES = (
    "w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-white/10 "
    "text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 "
    "focus:ring-2 focus:ring-cyan-500/20 transition-all"
)

_DARK_FILE_CLASSES = (
    "w-full px-4 py-3 rounded-xl bg-slate-800/60 border border-white/10 "
    "text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 "
    "file:bg-cyan-500/10 file:text-cyan-300 hover:file:bg-cyan-500/20 "
    "focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 transition-all"
)


# forms for campaign
class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['url', 'description', 'image']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': _DARK_INPUT_CLASSES,
                'placeholder': 'https://www.example.com',
            }),
            'description': forms.Textarea(attrs={
                'class': _DARK_INPUT_CLASSES,
                'rows': 4,
                'placeholder': 'Describe your campaign...',
            }),
            'image': forms.ClearableFileInput(attrs={'class': _DARK_FILE_CLASSES}),
        }


# forms for reels
class ReelForm(forms.ModelForm):
    class Meta:
        model = Reel
        fields = ['video', 'description', 'url']
        widgets = {
            'video': forms.ClearableFileInput(attrs={'class': _DARK_FILE_CLASSES}),
            'description': forms.Textarea(attrs={
                'class': _DARK_INPUT_CLASSES,
                'rows': 4,
                'placeholder': 'Describe your reel...',
            }),
            'url': forms.URLInput(attrs={
                'class': _DARK_INPUT_CLASSES,
                'placeholder': 'https://www.example.com',
            }),
        }


# forms for comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': _DARK_INPUT_CLASSES,
                'rows': 4,
                'placeholder': 'Write a comment...',
            }),
        }

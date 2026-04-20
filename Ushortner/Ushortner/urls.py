
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from user_profile import views as profile_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('urlshortner.urls')),
    path('accounts/', include('allauth.urls')),
    path('chat/', include('chat.urls')),
    path('business_card/', include('business_card.urls')),
    path('detect/', include('detect.urls')),
    path('advertisements/', include('advertisements.urls')),
    path('landing/', include('landing_pages.urls')),
    path('profile/', include('user_profile.urls')),
    path('s/', include('user.urls')),  # Short URL routes with /s/ prefix
    
    # Public profile route (must be last to avoid conflicts)
    path('<str:username>/', profile_views.public_profile, name='public_profile'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


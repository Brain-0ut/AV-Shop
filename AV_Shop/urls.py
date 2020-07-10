from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.urls import path, include
from django.views.generic import RedirectView

from AVShop import views

urlpatterns = [
                  path('', views.index, name='homepage'),
                  path('admin/', admin.site.urls),
                  path('shop/', include('AVShop.urls')),
                  path('users/', include('users.urls')),
                  path('about/', RedirectView.as_view(url='/articles/about_us')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.contrib import admin
from django.urls import path, include

from myauth.feeds import LatestServiceFeed
from . import views as web_views
from support import views as serv_views

from django.conf import settings
from django.conf.urls.static import static
from myauth.sitemaps import *
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'services': ServiceSitemap,
 
    'others': StaticSitemap,
}

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('auth', include("myauth.urls")),
    path('', web_views.home, name='home'),
    path('<int:id>/<slug:slug>', serv_views.service, name='service'),
    path('about', web_views.about, name='about'),
    path('portfolio', web_views.portfolio, name='portfolio'),
    path('services', web_views.services, name='services'),
    path('contact', web_views.contact, name='contact'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feeds/', LatestServiceFeed(), name='vehicle_feed'),
]


admin.site.site_title = "Earth Work Civils Services"
admin.site.site_header = "Earth Work Civils Inc"
admin.site.index_title = "Earth Work Civils welcomes you!!!"



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
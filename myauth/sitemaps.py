from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from support.models import Service



class StaticSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 1

    def items(self):
        return ['home', 'about', 'portfolio', 'contact', 'services']

    def location(self, item):
        return reverse(item)
    
class ServiceSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9
    
    def items(self):
        return Service.objects.all()
    
    def lastmod(self, obj):
        return obj.date_updated
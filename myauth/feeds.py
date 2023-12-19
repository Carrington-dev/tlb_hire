from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from support.models import Service
# from cars.models import Vehicle

class LatestServiceFeed(Feed):
    title = f'Earth Work Civils'
    link = reverse_lazy('services')
    description = 'Earth Work Civils'
    
    def items(self):
        return Service.objects.all()
    
    def item_title(self, item):
        return item.subject
    
    def item_description(self, item):
        return truncatewords(item.message, 50)
    
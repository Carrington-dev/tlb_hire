from django.shortcuts import render
from support.models import Service



def service(request, id, slug):
    context = dict()
    try:
        work = Service.objects.get(id=id)
        context['service'] = work
        context['title'] = work.subject
    except:
        pass
    context['services'] = Service.objects.all()
    return render(request, 'basic/service.html', context)
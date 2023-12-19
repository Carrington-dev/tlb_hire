from django.shortcuts import render, redirect
from django.contrib import messages
from support.forms import ContactForm
from support.models import Service


def home(request):
    context = {}
    context['title'] = 'TLB Hire Gauteng. Best Price TLB Hire'
    return render(request, 'basic/home.html', context)

def about(request):
    context = {}
    context['title'] = 'Site Demolition in Gauteng. Rubble Removal'
    return render(request, 'basic/about.html', context)

def portfolio(request):
    context = {}
    context['title'] = 'Tree Cutting. Earth Work and Excavations'
    return render(request, 'basic/portfolio.html', context)

def contact(request):
    context = {}
    company = f'Earth Civil Works'
    context['title'] = f'Contact | { company }'
    form = ContactForm(request.POST, None)
    if request.method == 'POST':
        form = ContactForm(request.POST, None)
        form.save()
        messages.info(request, f'Your information was saved successfully!, you will be contacted soon.')
        return redirect('home')
    context['form'] = form
    return render(request, 'basic/contact.html', context)

def services(request):
    context = {}
    context['title'] = 'Truck Hire | Earth Civil Works'
    context['services'] = Service.objects.all() 
    return render(request, 'basic/services.html', context)
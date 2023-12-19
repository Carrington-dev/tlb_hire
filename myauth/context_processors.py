from support.models import Service


def show_me(request):
    context = {}
    context['company'] = "Earth Work Civils"   
    context['street'] = "10 Senekal Street"   
    context['state'] = "Wierdapark"   
    context['cc'] = "Gaunteng"   
    context['zip'] = "0157"   
    context['city'] = "Centurion"   
    context['company'] = "Earth Work Civils"   
    context['email'] = "info@earthworkcivils.co.za"   
    context['tel1'] = "+27 645 227 690"   
    context['tel2'] = "+27 645 227 690"   
      
    context['motivation'] = "Earth Work Civils (Pty) Ltd, a member of the Earth Work Civils Group, was established in 2015 by the E W C Group’s Managing Director, Nico Louw. The company’s constant drive to acquire brown and greenfield land for Commercial, Industrial, Retail and especially Residential development clearly indicated the growing need for an earthworks and civils arm within the company. All earthworks and civils work had been outsourced previously"    
    return context
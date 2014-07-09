'''
Created on 20 March 2014
@author: adeel
'''
from iwidget.models import DMA

'''
make the DMA object available throughout the website
make the household of the user available throughout the site, this method only return one/first household of user, need NTUA clarification?
'''
def initialise(request):
    #user = request.user
    #if not (user.is_staff or user.is_superuser):
    #    household = user.households.all()[0]
    #else:
    #    household = None
    return {
        'dmas': DMA.objects.all(),#'household': household,
    }      
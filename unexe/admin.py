from django.contrib.gis import admin
from unexe.models import *

admin.site.register(Forecast)
admin.site.register(ElectricForecast)
admin.site.register(DMAstats)
admin.site.register(userDMAstats)
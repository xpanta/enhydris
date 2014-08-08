from django.contrib import admin
from iwidget.models import (HouseholdValueCategory, HouseholdValueSubcategory,
                          PropertyType, ConstructionPeriod, OwnershipStatus,
                          OutdoorFacility, WaterHeater, EfficientAppliance,
                          WaterPricingScheme, WaterDMS,Country,UserProfile)
admin.site.register(HouseholdValueCategory)
admin.site.register(HouseholdValueSubcategory)
admin.site.register(PropertyType)
admin.site.register(ConstructionPeriod)
admin.site.register(OwnershipStatus)
admin.site.register(OutdoorFacility)
admin.site.register(WaterHeater)
admin.site.register(EfficientAppliance)
admin.site.register(WaterPricingScheme)
admin.site.register(WaterDMS)
admin.site.register(Country)
admin.site.register(UserProfile)
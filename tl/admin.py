#UWOTTL, Copyright (c) 2012, National Technical University of Athens

from tl.models import *
from django.contrib import admin
from django.views.decorators.csrf import csrf_protect

def has_permission(request, obj=None, perm=''):
     if request.user.has_perm(perm):
         return True
     return False

class BrandInline(admin.TabularInline):
    model = Brand
    extra = 1

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1

class TechnologyAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            if not has_permission(request, obj,
                    'tl.can_alter_remarks'):
                self.fields = []
            else:
                self.fields = ['remarks']
            self.inlines = []
        return super(TechnologyAdmin, self).get_form(request, obj, **kwargs)

    list_display = ('id', 'descr', 'code',)
    inlines = [BrandInline,]    

class BrandAdmin(admin.ModelAdmin):
    list_filter = ('technology', )
    inlines = [SpecificationInline,]
    list_display = ('id','old_id', 'technology', 'descr')

class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('brand', 'category', 'no', 'i', 'j')

admin.site.register(Unit, admin.ModelAdmin)
admin.site.register(SpecificationCategory, admin.ModelAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Specification, SpecificationAdmin)

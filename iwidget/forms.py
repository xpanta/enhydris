# -*- coding: utf-8 -*-
#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013 National Techincal University of Athens

from django import forms

from uc011.models import (Household, ArithmeticValueItem,
                          HouseholdValueSubcategory)


class HouseholdForm(forms.ModelForm):

    class Meta:
        model = Household
        fields = ['num_of_occupants', 'property_type', 'property_size',
                  'construction_period', 'ownership_status',
                  'outdoor_facilities', 'water_heaters', 'water_pricing',
                  'efficient_appliances', 'water_dms']
        widgets = {
            'outdoor_facilities': forms.CheckboxSelectMultiple,
            'water_heaters': forms.CheckboxSelectMultiple,
            'efficient_appliances': forms.CheckboxSelectMultiple,
            'water_dms': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(HouseholdForm, self).__init__(*args, **kwargs)
        for item in HouseholdValueSubcategory.objects.\
                select_related('category').all().\
                order_by('category', 'id'):
            field_name = 'auto_%s_%s'%(item.category.id, item.id) \
                if not item.form_component else item.form_component
            self.fields[field_name] = forms.IntegerField(label=item.descr,
                                                         required=False)
            self.fields[field_name].category = item.category.descr
        for item in self.instance.arithmetic_values_items.all():
            field_name = 'auto_%s_%s' % (item.subcategory.category.id,
                                         item.subcategory.id) \
                if not item.subcategory.form_component \
                else item.subcategory.form_component
            self.fields[field_name].initial = item.number
        # This is a workarround to Django 1.4 bug
        for field in ('outdoor_facilities', 'water_heaters',
                      'efficient_appliances', 'water_dms'):
            self.fields[field].help_text = self.fields[field].help_text.\
                split('$')[0]

    def save(self, *args, **kwargs):
        super(HouseholdForm, self).save(*args, **kwargs)
        aset = []
        self.instance.arithmetic_values.clear()
        for item in HouseholdValueSubcategory.objects.\
                select_related('category').all().\
                order_by('category', 'id'):
            field_name = 'auto_%s_%s'%(item.category.id, item.id) if \
                    not item.form_component else item.form_component
            if self.cleaned_data.get(field_name, None):
                value = self.cleaned_data[field_name]
                aset.append(ArithmeticValueItem.objects.create(
                            subcategory=item,
                            household=self.instance,
                            number=value))
        self.arithmetic_values_items = aset


from django.contrib import admin

# Register your models here.


from .models import (FileType,
                    ShoreFile,
					Vessel,
					Shipper,
					Booking,
					Container)

from datetime import date
from django.utils.translation import gettext_lazy as _




class ShoreFileAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description','status')
    list_editable = ()
    fieldsets = [
        ('Basic Information',{'fields': ['name','description','status']}),
    ]
admin.site.register(ShoreFile,ShoreFileAdmin)


class VesselAdmin(admin.ModelAdmin):
    search_fields = ['name','code','description']
    list_filter = []
    list_display = ('name','code','description','status')
    list_editable = ()
    fieldsets = [
        ('Basic Information',{'fields': ['name','code','description','status']}),
    ]
admin.site.register(Vessel,VesselAdmin)


class ShipperAdmin(admin.ModelAdmin):
    search_fields = ['name','code','description']
    list_filter = []
    list_display = ('name','code','description','status')
    list_editable = ()
    fieldsets = [
        ('Basic Information',{'fields': ['name','code','description','status']}),
    ]
admin.site.register(Shipper,ShipperAdmin)



class BookingAdmin(admin.ModelAdmin):
    search_fields = ['number','voy','pod','shipper__name','vessel__name','description']
    list_filter = ['pod','shipper']
    list_display = ('number','voy','pod','shipper','vessel','description')
    list_editable = ()
    fieldsets = [
        ('Basic Information',{'fields': ['number','slug','voy','pod','shipper','vessel','description','status','user']}),
    ]
admin.site.register(Booking,BookingAdmin)



class ContainerAdmin(admin.ModelAdmin):
    search_fields = ['number','booking__number']
    list_filter = ['container_type','container_size']
    list_display = ('number','booking','container_type','container_size','payment','dg_class','created_date')
    list_editable = ()
    fieldsets = [
        ('Basic Information',{'fields': ['number','booking','description']}),
        ('Type',{'fields': ['container_type','container_size','dg_class','temperature']}),
        ('Other',{'fields': ['payment','unno','status']}),
    ]
admin.site.register(Container,ContainerAdmin)

admin.site.register(FileType)
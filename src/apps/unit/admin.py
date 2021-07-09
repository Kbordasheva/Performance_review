from django.contrib import admin

from unit.models import Unit


class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager')
    fields = ('name', 'manager')


admin.site.register(Unit, UnitAdmin)
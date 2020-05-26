from .models import *
# Register your models here.
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# class OdpowiedziAdminListFilter(admin.SimpleListFilter):
#     title = _('pytanie')
#     parameter_name = 'pytanie'
#     def lookups(self, request, model_admin):
#         pytania = Odpowiedzi.pytanie.get_queryset()
#         return [(pytania.pk, pytania.tresc) for pytania in pytania]
#     def queryset(self, request, queryset):
#         value = self.value()
#         if value is not None:
#             return queryset.filter(pytania_id = self.value())
#         return queryset

class OdpowiedziAdminModel(admin.ModelAdmin):
    pytanie = list(Odpowiedzi.pytanie.get_queryset())
    list_filter = ('pytanie',)



class WynikiAdminModel(admin.ModelAdmin):
    list_display = ('uzytkownik', 'wynik')
    list_filter = ('uzytkownik','wynik')


admin.site.site_header = 'Panel administracyjny projektu Django'
admin.site.register(WynikiModel, WynikiAdminModel)
admin.site.register(Pytania)
admin.site.register(Odpowiedzi,OdpowiedziAdminModel)
admin.site.register(WyborOdpowiedzi)
admin.site.register(Uzytkownicy)

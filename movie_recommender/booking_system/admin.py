from django.contrib import admin

from .models import *


class TheaterAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(TheaterAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(TheaterAdmin, self).get_form(request, obj=None, **kwargs)
        else:
            fields = ["name", "location"]
            kwargs.update({"fields": fields})
            return super(TheaterAdmin, self).get_form(request, obj=None, **kwargs)

    def save_form(self, request, form, change):
        obj = super(TheaterAdmin, self).save_form(request, form, change)
        if not request.user.is_superuser:
            obj.owner = request.user
            obj.save()
        return obj

    def save_formset(self, request, form, formset, change):
        formset.save()
        if not change:
            for f in formset.forms:
                try:
                    obj = f.instance
                    if obj.owner is None:
                        obj.owner = request.user
                        obj.save()
                except Exception as e:
                    continue


class ScreenAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(ScreenAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(theater__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "theater" and not request.user.is_superuser:
            kwargs["queryset"] = Theater.objects.filter(owner=request.user)
        return super(ScreenAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ShowAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(ShowAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(screen__theater__owner=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "screen" and not request.user.is_superuser:
            kwargs["queryset"] = Screen.objects.filter(theater__owner=request.user)
        return super(ShowAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.


admin.site.register(Movie)
admin.site.register(CrewProfile)
admin.site.register(Crew)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(Genre)
admin.site.register(Show, ShowAdmin)
admin.site.register(Screen, ScreenAdmin)
admin.site.register(SeatType)
admin.site.register(CastType)
admin.site.register(Location)
admin.site.register(StatusType)
admin.site.register(Invoice)
admin.site.register(Booking)
admin.site.register(Seat, ShowAdmin)
admin.site.register(UserProfile)
admin.site.register(City)
admin.site.register(PredictedRating)
admin.site.register(Similar)

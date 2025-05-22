from django.contrib import admin
from .models import RoadSegment, SpeedReading


@admin.register(RoadSegment)
class RoadSegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'long_start', 'lat_start', 'long_end', 'lat_end', 'length')
    search_fields = ('id',)
    list_filter = ('length',)


@admin.register(SpeedReading)
class SpeedReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'road_segment', 'speed', 'intensity_display', 'timestamp')
    search_fields = ('road_segment__id',)

    list_filter = ('speed',)
    
    def intensity_display(self, obj):
        return obj.intensity
    intensity_display.short_description = 'Intensity'


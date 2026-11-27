from django.contrib import admin
from .models import TelemetryRecord

@admin.register(TelemetryRecord)
class TelemetryRecordAdmin(admin.ModelAdmin):
    list_display = ("satellite_id", "altitude", "temperature", "battery", "signal_strength", "status")
    list_filter = ("status",)
    search_fields = ("satellite_id",)

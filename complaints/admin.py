from django.contrib import admin
from django.utils.html import format_html
from .models import Complaint, ComplaintImage

class ComplaintImageInline(admin.TabularInline):
    model = ComplaintImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 100px;">', obj.image.url) if obj.image else "No Image"
    image_preview.short_description = "Preview"

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'complaint_type', 'ward_number', 'city', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'complaint_type', 'city')
    search_fields = ('city', 'ward_number', 'description')
    inlines = [ComplaintImageInline]

@admin.register(ComplaintImage)
class ComplaintImageAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 200px;">', obj.image.url)
    image_preview.short_description = "Image Preview"
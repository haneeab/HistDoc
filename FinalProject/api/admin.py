from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Manuscript, ManuscriptFile

@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)

@admin.register(ManuscriptFile)
class ManuscriptFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_type', 'manuscript', 'uploaded_at')
    search_fields = ('file',)
    list_filter = ('file_type', 'uploaded_at')

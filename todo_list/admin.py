from django.contrib import admin
from .models import Todo_model

@admin.register(Todo_model)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'priority', 'completed', 'user')
    list_filter = ('priority', 'completed')
    search_fields = ('title',)

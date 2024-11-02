from django.contrib import admin
from .models import Request, Category

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'user']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'user__username']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'completed':
            return ['title', 'user', 'description', 'category', 'photo', 'status', 'comment']
        return ['title', 'user', 'description', 'category', 'photo']

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status == 'completed':
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if change and obj.status == 'completed':
            self.message_user(request, "Невозможно изменить объект с этим статусом.", level='error')
            return
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
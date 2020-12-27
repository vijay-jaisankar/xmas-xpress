from django.contrib import admin
from .models import Room
# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','slug','description','budget','active')
    list_filter = ('name','description')
    search_fields = ('name','description')
    prepopulated_fields = {'slug':('name','password',)}
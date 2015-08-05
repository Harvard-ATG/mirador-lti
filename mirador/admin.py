from django.contrib import admin
from .models import IsiteImages, LTICourseImages

class IsiteImagesAdmin(admin.ModelAdmin):
    pass

class LTICourseImagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(IsiteImages, IsiteImagesAdmin)
admin.site.register(LTICourseImages, LTICourseImagesAdmin)

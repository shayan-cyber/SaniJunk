from django.contrib import admin
from .models import Locations, NewsLetter, Quiz

# Register your models here.
admin.site.register(Locations)
admin.site.register(NewsLetter)
admin.site.register(Quiz)

from django.contrib import admin
from .models import User, Bet, Relationship

admin.site.register(User)
admin.site.register(Relationship)
admin.site.register(Bet)

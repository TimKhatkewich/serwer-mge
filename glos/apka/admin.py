from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Vote)
admin.site.register(VotingSession)
admin.site.register(Choice)
admin.site.register(CustomUser)

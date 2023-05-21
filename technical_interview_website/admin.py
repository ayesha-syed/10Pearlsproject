from django.contrib import admin

# Register your models here.
from .models import videos
from .models import Candidate
from .models import Position
from .models import ActualQuestion
from .models import Questionnaire
from .models import Admin
from .models import Interview

admin.site.register(videos)
admin.site.register(Candidate)
admin.site.register(Position)
admin.site.register(ActualQuestion)
admin.site.register(Admin)
admin.site.register(Questionnaire)
admin.site.register(Interview)
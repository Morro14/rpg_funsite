from django.contrib import admin
from .models import Post, Comment, User, News
from django.conf import settings


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(News)



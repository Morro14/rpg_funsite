from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField


class User(AbstractUser):

    def __str__(self):
        return f'{self.username}'

    tank = "TA"
    healer = "HE"
    dd = "DD"
    trader = "TR"
    guild_master = "GM"
    quest_giver = "QG"
    blacksmith = "BS"
    leatherworker = "LW"
    potion_master = "PM"
    spell_master = "SM"

    TYPES = [(tank, 'Tank'), (healer, 'Healer'), (dd, 'Damage Dealer'), (trader, 'Trader'),
             (guild_master, 'Guild Master'), (quest_giver, 'Quest Giver'), (blacksmith, 'Blacksmith'),
             (leatherworker, 'Leather-worker'), (potion_master, 'Potion Master'), (spell_master, 'Spell Master')]

    role = models.CharField(max_length=2, choices=TYPES, verbose_name='Role', )
    email_confirmed = models.BooleanField(default=False)


# class Author(models.Model):
#    def __str__(self):
#        return f'{self.user}'
#
#    user = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Post(models.Model):
    def __str__(self):
        return f'{self.head} ({self.user})'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    head = models.CharField(max_length=255, help_text='Head')
    rating = models.FloatField(default=0.0)
    #    text = models.TextField(null=True)
    time_in = models.DateTimeField(auto_created=True, auto_now_add=True)
    #    content = RichTextField(default='')
    content_upload = RichTextUploadingField(null=True,
                                            blank=True,
                                            #  config_name='default',
                                            #  external_plugin_resources=[('youtube',
                                            #                              '/static/ckeditor/ckeditor/plugins/youtube',
                                            #                              'plugin.js'
                                            #                              )],
                                            )

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Comment(models.Model):
    def __str__(self):
        return f'{self.text[0:20]}'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = RichTextField(blank=False, default='', max_length=255, )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    time_in = models.DateTimeField(auto_created=True, auto_now_add=True)


class News(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    head = models.CharField(max_length=255, help_text='Head')
    text = models.TextField()
    time_in = models.DateTimeField(auto_created=True, auto_now_add=True)

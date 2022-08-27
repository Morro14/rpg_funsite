import random
from django.db import models


class OneTimeCode(models.Model):
    def __str__(self):
        return f'{self.code}'
    rand_code = random.randrange(start=1000, stop=10000)
    code = models.TextField(default=rand_code, auto_created=True, )
    user = models.TextField()



from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_bithd = models.DateField(null = True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}',format(self.user.username)


'''Промежуточная модель поля ManyToMany'''
class Contanc(models.Model):
    user_from = models.ForeignKey(User, on_delete = models.CASCADE, related_name='rel_from_set')
    user_to = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Mete:
        ordering = ('-created')
    def __str__(self):
        return '{} folowing {}'.format(self.user_from, self.user_to)

'''Добавили динамическим способом поле в сандартную модель User'''
User.add_to_class('following', models.ManyToManyField('self',
                                                     related_name = 'followers',
                                                     through=Contanc,
                                                     symmetrical=False))
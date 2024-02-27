from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'actions', db_index=True)
    verb = models.CharField(max_length = 200, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj')
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    target = GenericForeignKey('target_ct','target_id')#поле поз-ет обращ.-ся к конкретным поля связанной модели


    class Meta:
        ordering = ('-date_created',)

# Create your models here.

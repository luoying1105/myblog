from django.contrib.auth.models import User
from django.db import models


# 用户之间关系模型 多对多
class Contact(models.Model):
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set')
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,
                                      self.user_to)



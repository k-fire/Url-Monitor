from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):

    # user对象可使用 user.userprofile, 或 user.proflie 得到用户信息
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    url_list = models.TextField('URL列表')

    class Meta:
        verbose_name = "用户URL"

    def __str__(self):
        return f"{self.user.__str__()}'s profile"

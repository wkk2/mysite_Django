from django.db import models

class User(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    sex = models.CharField(max_length=16,choices=gender,default='男')
    register_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-register_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    register_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user+": "+self.code
    class Meta:
        ordering = ['-register_time']
        verbose_name = 'confirm_link'
        verbose_name_plural = 'confirm_link'
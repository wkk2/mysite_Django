from django.db import models

class ServerManage(models.Model):
    serverName = models.CharField(max_length=30)
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    serverPart = models.CharField(max_length=30)

    def __str__(self):
        return self.serverName


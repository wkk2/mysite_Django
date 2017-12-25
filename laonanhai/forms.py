from django.forms import ModelForm
from .models import ServerManage

class ServerManageForm(ModelForm):
    class Meta:
        model = ServerManage
        fields = ['serverName' ,'ip','port','serverPart']

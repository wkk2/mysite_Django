from django.shortcuts import render
from .models import ServerManage
from .forms import ServerManageForm

def index(request):
    if request.method == 'POST':
        form = ServerManageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            serverName = cd['serverName']
            ip = cd['ip']
            port = cd['port']
            serverPart = cd['serverPart']
            ServerManage.objects.create(serverName,ip,port,serverPart)

    try:
        reqs = ServerManage.objects.all()
    except:
        message = 'NO datas'
        return render(request,'index.html', {'message': message})
    return render(request,'index.html',{'reqs':reqs})


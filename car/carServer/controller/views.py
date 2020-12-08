from django.shortcuts import render


def index(request):
    if request.method == "POST":
        if request.POST['front']:
            print(1)
    else:
        return render(request, 'controller/controller.html', locals())

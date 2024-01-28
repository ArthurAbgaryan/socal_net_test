from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from django.contrib import messages
from django.shortcuts import redirect

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageForm(data = request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit = False)
            new_item.user = request.user
            new_item.save()
            messages.success(request,'форма успешно сохранена')
            return redirect(new_item.get_absolute_url())

    else:
        form = ImageForm(data = request.GET)

    return render(request,'image_socal/image_create_form.html',{'form':form})


# Create your views here.

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import Image

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


def image_detail(request,slug, pk):
    image = get_object_or_404(Image, slug = slug,id = pk )

    return render(request, 'image_socal/image_detail.html',{'image':image})



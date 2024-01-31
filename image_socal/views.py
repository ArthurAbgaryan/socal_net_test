from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import Image
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse



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

@login_required
def like_ajax(request):
    object = get_object_or_404(Image,id = request.POST.get('id'))
    context = {}
    liked = False
    if object.users_likes.filter(id = request.user):
        object.users_likes.remove(request.user)
        liked = False
    else:
        object.users_likes.add(request.user)
        liked = True

    context['liked'] = liked
    context['object'] = object
    if request.is_ajax():
        html = render_to_string('image_socal/like_form_ajax.html',context,request = request)
    return JsonResponse({'form':html})

def image_detail(request,slug, pk):
    context = {}
    image = get_object_or_404(Image, slug = slug,id = pk )

    liked = False
    if image.users_likes.filter(id = request.user.id).exists():
        liked = True

    context['image'] = image
    context['liked'] = liked

    return render(request, 'image_socal/image_detail.html',context)



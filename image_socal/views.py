from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import Image
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST


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
@require_POST
def like_post_ajax(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    try:
        if image_id and action:
            image = Image.objects.get(id = image_id)
            if action == 'unlike':
                image.users_likes.remove(request.user)
            else:
                image.users_likes.add(request.user)
            return JsonResponse({'status':'ok'})
    except:
        pass
    return JsonResponse({'statis':'ok'})

# def like_post_ajax(request):
#     post = get_object_or_404(Image, id = 8)
#     liked = False
#     if post.users_likes.filter(id = request.user.id).exists():
#         post.users_likes.remove(request.user)
#         liked = False
#     else:
#         post.users_likes.add(request.user)
#         liked = True
#
#     context = {
#         'liked': liked,
#         'image': post,
#     }
#     if request.is_ajax():
#         html = render_to_string('image_socal/like_form_ajax.html', context, request=request)
#         return JsonResponse({'form':html})


def image_detail(request,slug, pk):
    image = get_object_or_404(Image, slug = slug,id = pk )
    liked = False
    if image.users_likes.filter(id = request.user.id).exists():
        liked = True
    return render(request, 'image_socal/image_detail.html',{'image':image, 'liked':liked})



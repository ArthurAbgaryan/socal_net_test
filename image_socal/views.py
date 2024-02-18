from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImageForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import Image
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
from actions.models import Action

@login_required
def list_image(request):
    list = Image.objects.all()
    paginator = Paginator(list,8)
    number_page = request.GET.get('page')
    actions = Action.objects.exclude(user = request.user)#об-кты активности кроме активностей пол-ля
    folow_obj = request.user.following.values_list('id', flat = True)#список подписок поль-ля
    if folow_obj:#если они есть
        actions = actions.filter(user_id__in = folow_obj)[:10]#получаем полсед. 10 активностей пол-ей
        actions = actions.select_related('user','user__profile')#пол-ем обекты ForeignKey через метод select_related
                                        #user__profile позвол. связаться с профилем польхователя
        actions = actions.prefetch_related('target')
    try:
        object = paginator.page(number_page)
    except PageNotAnInteger:
        object = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        object=paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'image_socal/list_ajax.html', {'object':object,
                                                              'section':'object',
                                                              'actions':actions})

    return render (request, 'image_socal/list_image.html', {'object':object,
                                                            'section':'object',
                                                            'actions':actions})
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageForm(data = request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit = False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'create image',new_item)
            messages.success(request,'форма успешно сохранена')
            return redirect(new_item.get_absolute_url())

    else:
        form = ImageForm(data = request.GET)

    return render(request,'image_socal/image_create_form.html',{'form':form})

@ajax_required
@login_required
@require_POST
def like_post_ajax(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    try:
        if image_id and action:
            obj = Image.objects.get(id = image_id)
            if action == 'unlike':
                obj.users_likes.remove(request.user)
            else:
                obj.users_likes.add(request.user)
                create_action(request.user, 'likes', obj)
            return JsonResponse({'status':'ok'})
    except:
        pass
    return JsonResponse({'status':'ok'})

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



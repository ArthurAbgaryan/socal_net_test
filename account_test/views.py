from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from .forms import LoginForm,UserForm,UserEdit,ProfileEdit
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from .models import Profile, Contanc
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from common.decorators import ajax_required
from actions.utils import create_action



@ajax_required
@login_required
@require_POST
def ajax_following(request):
    data_id = request.POST.get('id')
    data_action = request.POST.get('action')
    if data_id and data_action:
        try:
            user_get = User.objects.get(id = data_id)
            if data_action == 'follow':
                Contanc.objects.get_or_create(user_from = request.user, user_to = user_get)
                create_action(request.user, 'is follow', user_get)

            else:
                Contanc.objects.filter(user_from = request.user, user_to = user_get).delete()
            return JsonResponse ({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})



@login_required
def users_list(request):
    list_users = User.objects.filter(is_active = True)
    return render(request, 'account_test/users_list.html',
                  {'section':'people', 'list_users':list_users})

@login_required
def user_detail(request,username):
    user_profile = get_object_or_404(User, username = username, is_active = True)
    return render (request, 'account_test/user_detail.html',
                   {'section':'people', 'user_profile':user_profile})




@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEdit(instance= request.user, data=request.POST)
        profile_form = ProfileEdit(instance=request.user.profile, data = request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return render(request, 'account_test/edit_profile_done.html', {'user_form':user_form})
    else:
        user_form = UserEdit(instance = request.user)
        profile_form = ProfileEdit(instance= request.user.profile)
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'account_test/edit_profile.html', context)


def register(request):
    if request.method =='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user = new_user)
            create_action(new_user, 'create_profile')

            return render(request, 'account_test/register_done.html', {'new_user':new_user})
    else:
        form = UserForm()
    return render (request, 'account_test/register_form.html',{'form':form})

def main(request):
    return render(request, 'account_test/main.html', {'name':'Text from views'})

# def login_main(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username = cd['username'], password = cd['password'])
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponse ('Вы успешно зашли')
#             else:
#                 return HttpResponse ('Этот пользователь не активен')
#         else:
#             return HttpResponse('Такого пользователя не существует')
#     else:
#         form = LoginForm()
#     return render(request, 'account_test/login.html', {'form':form})





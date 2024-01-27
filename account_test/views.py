from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import LoginForm,UserForm,UserEdit,ProfileEdit
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required

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





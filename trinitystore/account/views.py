import mimetypes
import os

from .models import Profile
from actions.models import Action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

# from account.forms import UserRegisterationForm, UserEditForm, ProfileEditForm
# from account.models import Profile

# from actinos.models import Action
# from actions.utils import create_action
from account.forms import UserEditForm, ProfileEditForm, UserRegisterationForm
from actions.utils import create_action


@login_required
def dashboard(request):
    return render(request, 'account/index3.html', {'section': 'dashboard'})


@login_required
def profile(request):
    user = request.user
    actions = Action.objects.filter(user=request.user)
    dates = [item.created.date() for item in actions]
    dates = list(dict.fromkeys(dates))
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/profile.html', {'section': 'profile',
                                                    'actions': actions,
                                                    'dates': dates,
                                                    'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'user': user})


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)

            create_action(new_user, 'has created an account')
            #
            # send_mail('Trinity', 'welcome to Trinity', settings.EMAIL_HOST_USER, new_user.email)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegisterationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def is_ajax(request):
    return


@login_required
def edit(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            instance1 = user_form.save()
            instance2 = profile_form.save()
            ser_instance = serializers.serialize('json', [instance1, instance2])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": user_form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)


def do_edit(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def edit_form(request):
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def vip(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    vip_status = profile.vip
    if vip_status:
        return render(request, 'account/vip.html', {'section': 'vip'})
    else:
        return render(request, 'account/not_vip.html')


def download(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    vip_status = profile.vip
    if vip_status:
        pass
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define text file name
        filename = 'CSGOCheats-Loader-v1.0.0.1.zip'
        # Define the full file path
        filepath = BASE_DIR + '/filedownload/Files/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        return HttpResponse(status=404)


class CustomPasswordResetView(PasswordResetView):
    # success_url = reverse('account/password_reset_done.html')
    def get_success_url(self):
        # if not self.success_url:
        #     print('hgrerngjk')
        #     raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        # if self.success_url:
        print('ajsdofiahjg')
        self.success_url = reverse_lazy('account:password_reset_done')
        return str(self.success_url)  # success_url may be lazy


#
#     def get(self, request, *args, **kwargs):
#         success_url = 'account/password_reset_done.html'
#         super().get(request, *args, **kwargs)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_success_url(self):
        self.success_url = reverse_lazy('account:password_reset_complete')
        return str(self.success_url)  # success_url may be lazy

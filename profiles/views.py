from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import ProfileModelForm
from .models import Profile, Relationship

# Create your views here.


@login_required
def my_profile_view(request):

    profile = Profile.objects.get(user=request.user)

    form = ProfileModelForm(
        request.POST or None, request.FILES or None, instance=profile
    )

    confirm = False

    if request.method == "POST":
        if form.is_valid():
            form.save()
            confirm = True

    context = {"profile": profile, "form": form, "confirm": confirm}

    return render(request, "profiles/myProfile.html", context)


@login_required
def invites_recieved_view(request):

    profile = Profile.objects.get(user=request.user)

    qs = Relationship.objects.invitations_recieved(profile)

    results = list(map(lambda x: x.sender, qs))

    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {"qs": results, "is_empty": is_empty}

    return render(request, "profiles/my_invites.html", context)


@login_required
def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pk=pk)
        reciever = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, reciever=reciever)
        if rel.status == "send":
            rel.status = "accepted"
            rel.save()

    return redirect("profiles:my-invites-view")


@login_required
def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pk=pk)
        reciever = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship, sender=sender, reciever=reciever)
        rel.delete()

    return redirect("profiles:my-invites-view")


@login_required
def invite_profiles_list_view(request):

    qs = Profile.objects.get_all_profiles_to_invite(request.user)

    context = {"qs": qs}

    return render(request, "profiles/to_invite_profiles_list.html", context)


class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = Profile
    template_name = "profiles/profile_detail.html"

    def get_object(self):
        slug = self.kwargs["slug"]
        proifle = Profile.objects.get(slug=slug)
        return proifle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(reciever=profile)

        rel_reciver = []
        rel_sender = []

        for item in rel_r:
            rel_reciver.append(item.reciever.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_reciver"] = rel_reciver
        context["rel_sender"] = rel_sender
        context["posts"] = self.get_object().get_all_authors_posts()
        context["len_posts"] = (
            True if len(self.get_object().get_all_authors_posts()) > 0 else False
        )

        return context


class ProfileListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Profile.objects.get_all_profiles(self.request.user)

    context_object_name = "qs"

    template_name = "profiles/profiles_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(reciever=profile)

        rel_reciver = []
        rel_sender = []

        for item in rel_r:
            rel_reciver.append(item.reciever.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_reciver"] = rel_reciver
        context["rel_sender"] = rel_sender
        context["is_empty"] = False

        if len(self.get_queryset()) == 0:
            context["is_empty"] = True

        return context


@login_required
def send_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(user=request.user)
        reciever = Profile.objects.get(pk=pk)

        Relationship.objects.create(sender=sender, reciever=reciever, status="send")

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("profiles:my-profile-view")


@login_required
def remove_friends(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(user=request.user)
        reciever = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(reciever=reciever))
            | (Q(sender=reciever) & Q(reciever=sender))
        )

        rel.delete()

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect("profiles:my-profile-view")

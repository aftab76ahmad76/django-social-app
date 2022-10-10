from django.urls import path

from .views import (ProfileDetailView, ProfileListView, accept_invitation,
                    invite_profiles_list_view, invites_recieved_view,
                    my_profile_view, reject_invitation, remove_friends,
                    send_invitation)

app_name = "profiles"

urlpatterns = [
    path("", ProfileListView.as_view(), name="all-profiles-view"),
    path("accept-invitation/", accept_invitation, name="accept-invitation-view"),
    path("send-invite/", send_invitation, name="send-invite-view"),
    path("myProfile/", my_profile_view, name="my-profile-view"),
    path("my-invites/", invites_recieved_view, name="my-invites-view"),
    path("to-invite/", invite_profiles_list_view, name="to_invite_profiles-view"),
    path("remove-friends/", remove_friends, name="remove-friends-view"),
    path("<slug>/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("reject-invitation/", reject_invitation, name="reject-invitation-view"),
]

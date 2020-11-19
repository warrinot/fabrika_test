from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from polls.users_api import user_views
from polls.admin_api import admin_views


admin_router = routers.DefaultRouter()
admin_router.register('polls', admin_views.PollViewSet)
admin_router.register('questions', admin_views.QuestionViewSet)
admin_router.register('choices', admin_views.ChoiceViewSet)
admin_router.register('nested_polls', admin_views.NestedPollViewSet)

user_router = routers.DefaultRouter()
user_router.register('active_polls', user_views.ActivePollViewSet, basename='active_polls')
user_router.register('user_choices', user_views.UserChoiceViewsSet, basename='user_choices')
user_router.register('polls_finished_by_user', user_views.UserFinishedPolls,
                     basename='polls_finished_by_user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_api/', include(user_router.urls)),
    path('admin_api/', include(admin_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

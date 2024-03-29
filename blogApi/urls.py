from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
# from knox import view as knox_views
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = DefaultRouter()
router.register("Hello-viewset", views.HelloViewSet, basename="hello-viewset")
router.register("profile", views.UserProfileViewSet)
# router.register("login", views.LoginViewSet, basename="login")
router.register("feed", views.ProfileFeedViewSet)

urlpatterns = [
    url(r'^hello-django/?$', views.HelloApiView.as_view()),
    url(r'', include(router.urls)),
    url("auth/login/", obtain_auth_token, name='login')
    # url(r'login/', views.LoginApi.as_view(), name='login')
]


from django.shortcuts import render

from rest_framework import viewsets, status, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login
from knox.views import LoginView
from knox.models import AuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions


# Create your views here.


class HelloApiView(APIView):
    serializers_class = serializers.HelloSerializer

    # permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):

        an_apiView = [
            "Hello django 1 api view",
            "Hello django 2 api view",
            "Hello django 3 api view"
        ]

        return Response({"message": "Hello django", "an_apiView": an_apiView})

    def post(self, request):
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid:
            name = serializer.data.get('name')
            message = "Hello {0}".format(name)
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({"message": "Method put"})

    def patch(self, request, pk=None):
        return Response({"message": "Method patch"})

    def delete(self, request, pk=None):
        return Response({"message": "Method delete"})


class HelloViewSet(viewsets.ViewSet):
    serializers_class = serializers.HelloSerializer

    def list(self, request):

        an_viewSet = [
            "Hello django 1 view set",
            "Hello django 2 view set",
            "Hello django 3 view set"
        ]

        return Response({"message": "Hello django View Set", "an_viewSet": an_viewSet})

    def create(self, request):
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid:
            name = serializer.data.get('name')
            message = "Hello {0}".format(name)
            return Response({"message": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrive(self, request, pk=None):
        return Response({"message": "get data of a specific object"})

    def update(self, request, pk=None):
        return Response({"message": "Method put"})

    def partial_update(self, request, pk=None):
        return Response({"message": "Method for update some data"})

    def destroy(self, request, pk=None):
        return Response({"message": "Method delete"})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles create and update user also search"""

    serializer_class = serializers.UserSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username", "email",)


# class LoginViewSet(viewsets.ViewSet):
#     """Handles Login session by check email and password then return token"""
#     serializer_class = AuthTokenSerializer
#
#     def create(self, request):
#         return ObtainAuthToken().post(request)
#
#     # def post(self,request):
#     #     return Response({
#     #         "token":TokenAuthentication.objects.create(user)[1]
#     #     })

# class RegisterApi(generics.GenericAPIView):
#     serializer_class = serializers.RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)[1]
#         })

# class LoginViewSet(viewsets.ViewSet):
#     """Checks email and password and returns an auth token."""
#
#     serializer_class = AuthTokenSerializer
#
#     def create(self, request):
#         """Use the ObtainAuthToken APIView to validate and create a token."""
#
#         return ObtainAuthToken().post(request)

class LoginApi(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        # print(serializer, request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginApi, self).post(request, format=None)


class ProfileFeedViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileFeedSerializer
    queryset = models.ProfileFeedItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("status_text",)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

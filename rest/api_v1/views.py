from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, FullUserSerializer, PasswordSerializer, \
    ChangePasswordSerializer, SuperUserAccessSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from django.http import Http404
# from .settings import api_settings

from rest_framework.generics import get_object_or_404

# Create your views here.

_usermodel = get_user_model()


class LocalUsersList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        all_local_users = _usermodel.objects.all()
        serializer = FullUserSerializer(all_local_users, context={'request': self.request}, many=True)
        return Response({'result': serializer.data})


class LocalUserAdd(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            saved_user = serializer.save()
        return Response({'message': 'User {} successfully created'.format(saved_user.username)},
                        status=status.HTTP_201_CREATED)


class LocalUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        local_user_instance = get_object_or_404(_usermodel.objects.all(), pk=pk)
        serializer = FullUserSerializer(local_user_instance, context={'request': self.request})
        return Response({'result': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        local_user_instance = get_object_or_404(_usermodel.objects.all(), pk=pk)
        #
        # ## check permission here
        #
        serializer = FullUserSerializer(instance=local_user_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_updated = serializer.save()
        return Response({'message': 'User {} updated successfully'.format(user_updated.username)},
                        status=status.HTTP_200_OK)


class LocalUserSetPassword(APIView):
    # admins only can set users password for user without confirmation
    # pk - user id whose password we will set
    # {'new_password': 'PassWord'}
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, format=None):
        # we must give rights to this endpoint to admins only
        local_user_instance = get_object_or_404(_usermodel.objects.all(), pk=pk)
        serializer = PasswordSerializer(data=request.data, context={'user': local_user_instance})
        if serializer.is_valid(raise_exception=True):
            local_user_instance.set_password(serializer.data["new_password"])
            local_user_instance.save()
        return Response({'message': 'Password set successfully for user {} '.format(local_user_instance.username)},
                        status=status.HTTP_200_OK)


class LocalUserChangePassword(APIView):
    # each local user can change his/her own password
    # {'current_password': 'WordPass', 'new_password': 'PassWord', 're_new_password': 'PassWord'}
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # we must give rights to access this endpoint to authenticated users

        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(serializer.data["new_password"])
            self.request.user.save()

        return Response({'message': 'Password for user {} has changed successfully'.format(self.request.user.username)},
                        status=status.HTTP_200_OK)


class LocalUserProvidingSuperUserAccess(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):
        # we must give rights to this endpoint to superusers only
        local_user_instance = get_object_or_404(_usermodel.objects.all(), pk=pk)

        serializer = SuperUserAccessSerializer(instance=local_user_instance, data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_updated = serializer.save()
        return Response({'message': 'User {} is a superuser now'.format(user_updated)},
                        status=status.HTTP_200_OK)

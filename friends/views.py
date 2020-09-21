from django.contrib.auth import get_user_model
from django.db.models import Q
from djoser.serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Invite

from.serializers import (
    PostInviteSerializer,
)

User = get_user_model()


class MeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: UserSerializer(many=True)
    })
    def friends(self, request):
        """
        Метод возвращает список друзей текущего пользователя
        """

        user_id = int(request.user.id)
        invites = [x for x in Invite.objects
                   .only("id",
                         "from_user_id",
                         "to_user_id")
                   .filter(confirmed=True)
                   .filter(Q(from_user=user_id) | Q(to_user=user_id))]

        users = set(
            [x.from_user_id for x in invites if x.to_user_id == user_id])

        users.update(
            [x.to_user_id for x in invites if x.from_user_id == user_id])

        friends = User.objects.filter(id__in=users)

        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: UserSerializer(many=True)
    })
    def input(self, request):
        """
        Метод возвращает список пользователей, от которых есть непринятые входящие заявки
        """

        user_id = request.user.id
        invites = [x for x in Invite.objects
                   .only("id",
                         "from_user_id")
                   .filter(confirmed=False, to_user=user_id)]

        users = [x.from_user_id for x in invites]

        input_users = User.objects.filter(id__in=users)

        serializer = UserSerializer(input_users, many=True)
        return Response(serializer.data)

    @action(detail=False)
    @swagger_auto_schema(responses={
        200: UserSerializer(many=True)
    })
    def output(self, request):
        """
        Метод возвращает список пользователей которым отправлены заявки
        """

        user_id = request.user.id
        invites = [x for x in Invite.objects
                   .only("id",
                         "to_user_id")
                   .filter(confirmed=False, from_user=user_id)]

        users = [x.to_user_id for x in invites]

        output_users = User.objects.filter(id__in=users)

        serializer = UserSerializer(output_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], )
    @swagger_auto_schema(
        request_body=PostInviteSerializer,
        responses={
            201: UserSerializer,
        })
    def invite(self, request):
        """
        Метод создает запрос в друзья по заданному id пользователя
        """

        try:
            user_id = int(request.data['user_id'])
            self_id = request.user.id
            users = User.objects.filter(id=user_id)
            if users.count() != 1:
                raise ValidationError("Пользователя не существует")

            invite = Invite(from_user_id=self_id, to_user_id=user_id)
            invite.clean()
            invite.save()
            res = UserSerializer(invite.to_user)
            return Response(res.data, status=201)
        except DjangoValidationError as dverror:
            return Response(
                ValidationError(dverror).get_full_details(),
                status=400)
        except ValidationError as verror:
            return Response(verror.get_full_details(), status=400)
        except KeyError:
            return Response(status=400)

    @action(detail=False, methods=['post'], )
    @swagger_auto_schema(
        request_body=PostInviteSerializer,
        responses={
            201: UserSerializer,
        })
    def accept(self, request):
        """
        Подтверждение дружбы
        """
        try:
            user_id = int(request.data['user_id'])
            users = User.objects.filter(id=user_id)
            if users.count() != 1:
                raise ValidationError("Пользователя не существует")

            invites = Invite.objects.filter(from_user_id=user_id)

            if invites.count() != 1:
                raise ValidationError("Приглашения не существует")

            invite = invites.first()
            if invite.confirmed:
                raise ValidationError("Приглашение уже принято")

            invite.confirmed = True
            invite.save()

            res = UserSerializer(invite.from_user)
            return Response(res.data, status=201)
        except DjangoValidationError as dverror:
            return Response(
                ValidationError(dverror).get_full_details(),
                status=400)
        except ValidationError as verror:
            return Response(verror.get_full_details(), status=400)
        except KeyError:
            return Response(status=400)

    @action(detail=False, methods=['post'], )
    @swagger_auto_schema(
        request_body=PostInviteSerializer,
        responses={
            201: UserSerializer,
        })
    def decline(self, request):
        """
        Отклонение запроса на дружбу
        """
        try:
            user_id = int(request.data['user_id'])
            users = User.objects.filter(id=user_id)
            if users.count() != 1:
                raise ValidationError("Пользователя не существует")

            invites = Invite.objects.filter(from_user_id=user_id)

            if invites.count() != 1:
                raise ValidationError("Приглашения не существует")

            invite = invites.first()
            if invite.confirmed:
                raise ValidationError("Приглашение уже принято")

            invite.delete()

            res = UserSerializer(invite.from_user)
            return Response(res.data, status=201)
        except DjangoValidationError as dverror:
            return Response(
                ValidationError(dverror).get_full_details(),
                status=400)
        except ValidationError as verror:
            return Response(verror.get_full_details(), status=400)
        except KeyError:
            return Response(status=400)

    @action(detail=False, methods=['post'], )
    @swagger_auto_schema(
        request_body=PostInviteSerializer,
        responses={
            200: UserSerializer,
        })
    def delete(self, request):
        """
        Отклонение запроса на дружбу
        """
        try:
            user_id = int(request.data['user_id'])
            users = User.objects.filter(id=user_id)
            if users.count() != 1:
                raise ValidationError("Пользователя не существует")

            invites = Invite.objects.filter(from_user_id=user_id)

            if invites.count() != 1:
                raise ValidationError("Приглашения не существует")

            invite = invites.first()
            if not invite.confirmed:
                raise ValidationError("Приглашение еще принято")

            invite.delete()

            res = UserSerializer(invite.from_user)
            return Response(res.data, status=200)
        except DjangoValidationError as dverror:
            return Response(
                ValidationError(dverror).get_full_details(),
                status=400)
        except ValidationError as verror:
            return Response(verror.get_full_details(), status=400)
        except KeyError:
            return Response(status=400)


class UserIdViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True)
    @swagger_auto_schema(responses={
        200: UserSerializer(many=True)
    })
    def friends(self, request, pk=None):
        """
        Метод возвращает список друзей для заданного пользователя
        """
        user_id = int(pk)
        invites = [x for x in Invite.objects
                   .only("id",
                         "from_user_id",
                         "to_user_id")
                   .filter(confirmed=True)
                   .filter(Q(from_user=user_id) | Q(to_user=user_id))]

        users = set(
            [x.from_user_id for x in invites if x.to_user_id == user_id])

        users.update(
            [x.to_user_id for x in invites if x.from_user_id == user_id])

        friends = User.objects.filter(id__in=users)

        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

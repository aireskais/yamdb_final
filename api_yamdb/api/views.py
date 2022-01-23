import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, RoleChoices, Title

from .filters import TitleFilter
from .mixins import NoSlugDeleteViewSet
from .permissions import (AdminOnly, AdminOrReadOnly, AuthorOrStaffOrReadOnly,
                          IsSelf)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitlePostSerializer, TitleReadSerializer,
                          TokenSerializer, UserSerializer)

User = get_user_model()


@permission_classes([AllowAny])
class SignUp(APIView):
    """
    Регистрирует нового пользователя, отправляет confirmation_code
    на почту и сохраняет его в объект модели User.
    """

    def send_email_and_get_code(self, username, email):
        confirmation_code = str(uuid.uuid4())
        subject = 'Ваш код верификации YamDB'
        body = (f'Привет, {username}!\n'
                f'Ваш код верификации {confirmation_code}, '
                'введите свой email и этот код, чтобы получить токен.\n'
                'Сохраните письмо, чтобы не потерять код.')
        sender = settings.EMAIL_HOST_USER
        recipient = [email]
        send_mail(subject, body, sender, recipient)
        return confirmation_code

    def check_user(self, username, email):
        """
        Если пользователь существует с указанным email, вернет True.
        """

        if username is None:
            return False
        try:
            current_user = User.objects.get(username=username)
            return current_user.email == email
        except User.DoesNotExist:
            return False

    def get_and_save_user(self, serializer, username, confirmation_code):
        current_user = get_object_or_404(User, username=username)
        current_user.confirmation_code = confirmation_code
        current_user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        confirmation_code = self.send_email_and_get_code(
            username, email
        )
        if self.check_user(username, email):
            return self.get_and_save_user(
                serializer, username, confirmation_code
            )
        serializer.save()
        return self.get_and_save_user(serializer, username, confirmation_code)


@permission_classes([AllowAny])
class Token(APIView):
    """
    Проверяет существование пользователя, сличает confirmation_code
    и выдает/обновляет токен.
    """

    def generate_token_or_error(self, request):
        if ('username' not in request.data
                or 'confirmation_code' not in request.data):
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        current_user = get_object_or_404(User, username=username)

        if str(current_user.confirmation_code) != str(confirmation_code):
            return {
                'confirmation_code': 'неверный код верификации',
            }
        refresh = RefreshToken.for_user(current_user)
        return {
            'token': str(refresh.access_token),
        }

    def post(self, request):
        data = self.generate_token_or_error(request)
        serializer = TokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data, status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    """Управление пользователями"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (AdminOnly,)

    @action(
        detail=False, methods=['get', 'patch'], permission_classes=[IsSelf]
    )
    def me(self, request):
        """
        Дополнительный ресурс, получает данные авторизованного
        пользователя и дает возможность изменить данные.
        """

        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        if user.is_user:
            request.data._mutable = True
            request.data['role'] = RoleChoices.user
            request.data._mutable = False

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.validated_data, status=status.HTTP_200_OK
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitlePostSerializer


class CategoryViewSet(NoSlugDeleteViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(NoSlugDeleteViewSet):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    permission_classes = (AdminOrReadOnly,)


class ReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrStaffOrReadOnly,)
    serializer_class = ReviewSerializer

    def get_queryset(self, title_id=None):
        title_now = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title_now.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffOrReadOnly,)

    def get_queryset(self, review_id=None, title_id=None):
        review_now = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get("title_id")
        )
        return review_now.comments.all()

    def perform_create(self, serializer):
        review_now = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get("title_id")
        )
        serializer.save(
            author=self.request.user,
            review=review_now
        )

from api.validators import validate_year
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q


class RoleChoices(models.Model):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    ROLE_CHOICES = [
        (user, 'user'),
        (moderator, 'moderator'),
        (admin, 'admin'),
    ]


class User(AbstractUser):
    """Переопределяем модель User"""

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
        blank=False
    )
    confirmation_code = models.CharField(max_length=40, null=True, blank=True)
    role = models.CharField(
        max_length=32,
        choices=RoleChoices.ROLE_CHOICES,
        default=RoleChoices.user
    )

    @property
    def is_user(self):
        return self.role == RoleChoices.user

    @property
    def is_moderator(self):
        return self.role == RoleChoices.moderator

    @property
    def is_admin(self):
        return self.role == RoleChoices.admin

    class Meta:
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(
                check=(~Q(username='me')), name='me_is_unacceptable_name'
            )
        ]


class Genre(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=200, db_index=True)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='titles',
        verbose_name='Категория',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Category(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы к произведениям"""
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        null=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Комментарии к отзывам"""
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text

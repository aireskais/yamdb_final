from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError('username me запрещен')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class PatchMethodForUserRole(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio'
        )


class TokenSerializer(serializers.Serializer):
    """Обрабатывает сгенерированный токен, чтобы выдать его в JSON"""

    token = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        author = self.context['request'].user
        request = self.context.get('request')
        title_id_request = request.parser_context['kwargs']['title_id']
        review = Review.objects.filter(
            title_id=title_id_request,
            author=author
        ).exists()
        if review and request.method == 'POST':
            raise ValidationError('1 произведение, 1 отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

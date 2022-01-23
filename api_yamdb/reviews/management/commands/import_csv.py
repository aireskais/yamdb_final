import csv

from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class Command(BaseCommand):
    help = 'импорт model'

    def handle(self, *args, **options):
        # import User model
        path = 'static/data/users.csv'
        with open(path, 'r', newline='', encoding='utf-8') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                id_user = line['id']
                username = line['username']
                email = line['email']
                role = line['role']
                bio = line['bio']
                first_name = line['first_name']
                last_name = line['last_name']
                User.objects.get_or_create(
                    id=id_user,
                    bio=bio,
                    email=email,
                    role=role,
                    first_name=first_name,
                    last_name=last_name,
                    username=username
                )
        # import Category model
        path = 'static/data/category.csv'
        with open(path, 'r', newline='', encoding='utf-8') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                name = line['name']
                slug = line['slug']
                Category.objects.get_or_create(
                    name=name,
                    slug=slug
                )
        # import Genre model
        path = 'static/data/genre.csv'
        with open(path, 'r', newline='', encoding='utf-8') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                name = line['name']
                slug = line['slug']
                Genre.objects.get_or_create(
                    name=name,
                    slug=slug
                )
        # import Title model
        path = 'static/data/titles.csv'
        with open(path, 'r', newline='', encoding='utf-8') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                name = line['name']
                year = line['year']
                category = line['category']
                Title.objects.get_or_create(
                    name=name,
                    year=year,
                    category=Category.objects.get(pk=category)
                )
        # import GenreTitle model
        path = 'static/data/genre_title.csv'
        with open(path, 'r', newline='', encoding='utf-8') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                title = line['title_id']
                genre = line['genre_id']
                GenreTitle.objects.get_or_create(
                    title=Title.objects.get(pk=title),
                    genre=Genre.objects.get(pk=genre)
                )
        # import Review model
        path = 'static/data/review.csv'
        with open(path, 'r', newline='', encoding='utf-8') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                title = line['title_id']
                text = line['text']
                author = line['author']
                score = line['score']
                pub_date = line['pub_date']
                Review.objects.get_or_create(
                    title=Title.objects.get(pk=title),
                    text=text,
                    author=User.objects.get(pk=author),
                    score=score,
                    pub_date=pub_date
                )
        # import Comment model
        path = 'static/data/comments.csv'
        with open(path, 'r', newline='', encoding='utf-8') as data:
            result = csv.DictReader(data, delimiter=',')
            for line in result:
                review = line['review_id']
                text = line['text']
                author = line['author']
                pub_date = line['pub_date']
                Comment.objects.get_or_create(
                    review=Review.objects.get(pk=review),
                    text=text,
                    author=User.objects.get(pk=author),
                    pub_date=pub_date
                )

import datetime

from rest_framework import serializers


def validate_year(value):
    if value > datetime.datetime.now().year:
        raise serializers.ValidationError(f'{value} год еще не наступил')
    return value

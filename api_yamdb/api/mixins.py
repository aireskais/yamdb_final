from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class NoSlugDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    pass

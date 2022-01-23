from django.urls import include, path

from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, SignUp, TitleViewSet, Token, UsersViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(
        'v1/auth/token/', Token.as_view(), name='get_token'
    ),
    path(
        'v1/auth/signup/', SignUp.as_view(), name='sign_up'
    ),
]

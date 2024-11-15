from django.urls import path
from lms.api.views import AuthorAPIView, AuthorDetailsAPIView, BookAPIView, BookDetailsAPIView

urlpatterns = [
    path('author', AuthorAPIView.as_view(), name='author_list_create'),
    path('author/<int:pk>', AuthorDetailsAPIView.as_view(), name='author_detail_update_delete'),
    path('book', BookAPIView.as_view(), name='author_list_create'),
    path('book/<int:pk>', BookDetailsAPIView.as_view(), name='book_detail_update_delete')
]

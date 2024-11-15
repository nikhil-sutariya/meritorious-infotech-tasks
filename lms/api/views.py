from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from lms.api.serializers import AuthorSerializer, BookSerializer
from lms.models import Author, Book
from app import utils
from lms.api import response as lms_app_response
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class AuthorAPIView(GenericAPIView):
    serializer_class = AuthorSerializer

    def get(self, request):
        try:
            queryset = utils.get_or_raise(Author, obj_id=None, error_message=None)
            serializer = self.serializer_class(queryset, many=True)
            response = {
                "success": True,
                "message": lms_app_response.getting_authors,
                "data": serializer.data
            }

        except Exception as e:
            response = {
                "success": False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            response = {
                'success': True,
                'message': lms_app_response.author_added,
                'data': serializer.data
            }
        
        except Exception as e:
            response = {
                'success': False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                'data': None
            }

            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status = status.HTTP_201_CREATED)
     
class AuthorDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    
    def get(self, request, pk):
        try:
            author = utils.get_or_raise(Author, pk, lms_app_response.author_not_exists)
            serializer = self.get_serializer(author)
            response = {
                "success": True,
                "message": lms_app_response.author_data,
                "data": serializer.data
            }

        except Exception as e:
            response = {
                "success": False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        try:
            author = utils.get_or_raise(Author, pk, lms_app_response.author_not_exists)
            data = request.data
            serializer = self.serializer_class(author, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {
                'success': True,
                'message': lms_app_response.author_updated,
                'data': serializer.data
            }
        
        except Exception as e:
            response = {
                'success': False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                'data': None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            author = utils.get_or_raise(Author, pk, lms_app_response.author_not_exists)
            author.delete()
            response = {
                'success': True,
                'message': lms_app_response.author_deleted,
                'data': None
            }
        
        except Exception as e:
            response = {
                'success': False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                'data': None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(response, status=status.HTTP_200_OK)

class BookAPIView(GenericAPIView):
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ['author__name', 'available']
    search_fields = ['title', 'author__name']

    def get(self, request):
        try:
            books = utils.get_or_raise(Book, obj_id=None, error_message=None)
            books = self.filter_queryset(books)
            paginator = Paginator(books, 10)
            page_number = request.GET.get('page', 1)
            if page_number:
                page = paginator.get_page(page_number)
                serializer = self.serializer_class(page.object_list, many=True)
                response = {
                    "success": True,
                    "message": lms_app_response.getting_books,
                    "count": paginator.count,
                    "page_number": page.number,
                    "total_pages": paginator.num_pages,
                    "data": serializer.data
                }

            else: 
                serializer = self.serializer_class(books, many=True)

                response = {
                    "success": True,
                    "message": lms_app_response.getting_books,
                    "data": serializer.data
                }

        except Exception as e:
            response = {
                "success": False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            response = {
                'success': True,
                'message': lms_app_response.book_added,
                'data': serializer.data
            }
        
        except Exception as e:
            response = {
                'success': False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                'data': None
            }

            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status = status.HTTP_201_CREATED)
     
class BookDetailsAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    
    def get(self, request, pk):
        try:
            book = utils.get_or_raise(Book, pk, lms_app_response.book_not_exists)
            serializer = self.get_serializer(book)
            response = {
                "success": True,
                "message": lms_app_response.book_data,
                "data": serializer.data
            }

        except Exception as e:
            response = {
                "success": False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, pk, *args, **kwargs):
        try:
            book = utils.get_or_raise(Book, pk, lms_app_response.book_not_exists)
            data = request.data
            serializer = self.serializer_class(book, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {
                'success': True,
                'message': lms_app_response.book_updated,
                'data': serializer.data
            }
        
        except Exception as e:
            response = {
                'success': False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                'data': None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            book = utils.get_or_raise(Book, pk, lms_app_response.book_not_exists)
            book.delete()
            response = {
                'success': True,
                'message': lms_app_response.book_deleted,
                'data': None
            }
        
        except Exception as e:
            response = {
                'success': False,
                "message": lms_app_response.error_message,
                "error_message": str(e),
                'data': None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(response, status=status.HTTP_200_OK)

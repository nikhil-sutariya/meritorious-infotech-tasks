from rest_framework.serializers import ModelSerializer, CharField
from lms.models import Author, Book
from app import utils
from lms.api import response as lms_app_response

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(ModelSerializer):
    author_id = CharField(required=False)

    class Meta:
        model = Book
        fields = ["id", "title", "author_id", "published_date", "isbn", "available"]
    
    def create(self, validated_data):
        author_id = validated_data.pop('author_id')
        if not author_id:
            raise ValueError(lms_app_response.author_id_required)
        author = utils.get_or_raise(Author, author_id, lms_app_response.author_not_exists)
        validated_data['author'] = author
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('author_id'):
            del data['author_id']
        data['author'] = {
            "id": instance.author.id,
            "name": instance.author.name
        }
        return data

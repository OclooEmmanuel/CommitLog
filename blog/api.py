from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .serializers import PostSerialiser, CommentSerializer
from .models import Post, Comment

@api_view(['GET'])
def post_list_api(request):
    posts = Post.objects.all()
    serializers = PostSerialiser(posts, many =True)
    return Response(serializers.data)


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the logged-in user as the author
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Ensure only the author can update the post
        if self.get_object().author != self.request.user:
            raise PermissionError("You are not allowed to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure only the author can delete the post
        if instance.author != self.request.user:
            raise PermissionError("You are not allowed to delete this post.")
        instance.delete()

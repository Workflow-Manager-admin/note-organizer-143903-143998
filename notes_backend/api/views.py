from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets, filters
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import Note
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    NoteSerializer,
)
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# Health endpoint for sanity check
@api_view(['GET'])
def health(request):
    """Check if server is up."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class UserRegisterView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

# PUBLIC_INTERFACE
class UserLoginView(APIView):
    """
    API endpoint for user login.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "Login successful", "token": token.key, "username": user.username},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class UserLogoutView(APIView):
    """
    API endpoint for logging out the current user.
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        # Also delete the token
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for notes, with support for filtering and search.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "content", "folder"]
    filterset_fields = ["is_favorite", "is_archived", "folder"]

    def get_queryset(self):
        # Only return notes owned by the currently logged in user
        user = self.request.user
        queryset = Note.objects.filter(owner=user)
        # Optionally filter by search query
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(content__icontains=q)
        return queryset.order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

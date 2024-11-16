from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .serializers import CurrentUserSerializer
from .permissions import IsActiveUser


@api_view(['GET'])
@permission_classes([AllowAny])
def root_route(request):
    """
    Provides a welcome message and documentation link for the API.
    """
    return Response({
        "message": "Welcome to the Blog API!",
        "description": (
            "This is the backend API for the blog platform, providing endpoints for "
            "user management, blog posts, comments, likes, and more."
        ),
        "documentation": (
            "Visit /docs/ for more details on the available API endpoints."
        )
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def docs_route(request):
    return Response({
        "title": "Blog API Documentation",
        "description": "This API provides endpoints for managing blog posts, profiles, likes, follows, and comments.",
        "authentication": {
            "JWT Authentication": {
                "login": "/api/token/",
                "refresh": "/api/token/refresh/",
                "verify": "/api/token/verify/",
                "logout": "/api/token/blacklist/"
            }
        },
        "general_endpoints": {
            "root": {
                "url": "/",
                "Method": ["GET"],
                "Description": "Provides a welcome message and link to API documentation."
            },
            "documentation": {
                "url": "/docs/",
                "Method": ["GET"],
                "Description": "Provides documentation for the API endpoints."
            },
            "current_user": {
                "url": "/current-user/",
                "Method": ["GET"],
                "Description": "Retrieve details for the currently authenticated user."
            },
            "logout": {
                "url": "/logout/",
                "Method": ["POST"],
                "Description": "Log out the user by blacklisting the refresh token."
            },
        },
        "profiles_endpoints": {
            "user_registration": {
                "url": "/profiles/register/",
                "Method": ["POST"],
                "Description": "Register a new user account."
            },
            "profile_list": {
                "url": "/profiles/",
                "Method": ["GET"],
                "Description": "Retrieve a list of all user profiles."
            },
            "profile_details": {
                "url": "/profiles/<int:pk>/",
                "Method": ["GET", "PUT", "DELETE"],
                "Description": "Retrieve, update, or delete a specific user profile."
            },
            "password_reset": {
                "url": "/profiles/reset_password/",
                "Method": ["POST"],
                "Description": "Send a password reset email to the specified email address."
            },
            "password_reset_confirm": {
                "url": "/profiles/reset_password_confirm/",
                "Method": ["POST"],
                "Description": "Confirm a new password for the user."
            },
            "change_password": {
                "url": "/profiles/change_password/",
                "Method": ["POST"],
                "Description": "Change the password for the authenticated user."
            },
        },
        "posts_endpoints": {
            "post_list_create": {
                "url": "/posts/",
                "Method": ["GET", "POST"],
                "Description": "Retrieve a list of all blog posts or create a new post."
            },
            "post_details": {
                "url": "/posts/<int:pk>/",
                "Method": ["GET", "PUT", "DELETE"],
                "Description": "Retrieve details for a specific blog post."
            },
            "user_posts": {
                "url": "/posts/user/<int:user_id>/",
                "Method": ["GET"],
                "Description": "Retrieve a list of blog posts by a specific user."
            },
            "category_list": {
                "url": "/posts/categories/",
                "Method": ["GET"],
                "Description": "Retrieve a list of all blog post categories."
            },
            "tag_list": {
                "url": "/posts/tags/",
                "Method": ["GET"],
                "Description": "Retrieve a list of all blog post tags."
            },
        },
        "likes_endpoints": {
            "list_create_likes": {
                "url": "/likes/",
                "Method": ["GET", "POST"],
                "Description": "Retrieve a list of all likes or create a new like."
            },
            "like_details": {
                "url": "/likes/<int:pk>/",
                "Method": ["GET", "DELETE"],
                "Description": "Retrieve or delete a specific like."
            },
        },
        "follows_endpoints": {
            "create_follow": {
                "url": "/follows/",
                "Method": ["POST"],
                "Description": "Follow a user."
            },
            "delete_follow": {
                "url": "/follows/<int:pk>/",
                "Method": ["DELETE"],
                "Description": "Unfollow a user."
            },
        },
        "comments_endpoints": {
            "list_create_comments": {
                "url": "/comments/",
                "Method": ["GET", "POST"],
                "Description": "Retrieve a list of all comments or create a new comment."
            },
            "comment_details": {
                "url": "/comments/<int:pk>/",
                "Method": ["GET", "PUT", "DELETE"],
                "Description": "Retrieve details for a specific comment."
            },
        }
    })


class CurrentUserView(RetrieveAPIView):
    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticated, IsActiveUser]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    View for logging out the user by blacklisting the refresh token.
    """

    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

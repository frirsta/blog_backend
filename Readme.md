# Blog Project

# Overview

This repository contains the backend of the blog project built with Django REST Framework. It serves as the API for the frontend, providing functionalities such as user authentication, post creation, commenting, liking, following, and more.

- [Overview](#overview)
- [Features](#features)
- [Project Management](#project-management)
- [Technologies](#technologies)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [JWT Authentication](#jwt-authentication)
- [Testing](#testing)

[**Live Link**](https://frirsta-blog-frontend-bfdde69332c7.herokuapp.com/login)

[**Frontend Repository**](https://github.com/frirsta/blog_frontend)

# Features

### Authentication & Authorization

- JWT Authentication with Simple JWT.

- Login, Logout, and Token Refresh are implemented.

- Tokens are rotated and blacklisted after use for added security.

- The authentication backend uses case-insensitive login.

### User Profiles:

- **User Registration:** Users can create an account.

- **Profile Management:** Users can update their profile details, including profile picture, cover image, bio, website and location.

- **Account Deletion:** Users can delete their account.

- **Password Management:** Users can change or reset their password.

### Blog Posts:

- **Create, Read, Delete** functionalities for posts.

- Posts can have images, a title, text content, tags, and a category.

- Uploaded images are stored in Cloudinary through the Django backend.

### Comments and Likes:

- Users can like posts and view posts they have liked on their profile page.

- Users can comment on posts.

### Social Features:

- Users can follow/unfollow others and see followers and following lists.

# Project Management

I have used Github issues and Github project board for project management.

### Agile methodology

- **Must Have** - Are the issues that have to be top priority.
- **Should have** - Are second priority.
- **Could have** - Third priority.
- **Won't have** - Will not be in the project.

  The Won't have label is for long term use in the project and has not been

<img src="./assets/project_board.png">
<img src="./assets/issues.png">

# Technologies

## Core Frameworks & Libraries

- Django
- Django Rest framework

## Database

- PostgreSQL

## Media Storage

- Cloudinary

## Email Services

- Brevo

<img src="./assets//technologies.png">

# Setup

1. Clone the repository

2. Install backend dependencies:

- Set up a virtual environment:

  ```bash
  Source activate bin/local/myenv
  ```

- Install required Python packages:

  ```bash
   pip install -r requirements.txt
  ```

3. Install frontend dependencies:

   ```bash
   npm install
   ```

## Environment Variables

Create a .env file in the root directory with the following keys:

### Debug

- DEBUG=True

### Django secret key

- SECRET_KEY=your_secret_key

### Database URL

- DATABASE_URL=your_database_url

### Cloudinary configuration

- CLOUDINARY_CLOUD_NAME=your_cloud_name
- CLOUDINARY_API_KEY=your_api_key
- CLOUDINARY_API_SECRET=your_api_secret

### Email configuration (Brevo)

- EMAIL_HOST_USER=your_email
- EMAIL_HOST_PASSWORD=your_password
- DEFAULT_FROM_EMAIL=your_default_from_email

# API Endpoints

## Authentication

### JWT Authentication

- **Login**:

  - **URL**: `/api/token/`
  - **Method**: POST
  - **Description**: Obtain JWT access and refresh tokens by providing valid user credentials.

- **Refresh Token**:

  - **URL**: `/api/token/refresh/`
  - **Method**: POST
  - **Description**: Refresh the access token using the refresh token.

- **Verify Token**:

  - **URL**: `/api/token/verify/`
  - **Method**: POST
  - **Description**: Verify if a given token is valid.

- **Logout**:
  - **URL**: `/api/token/blacklist/`
  - **Method**: POST
  - **Description**: Blacklist the refresh token to log the user out.

## General Endpoints

- **Root**:

  - **URL**: `/`
  - **Method**: GET
  - **Description**: Provides a welcome message and link to API documentation.

- **Documentation**:

  - **URL**: `/docs/`
  - **Method**: GET
  - **Description**: Provides documentation for the API endpoints.

- **Current User**:
  - **URL**: `/current-user/`
  - **Method**: GET
  - **Description**: Retrieve details for the currently authenticated user.

## Profile Endpoints

- **User Registration**:

  - **URL**: `/profiles/register/`
  - **Method**: POST
  - **Description**: Register a new user account.

- **Profile List**:

  - **URL**: `/profiles/`
  - **Method**: GET
  - **Description**: Retrieve a list of all user profiles.

- **Profile Details**:

  - **URL**: `/profiles/<int:pk>/`
  - **Method**: GET, PUT, DELETE
  - **Description**: Retrieve, update, or delete a specific user profile.

- **Password Reset**:

  - **URL**: `/profiles/reset_password/`
  - **Method**: POST
  - **Description**: Send a password reset email to the specified email address.

- **Password Reset Confirm**:

  - **URL**: `/profiles/reset_password_confirm/`
  - **Method**: POST
  - **Description**: Confirm a new password for the user.

- **Change Password**:
  - **URL**: `/profiles/change_password/`
  - **Method**: POST
  - **Description**: Change the password for the authenticated user.

## Post Endpoints

- **Post List Create**:

  - **URL**: `/posts/`
  - **Method**: GET, POST
  - **Description**: Retrieve a list of all blog posts or create a new post.

- **Post Details**:

  - **URL**: `/posts/<int:pk>/`
  - **Method**: GET, PUT, DELETE
  - **Description**: Retrieve, update, or delete a specific blog post.

- **User Posts**:

  - **URL**: `/posts/user/<int:user_id>/`
  - **Method**: GET
  - **Description**: Retrieve a list of blog posts by a specific user.

- **Category List**:

  - **URL**: `/posts/categories/`
  - **Method**: GET
  - **Description**: Retrieve a list of all blog post categories.

- **Tag List**:
  - **URL**: `/posts/tags/`
  - **Method**: GET
  - **Description**: Retrieve a list of all blog post tags.

## Like Endpoints

- **List Create Likes**:

  - **URL**: `/likes/`
  - **Method**: GET, POST
  - **Description**: Retrieve a list of all likes or create a new like.

- **Like Details**:
  - **URL**: `/likes/<int:pk>/`
  - **Method**: GET, DELETE
  - **Description**: Retrieve or delete a specific like.

## Follow Endpoints

- **Create Follow**:

  - **URL**: `/follows/`
  - **Method**: POST
  - **Description**: Follow a user.

- **Delete Follow**:
  - **URL**: `/follows/<int:pk>/`
  - **Method**: DELETE
  - **Description**: Unfollow a user.

## Comment Endpoints

- **List Create Comments**:

  - **URL**: `/comments/`
  - **Method**: GET, POST
  - **Description**: Retrieve a list of all comments or create a new comment.

- **Comment Details**:
  - **URL**: `/comments/<int:pk>/`
  - **Method**: GET, PUT, DELETE
  - **Description**: Retrieve, update, or delete a specific comment.

# JWT Authentication

The project uses JWT-based authentication to manage user sessions. This is implemented using Django REST Framework SimpleJWT, but with enhanced customizations to ensure security and proper user management.

### Key Customizations:

1. Custom JWT Authentication Class

- A custom CustomJWTAuthentication class that extends the default JWTAuthentication from SimpleJWT.
- This class checks if the user associated with the token is active before granting access.
- If a user account is disabled, a 403 PermissionDenied error is returned with the message "User account is disabled."

2. Active User Check (IsActiveUser Permission)

- A custom permission class `IsActiveUser` ensures that only active users can access the API endpoints protected by this permission.
- This provides an additional layer of protection, even if the user’s token is valid but the account has been deactivated.

#### Configuration

In settings.py, the authentication and permission classes have been updated as follows:

```python
 REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'blog.authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'blog.permissions.IsActiveUser',
    ),

}
```

##### Custom Classes

- CustomJWTAuthentication:
- Located in blog/authentication.py.
- Overrides get_user method to check if the user is active.

```python
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        if not user.is_active:
            raise PermissionDenied("User account is disabled.")
        return user
```

##### IsActiveUser Permission:

- Located in blog/permissions.py.
- Ensures the request is made by an active user.

```python
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_active:
            raise PermissionDenied("User account is disabled.")
        return True
```

#### Updated Registration Flow

- During user registration, the backend no longer issues tokens directly using the `for_user` method due to a security vulnerability in versions of `djangorestframework-simplejwt` <= 5.3.1.
- Users register through the `/profiles/register/` endpoint, and the frontend handles logging in the user separately after a successful registration by making a login request to obtain JWT tokens.

# Testing

### Testing the Enhanced Authentication Flow

This section verifies that the enhanced authentication system handles both active and inactive users correctly, and that the logout functionality behaves as expected.

#### Prerequisites:

- You must have a valid access token (`<your_access_token>`) and refresh token (`<your_refresh_token>`).

1. **Scenario 1: Active User Access:**

   - Verify that the user account is active (user.is_active = True).
   - Send a request to the protected endpoint:

     ```bash
     curl -X GET http://127.0.0.1:8000/current-user/ \
     -H "Authorization: Bearer <your_access_token>"
     ```

   - The response should return the user details as expected:

     ```json
     {
       "id": 11,
       "username": "testuser",
       "email": "",
       "profile_picture": "http://...",
       "cover_picture": "http://...",
       "bio": null,
       "location": null,
       "website": null,
       "first_name": "",
       "last_name": ""
     }
     ```

2. **Scenario 2: Inactive User Access:**

   - Mark the user account as inactive in the Django shell:

     ```python
     user = User.objects.get(username="testuser")
     user.is_active = False
     user.save()
     ```

   - Send the same request as above.
   - The response should indicate that the user is inactive:

     ```json
     {
       "detail": "User account is disabled.",
       "code": "user_inactive"
     }
     ```

3. **Scenario 3: Successful Logout:**

   - Ensure an active user can successfully log out:

     ```bash
     curl -X POST http://127.0.0.1:8000/logout/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"refresh": "<your_refresh_token>"}'
     ```

   - The response should confirm successful logout:

     ```json
     {
       "detail": "Successfully logged out."
     }
     ```

4. **Scenario 4: Logout Attempt by Inactive User:**

   - Try logging out with an inactive user’s refresh token:

     ```bash
     curl -X POST http://127.0.0.1:8000/logout/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_access_token>" \
     -d '{"refresh": "<your_refresh_token>"}'
     ```

   - The response should indicate that the user account is disabled:

     ```json
     {
       "detail": "User account is disabled."
     }
     ```

> Note: If any unexpected issues occur during testing, ensure that the backend server is running, and the tokens are valid and not expired.

### Removing Vulnerable Code

- Security Update: The vulnerable `for_user` method was removed to avoid potential information disclosure vulnerabilities. The login flow now uses a separate request made from the frontend, which ensures that inactive users cannot access system resources with JWT tokens.

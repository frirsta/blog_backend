# Blog Project

# Overview

This repository contains the backend of the blog project built with Django REST Framework. It serves as the API for the frontend, providing functionalities such as user authentication, post creation, commenting, liking, following, and more.

- [Overview](#overview)
- [Features](#features)
- [Project Management](#project-management)
- [Technologies](#technologies)
- [Setup](#setup)

[**Live Link**](https://frirsta-blog-frontend-bfdde69332c7.herokuapp.com/login)

[**Frontend Repository**](https://github.com/frirsta/blog_frontend)

# Features

- User Management: User signup, login, and profile management with case-insensitive usernames.
- Blog Posts: Users can create, edit, and delete their blog posts, with support for categories and tags.
- Comments and Likes: Users can like posts and comment on them.
- Social Features: Users can follow/unfollow others and see followers and following lists.
- Media Handling: Supports image upload through Cloudinary.

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

  > Source activate bin/local/myenv

- Install required Python packages:
  > pip install -r requirements.txt

3. Install frontend dependencies:
   > npm install

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

## Profiles API Endpoints

1. User Registration

   - URL: /profiles/register/
   - Method: POST

2. Profile List

   - URL: /profiles/
   - Method: GET

3. Profile Detail

   - URL: /profiles/<int:pk>/
   - Method: GET, PUT, DELETE

4. Password Reset

   - URL: /profiles/password-reset/
   - Method: POST

5. Password Reset Confirmation

   - URL: /profiles/password-reset-confirm/
   - Method: POST

6. Change Password

   - URL: /profiles/change-password/
   - Method: POST

7. Current User Profile

   - URL: /profiles/current/
   - Method: GET

### Posts API Endpoints

1. Post List & Create

   - URL: /posts/
   - Method: GET, POST

2. Post Detail

   - URL: /posts/<int:pk>/
   - Method: GET, PUT, DELETE

3. User's Posts

   - URL: /posts/user/<int:user_id>/
   - Method: GET

4. Category List

   - URL: /posts/category/
   - Method: GET

5. Tag List

   - URL: /posts/tags/
   - Method: GET

### Likes API Endpoints

1. List & Create Likes

   - URL: /likes/
   - Method: GET, POST

2. Like Detail & Delete

   - URL: /likes/<int:pk>/
   - Method: GET, DELETE

### Follows API Endpoints

1. Create Follow

   - URL: /follows/
   - Method: POST

2. Unfollow User

   - URL: /follows/<int:pk>/
   - Method: DELETE

### Comments API Endpoints

1. List and Create Comments

   - URL: /comments/
   - Method: GET and POST

2. Comment Detail, Update, and Delete

   - URL: /comments/<int:pk>/
   - Method: GET, PUT, PATCH, and DELETE

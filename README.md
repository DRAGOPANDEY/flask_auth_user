# Flask User Authentication System

## Overview

This project provides a robust user authentication system using Flask. It includes user profile management, custom authentication, JWT-based access, and encryption for sensitive data.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Virtual environment (recommended)

### Setup

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd flask_auth_system

**API Endpoints Authentication**
```
User Registration Endpoint
Endpoint: POST /api/register

Method: POST
URL: http://127.0.0.1:5000/api/register
Headers:
Content-Type: application/json
Body: Select raw and JSON format, then enter the JSON payload:
json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "Test@1234",
  "address": "123 Test St",
  "phone_number": "+1234567890",
  "profile_picture": "http://example.com/profile.jpg"
}
```
```
POST /api/login
Request Body:
json
{
  "email": "user@example.com",
  "password": "your_password"
}
Response:
json
{
  "access_token": "your_jwt_token"
}
```
```
User Management
GET /api/users

Response:
json
[
  {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "address": "encrypted_address",
    "phone_number": "encrypted_phone_number",
    "profile_picture": "profile_picture_url"
  }
]
```
```
GET /api/users/<id>

Response:
json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "address": "encrypted_address",
  "phone_number": "encrypted_phone_number",
  "profile_picture": "profile_picture_url"
}
```
```
PUT /api/users/<id>

Request Body:
json
{
  "email": "new_user@example.com",
  "username": "new_username",
  "password": "new_password",
  "address": "new_address",
  "phone_number": "new_phone_number",
  "profile_picture": "new_profile_picture_url"
}

Response:
json
{
  "message": "User profile updated successfully."
}
```
```
DELETE /api/users/delete/<id>

Response:
json
{
  "message": "User profile deleted successfully."
}
```

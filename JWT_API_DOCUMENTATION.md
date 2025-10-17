# JWT Authentication API Documentation

This document describes the JWT authentication implementation for the Simple E-Commerce Django application.

## Features Implemented

1. **JWT Authentication**: Using djangorestframework-simplejwt
2. **User Registration API**: Creates new users and returns JWT tokens
3. **User Login API**: Authenticates users and returns JWT tokens
4. **Protected APIs**: All product and category APIs now require JWT authentication
5. **Token Management**: Access token (60 min), Refresh token (7 days)

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
- **URL**: `POST /accounts/api/register/`
- **Description**: Register a new user and get JWT tokens
- **Request Body**:
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```
- **Response**:
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2025-10-17T14:00:00Z"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "message": "User created successfully"
}
```

#### 2. User Login
- **URL**: `POST /accounts/api/login/`
- **Description**: Login and get JWT tokens
- **Request Body**:
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```
- **Response**:
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_joined": "2025-10-17T14:00:00Z"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "message": "Login successful"
}
```

#### 3. Get User Profile
- **URL**: `GET /accounts/api/profile/`
- **Description**: Get current user profile (requires authentication)
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**:
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2025-10-17T14:00:00Z"
}
```

#### 4. Logout
- **URL**: `POST /accounts/api/logout/`
- **Description**: Logout and blacklist refresh token
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Response**:
```json
{
    "message": "Successfully logged out"
}
```

#### 5. Token Refresh
- **URL**: `POST /api/token/refresh/`
- **Description**: Get new access token using refresh token
- **Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Response**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 6. Token Verification
- **URL**: `POST /api/token/verify/`
- **Description**: Verify if a token is valid
- **Request Body**:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
- **Response**: `200 OK` if valid, `401 Unauthorized` if invalid

### Protected Product APIs

All the following endpoints require JWT authentication. Include the access token in the request header:
```
Authorization: Bearer <access_token>
```

#### DRF-based APIs

1. **Categories**:
   - `GET /product_management/api/drf/categories/` - List all categories
   - `POST /product_management/api/drf/categories/` - Create new category
   - `GET /product_management/api/drf/categories/{id}/` - Get category details
   - `PUT /product_management/api/drf/categories/{id}/` - Update category
   - `DELETE /product_management/api/drf/categories/{id}/` - Delete category

2. **Products**:
   - `GET /product_management/api/drf/products/` - List all products
   - `POST /product_management/api/drf/products/` - Create new product
   - `GET /product_management/api/drf/products/{id}/` - Get product details
   - `PUT /product_management/api/drf/products/{id}/` - Update product
   - `DELETE /product_management/api/drf/products/{id}/` - Delete product

#### Non-DRF APIs

1. **Categories**:
   - `GET /product_management/api/categories/` - List all categories
   - `GET /product_management/api/categories/{id}/` - Get category details

2. **Products**:
   - `GET /product_management/api/products/` - List all products
   - `GET /product_management/api/products/{id}/` - Get product details
   - `GET /product_management/api/products/category/{category_slug}/` - Get products by category

## JWT Configuration

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled (new refresh token on each refresh)
- **Blacklisting**: Enabled (old tokens are blacklisted after rotation)

## Error Responses

### Authentication Errors
```json
{
    "detail": "Authentication credentials were not provided."
}
```

```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

### Validation Errors
```json
{
    "username": ["This field is required."],
    "password": ["This field is required."]
}
```

## Usage Examples

### 1. Register a new user
```bash
curl -X POST http://127.0.0.1:8000/accounts/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/accounts/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### 3. Access protected API
```bash
curl -X GET http://127.0.0.1:8000/product_management/api/drf/products/ \
  -H "Authorization: Bearer <your_access_token>"
```

### 4. Refresh token
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<your_refresh_token>"
  }'
```

## Security Notes

1. **HTTPS**: Always use HTTPS in production
2. **Token Storage**: Store tokens securely (preferably in httpOnly cookies)
3. **Token Expiration**: Access tokens have short expiration (60 minutes)
4. **Secret Key**: Ensure SECRET_KEY is secure in production
5. **CORS**: Configure CORS_ALLOWED_ORIGINS properly for production

## Migration Notes

- All existing APIs now require authentication
- Use the registration endpoint to create new users
- Include JWT tokens in all API requests
- Frontend applications need to handle token refresh
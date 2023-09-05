# Flask Image Upload & Zoom API

This Flask-based web application provides an interface for users to upload images, authenticate using JWT tokens, and Google OAuth. It also features a zoom functionality on the uploaded images.

## Features:

1. Image Upload & Display
2. JWT-based Authentication
3. API Throttle (Rate limit)
4. Google OAuth-based Login
5. Hover-to-Zoom Functionality on Images

## Routes:

1. **Main Page & Image Upload**
   - URL: `http://localhost:5000/`
   - Description: Access the main page to upload images.

2. **Google OAuth Login**
   - URL: `http://localhost:5000/login`
   - Description: Use this route to authenticate using Google OAuth.

3. **Image Display with Zoom**
   - URL: `http://localhost:5000/display/<filename>`
   - Description: Access the uploaded image and use the hover-to-zoom functionality.

4. **Protected Route** (for JWT authentication testing)
   - URL: `http://localhost:5000/protected`
   - Method: GET
   - Headers: Authorization: Bearer YOUR_ACCESS_TOKEN
   - Description: Access this endpoint with a valid JWT token to test the JWT functionality.

(Note: Replace `<filename>` with the name of the uploaded file to access a specific image.)

## Confidentiality:

For the sake of confidentiality and security, all secret keys, including the JWT secret key and the Google OAuth client secret, have been removed from this project. Ensure to replace them with your own before running the application.

# Product Catalog API

## Overview

This is a Flask-based RESTful API for managing a product catalog. The application uses both SQL and NoSQL databases to store user and product information. User registration, authentication, and product management are among the main functionalities provided by the API.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/RaviThejaReddy/Finkraft-backend-developer-assignment.git
   cd Finkraft-backend-developer-assignment
   ```

2. Build and run the Docker containers:

   ```bash
   docker-compose up --build
   ```

   The application will be accessible at [http://localhost:6000](http://localhost:6000).

    [Postman collection](./finkart%20backend%20assignment.postman_collection.json)

## API Endpoints

### User Registration

- **Endpoint:** `/register`
- **Method:** `POST`
- **Description:** Register a new user.
- **Request Body Schema:**
  ```json
  {
      "username": "string",
      "email": "string",
      "contact_number": "string or null",
      "password": "string",
      "confirm_password": "string"
  }
  ```
- **Response:**
  - 201: User registered successfully
  - 400: Invalid request body
  - 409: Username already exists
  - 500: Exception occurred

### User Login

- **Endpoint:** `/login`
- **Method:** `POST`
- **Description:** Authenticate a user.
- **Request Body Schema:**
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response:**
  - 200: Authentication successful
  - 400: Invalid request body
  - 401: Invalid username or password

### Protected Endpoint

- **Endpoint:** `/protected`
- **Method:** `GET`
- **Description:** Access a protected resource requiring a JWT token.
- **Response:**
  - 200: Logged in as `<current_user>`

### Product Listing

- **Endpoint:** `/products`
- **Method:** `GET`
- **Description:** Retrieve a list of products.
- **Response:** List of products

### Add Product

- **Endpoint:** `/add_product`
- **Method:** `POST`
- **Description:** Add a new product (requires JWT token).
- **Request Body Schema:**
  ```json
  {
      "name": "string",
      "description": "string",
      "price": "number",
      "category": "string",
      "stock_quantity": "integer"
  }
  ```
- **Response:**
  - 201: Product added successfully
  - 200: Product updated successfully
  - 400: Invalid request body
  - 500: Failed to add/update product

### Product Details

- **Endpoint:** `/product/<product_id>`
- **Method:** `GET`
- **Description:** Retrieve details of a specific product (requires JWT token).
- **Response:**
  - 200: Product details
  - 404: Product not found
  - 500: Internal Server Error

## Development

- To run the application in debug mode:

  ```bash
  docker-compose run api flask run --host 0.0.0.0 --port 6000 --debug
  ```

## Database-Related Tasks
- **Design a simple schema for the SQL user table and NoSQL product documents.**
    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        contact_number VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```
    ```json
        {
            "id": "mongodb_object_id",
            "name": "string",
            "description": "string",
            "price": "number",
            "category": "string",
            "stock_quantity": "integer",
            "created_at":"datetime",
            "updated_at":"datetime",
        }
    ```
- **Provide basic SQL script for user table creation and NoSQL setup instructions.**
    [Link to sql script](./user.sql)
    [Link to NoSql installation via docker](./nosql_installation_docker.md)
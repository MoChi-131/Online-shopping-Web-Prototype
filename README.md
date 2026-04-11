# Online Shopping Web Prototype

An e-commerce web application built with Flask and SQLite, featuring product browsing, shopping cart functionality, and a secure payment system.

## Project Overview

This is a full-stack web application that simulates an online shopping experience. Users can browse products, filter and sort items, manage a shopping basket, and complete purchases with payment validation. The application includes form validation, session management, and a local SQLite database for storing product and user information.

## Features

- **Product Browsing**: View all available products with detailed information
- **Advanced Sorting**: Sort products by:
  - Price (low to high / high to low)
  - Name (A-Z / Z-A)
  - Type/Category (A-Z / Z-A)
- **Product Details**: View individual product information including images, descriptions, and pricing
- **Shopping Cart**: Add items to basket with quantity management
- **Cart Management**: Update quantities and remove items from basket
- **Order Total Calculation**: Real-time total price calculation
- **Payment Form**: Secure payment processing with validation for:
  - Card number (16 digits)
  - CVV (3 digits)
  - Expiry date validation
  - Address and postcode verification
  - Phone number validation (11 digits)
- **User Management**: Track user information across transactions
- **Session Management**: Persistent basket across browsing sessions

## Tech Stack

- **Backend**: Python with Flask framework
- **Database**: SQLite (data.sqlite3)
- **Frontend**: HTML templates with Bootstrap styling
- **Forms**: Flask-WTF for form validation and rendering
- **Database ORM**: SQLAlchemy with Flask-Migrate for migrations
- **Session Management**: Flask-Session with filesystem storage
- **Bootstrap**: Flask-Bootstrap for responsive UI components

## Project Structure

```
Online-shopping-Web-Prototype/
├── index.py                 # Main Flask application
├── data.sqlite3            # SQLite database file
├── venv.zip                # Python virtual environment
├── instance/               # Flask instance folder
├── flask_session/          # Session storage directory
├── static/                 # Static files (CSS, JavaScript, images)
├── templates/              # HTML templates
│   ├── index.html         # Product listing page
│   ├── detail.html        # Product detail page
│   ├── basket.html        # Shopping cart page
│   └── payment.html       # Payment/checkout page
└── __pycache__/           # Python cache files
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Step 1: Extract Virtual Environment
```bash
unzip venv.zip
```

### Step 2: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install flask flask-bootstrap flask-wtf flask-session flask-sqlalchemy flask-migrate
```

### Step 4: Initialize Database
```bash
python index.py
```

The database tables will be created automatically on first run.

## Usage

### Running the Application
```bash
python index.py
```

The application will start at http://localhost:5000

### Application Flow

1. **Home Page** (/): Browse all products with sorting options
2. **Product Details** (/detail/<id>): View product information and add to basket
3. **Shopping Basket** (/basket/<item_id>/<update>): Review cart items and adjust quantities
4. **Payment** (/payment/<sum>): Complete purchase with payment information

## Database Models

### Item Model
```
- id: Product identifier (Primary Key)
- name: Product name (unique, max 40 chars)
- type: Product category (max 40 chars)
- price: Product price (integer)
- picture: Product image URL (max 200 chars)
- detail: Product description (max 1000 chars)
```

### User Model
```
- id: User identifier (Primary Key)
- name: User name (unique, max 16 chars)
```

## Validation Rules

| Field | Rule |
|-------|------|
| Card Number | Exactly 16 digits |
| CVV | Exactly 3 digits |
| Expiry Date | Must not be expired |
| Address | Minimum 6 characters |
| Postcode | Exactly 8 characters |
| Phone Number | Exactly 11 digits |

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET, POST | Product listing with sorting |
| `/detail/<int:id>` | GET, POST | Product details and add to basket |
| `/basket/<int:item_id>/<int:update>` | GET, POST | Shopping cart management |
| `/payment/<int:sum>` | GET, POST | Payment processing |

## Implementation Details

### Forms
- **SortForm**: Sort options (price, name, type - ascending/descending)
- **Quantity**: Add to cart with quantity input
- **Basket_AddDrop**: Modify cart quantities
- **PayForm**: Payment information with comprehensive validation

### Key Functions
- `append_order()`: Add or update items in basket
- `total()`: Calculate cart total
- `quantity_check_append()`: Validate and add quantity
- `validate_*()`: Custom validators for payment fields

### Session Management
- Session stored in filesystem (`/flask_session`)
- Basket initialized on first request
- Persistent across page navigation

## Known Limitations

- Uses SQLite (suitable for prototyping, not production)
- No authentication system
- Payment form validates data only, doesn't process actual payments
- Cart data lost when session expires
- No product recommendations algorithm implemented
- No order history tracking

## Future Enhancements

- User registration and login
- Product search and advanced filtering
- User order history
- Real payment gateway integration (Stripe/PayPal)
- Product similarity recommendations
- Admin dashboard
- Email notifications
- Product reviews and ratings
- Wishlist functionality
- Discount and coupon system

---

**Author**: MoChi-131  
**Repository**: https://github.com/MoChi-131/Online-shopping-Web-Prototype

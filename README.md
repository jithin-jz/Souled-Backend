<div align="center">

# 🛍️ Souled Store - Backend API

### Modern E-Commerce Platform Built with Django REST Framework

[![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Production-ready REST API** powering a full-featured e-commerce experience with JWT authentication, Stripe payments, and cloud media storage.

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Deployment](#-deployment)

</div>

---

## ✨ Features

### 🔐 Authentication & Security

- **JWT Cookie Authentication** - Secure, HttpOnly cookies with automatic refresh
- **Google OAuth Integration** - One-tap login with Google
- **Rate Limiting** - Protection against brute force attacks (3/h registration, 5/15m login)
- **Staff-Only Permissions** - Product mutations restricted to admin users
- **CSRF & CORS Protection** - Production-ready security defaults

### 🛒 E-Commerce Core

- **Product Catalog** - Full CRUD with search, filters, and categories
- **Shopping Cart** - Persistent, database-backed cart with quantity controls
- **Wishlist** - Save items for later
- **Order Management** - Complete order lifecycle with status tracking
- **Address Management** - Multiple shipping addresses per user
- **Stock Management** - Real-time inventory tracking with validation

### 💳 Payment Processing

- **Stripe Checkout** - Secure card payments with hosted checkout
- **Cash on Delivery** - Traditional COD support
- **Webhook Integration** - Automatic payment status sync
- **Fallback Verification** - Manual payment verification endpoint

### 📦 Infrastructure

- **Cloudinary Integration** - Cloud-based media storage and CDN
- **OpenAPI Documentation** - Auto-generated Swagger UI and ReDoc
- **Database Optimization** - Connection pooling and query optimization
- **Bulk Import** - Command-line tool for product catalog seeding

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.11+
PostgreSQL 13+
Cloudinary Account
Stripe Account (test mode)
```

### Installation

1. **Clone and Setup**

   ```bash
   git clone <your-repo-url>
   cd sBackend
   python -m venv .venv
   source .venv/Scripts/activate  # Windows: .venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**

   Create `.env` file:

   ```env
   # Django
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database
   DATABASE_URL=postgresql://user:password@localhost:5432/souled_db

   # Cloudinary
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret

   # Stripe
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_WEBHOOK_SECRET=whsec_...

   # OAuth
   GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com

   # Frontend
   FRONTEND_URL=http://localhost:5173
   ```

4. **Database Setup**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py import_products  # Optional: seed sample data
   ```

5. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

   🎉 API running at `http://localhost:8000`

---

## 📚 API Documentation

### Interactive Docs

- **Swagger UI**: http://localhost:8000/docs/
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI Schema**: http://localhost:8000/schema/

### Key Endpoints

#### 🔐 Authentication

```
POST   /api/register/          Create new account
POST   /api/login/             Email/password login
POST   /api/google/            Google OAuth login
POST   /api/logout/            Clear session
GET    /api/me/                Current user profile
POST   /api/refresh/           Refresh access token
```

#### 🛍️ Products

```
GET    /api/products/          List products (with filters)
POST   /api/products/create/   Create product (staff only)
GET    /api/products/:id/      Product details
PUT    /api/products/:id/      Update product (staff only)
DELETE /api/products/:id/      Delete product (staff only)
```

#### 🛒 Cart & Wishlist

```
GET    /api/cart/              Get cart
POST   /api/cart/add/          Add to cart
PATCH  /api/cart/update/:id/   Update quantity
DELETE /api/cart/remove/:id/   Remove item

GET    /api/cart/wishlist/     Get wishlist
POST   /api/cart/wishlist/add/ Add to wishlist
DELETE /api/cart/wishlist/remove/:id/
```

#### 📦 Orders

```
POST   /api/orders/create/     Create order (COD or Stripe)
GET    /api/orders/my/         Order history
GET    /api/orders/verify-payment/?session_id=...
POST   /api/orders/webhook/    Stripe webhook (internal)
```

#### 🏢 Admin

```
GET    /api/panel/users/       List all users
GET    /api/panel/dashboard/   Dashboard stats
GET    /api/orders/admin/all/  All orders
PATCH  /api/orders/:id/status/ Update order status
```

---

## 🏗️ Project Structure

```
sBackend/
├── accounts/           # User auth, JWT, Google OAuth
├── products/           # Product catalog & management
├── cart/              # Shopping cart & wishlist
├── orders/            # Order processing & Stripe
├── panel/             # Admin dashboard APIs
├── store/             # Project settings & config
├── utils.py           # Shared validators
├── products.json      # Sample product data
└── requirements.txt   # Python dependencies
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test products
python manage.py test orders

# With coverage
coverage run --source='.' manage.py test
coverage report
```

**Test Coverage**: 11 tests covering critical flows (product permissions, order creation)

---

## 🔒 Security Features

✅ **Rate Limiting** - Prevents brute force attacks  
✅ **Staff-Only Mutations** - Product CRUD restricted to admins  
✅ **CSRF Protection** - Cross-site request forgery prevention  
✅ **CORS Configuration** - Controlled cross-origin access  
✅ **HttpOnly Cookies** - XSS-resistant token storage  
✅ **Input Validation** - Comprehensive serializer validation  
✅ **SQL Injection Protection** - Django ORM safety

---

## 🚢 Deployment

### Pre-Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure production `ALLOWED_HOSTS`
- [ ] Enable secure cookies (`SESSION_COOKIE_SECURE=True`)
- [ ] Update `CORS_ALLOWED_ORIGINS` to production frontend
- [ ] Set up SSL/TLS certificates
- [ ] Configure Stripe webhook URL in dashboard
- [ ] Set up database backups
- [ ] Configure error monitoring (Sentry recommended)
- [ ] Run security audit: `python manage.py check --deploy`

### Recommended Stack

- **Application Server**: Gunicorn or uWSGI
- **Reverse Proxy**: Nginx
- **Database**: PostgreSQL (managed service)
- **Media Storage**: Cloudinary
- **Monitoring**: Sentry for errors, CloudWatch for logs

---

## 🛠️ Tech Stack

| Category           | Technology                     |
| ------------------ | ------------------------------ |
| **Framework**      | Django 5.2.8, DRF 3.16.1       |
| **Authentication** | SimpleJWT, Google OAuth        |
| **Database**       | PostgreSQL                     |
| **Media Storage**  | Cloudinary                     |
| **Payments**       | Stripe Checkout                |
| **API Docs**       | drf-spectacular                |
| **Security**       | django-ratelimit, CORS headers |

---

## 📝 Environment Variables

| Variable                | Description                      | Required |
| ----------------------- | -------------------------------- | -------- |
| `SECRET_KEY`            | Django secret key                | ✅       |
| `DEBUG`                 | Debug mode (False in production) | ✅       |
| `DATABASE_URL`          | PostgreSQL connection string     | ✅       |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name            | ✅       |
| `CLOUDINARY_API_KEY`    | Cloudinary API key               | ✅       |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret            | ✅       |
| `STRIPE_SECRET_KEY`     | Stripe secret key                | ✅       |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret    | ✅       |
| `GOOGLE_CLIENT_ID`      | Google OAuth client ID           | ✅       |
| `FRONTEND_URL`          | Frontend application URL         | ✅       |
| `ALLOWED_HOSTS`         | Comma-separated allowed hosts    | ✅       |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Stripe](https://stripe.com/)
- [Cloudinary](https://cloudinary.com/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)

---

<div align="center">

**Built with ❤️ by JITHIN**

⭐ Star this repo if you find it helpful!

</div>

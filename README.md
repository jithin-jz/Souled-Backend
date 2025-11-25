# Store Backend – Django REST API

Modern, cloud-ready e-commerce backend built with Django REST Framework. It powers catalog browsing, persistent carts and wishlists, and a Stripe-backed checkout pipeline, all secured by cookie-based JWT sessions. The API is optimized for SPA clients (default CORS origin `http://localhost:5173`) and stores media on Cloudinary.

---

## Table of Contents
- [Highlights](#highlights)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Surface](#api-surface)
- [Stripe & Webhooks](#stripe--webhooks)
- [Testing & Quality](#testing--quality)
- [Deployment Checklist](#deployment-checklist)
- [Roadmap](#roadmap)

---

## Highlights
- Email-first custom user model with access + refresh JWT cookies managed via SimpleJWT and Google One-Tap login.
- Product catalog with search, category, and price filters plus a bulk import command that pushes imagery to Cloudinary.
- Authenticated cart & wishlist APIs with quantity controls, deduplication, and clear validation messaging.
- Checkout pipeline supporting Cash on Delivery and Stripe Checkout, including webhook + fallback verification to keep order status in sync.
- Opinionated security defaults: CSRF & CORS configuration, cookie authentication, and environment-driven secrets.

---

## System Architecture
**Core services**
- `accounts`: User model, JWT cookie authentication (`CookieJWTAuthentication`), Google login, and session helpers.
- `products`: CRUD APIs, slug generation, and a management command (`import_products`) that hydrates the catalog from `products.json`.
- `cart`: Cart and wishlist resources linked to authenticated users with quantity tracking.
- `orders`: Order placement, address management, Stripe Checkout session creation, webhook handling, and fallback verification.
- `store`: Global settings, middleware, URL router, and integration glue (CORS, Cloudinary, Stripe, SimpleJWT).

**Request flow**
1. Client authenticates via `/api/auth/login/` (or `register/` or `google/`), receiving JWT cookies.
2. Subsequent requests include cookies (`credentials: 'include'`), allowing `CookieJWTAuthentication` to resolve the user.
3. Shopping flows hit `products`, `cart`, and `wishlist` endpoints; the order payload is submitted to `/api/orders/create/`.
4. Stripe webhooks call back into `/api/orders/webhook/` to finalize payment state; `verify-payment/` offers a manual fallback.

---

## Tech Stack
- Python 3.11+, Django 5, Django REST Framework
- SimpleJWT (cookie transport), `django-cors-headers`
- Cloudinary via `django-cloudinary-storage`
- Stripe Checkout + Webhooks
- PostgreSQL (via `DATABASE_URL`, swapable with any Django-supported DB)

---

## Project Structure
```
store/           Django project (settings, urls, wsgi/asgi)
accounts/        Custom user model + auth endpoints
products/        Product catalog, serializers, import command
cart/            Cart & wishlist models/APIs
orders/          Orders, addresses, Stripe integration
products.json    Seed data used by import_products command
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL (or swap `DATABASE_URL` to SQLite for local experiments)
- Cloudinary account and API keys
- Stripe account with test keys

### Installation
```bash
git clone <repo-url>
cd sBackend
python -m venv .venv
source .venv/Scripts/activate        # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Environment Setup
Create `.env` in the repo root:
```
SECRET_KEY=django-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:pass@localhost:5432/store

CLOUDINARY_CLOUD_NAME=xxx
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx

STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

GOOGLE_CLIENT_ID=<oauth-client-id>.apps.googleusercontent.com
FRONTEND_URL=http://localhost:5173
```

### Database & Admin User
```bash
python manage.py migrate
python manage.py createsuperuser
```

### (Optional) Import Sample Products
`products/management/commands/import_products.py` reads `products.json`, uploads media to Cloudinary, and seeds the catalog.
```bash
python manage.py import_products
```

### Run the API
```bash
python manage.py runserver
```

---

## Configuration
- **Authentication**: SimpleJWT cookies (HttpOnly, per settings). Ensure the frontend sends requests with `credentials: 'include'`.
- **CORS**: Managed via `django-cors-headers`; defaults to `http://localhost:5173`.
- **Media**: Served from Cloudinary storage; requires the `CLOUDINARY_*` trio.
- **Payments**: `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, and `STRIPE_WEBHOOK_SECRET` must be set. Webhooks expect INR by default but can be adapted in `orders`.
- **Database**: Driven by `DATABASE_URL` (PostgreSQL recommended). Use Django-supported URLs to swap engines.

---

## API Surface
**Auth (`/api/auth/`)**
- `POST register/` – create user & issue JWT cookies.
- `POST login/` – email/password login.
- `POST google/` – Google ID token login.
- `POST logout/` – clears cookies.
- `GET me/` – current user profile (auth required).

**Products (`/api/products/`)**
- `GET /` – list products with `search`, `category`, `min_price`, `max_price`.
- `POST create/` – create product (enforce staff-only in production).
- `GET|PUT|PATCH|DELETE <pk>/` – manage a specific product.

**Cart (`/api/cart/`)**
- `GET /` – retrieve authenticated user cart with expanded product data.
- `POST add/` – payload `{product_id, quantity}`.
- `PATCH update/<item_id>/` – adjust quantity.
- `DELETE remove/<item_id>/` – remove item.

**Wishlist (`/api/cart/wishlist/`)**
- `GET /`
- `POST add/` – payload `{product_id}`; duplicates return a friendly message.
- `DELETE remove/<item_id>/`

**Orders (`/api/orders/`)**
- `POST create/` – accepts cart snapshot, address, and `payment_method` (`cod` or `stripe`); returns either a processing order or Stripe Checkout URL.
- `GET verify-payment/?session_id=...` – fallback poller for Stripe sessions.
- `POST webhook/` – Stripe webhook entrypoint.
- `GET my/` – authenticated user order history with nested items.

---

## Stripe & Webhooks
1. Start a local tunnel: `stripe listen --forward-to localhost:8000/api/orders/webhook/`.
2. Place the generated signing secret into `STRIPE_WEBHOOK_SECRET`.
3. Complete checkout using the URL returned by `orders/create/` (test mode, INR).
4. Successful payments trigger the webhook, which syncs order status; `verify-payment/` is available if the webhook is delayed.

---

## Testing & Quality
Run Django’s test runner (apps ship with `tests.py` ready for expansion):
```bash
python manage.py test
```
Add coverage for cart mutations, order flows, and webhook edge cases as the project grows.

---

## Deployment Checklist
- Set `DEBUG=False`, tighten `ALLOWED_HOSTS`, and configure HTTPS so cookies can be `Secure` and `SameSite=None` when serving a different origin.
- Provide production `DATABASE_URL`, `CLOUDINARY_*`, and Stripe keys.
- Tune database settings (`CONN_MAX_AGE`, SSL) and restrict CORS origins.
- Configure `CSRF_TRUSTED_ORIGINS` for hosted frontends.
- Rotate webhook secrets when moving between environments.

---

## Roadmap
- Enforce staff-only access for product mutations.
- Add rate limiting and email verification for new accounts.
- Expand automated test coverage for cart, order, and webhook flows.


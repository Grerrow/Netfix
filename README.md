# Netfix

A service marketplace web application built with Django that connects customers with service companies across multiple trade fields. Customers can browse, filter, and book services, while companies can list and manage their offerings.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Getting Started](#getting-started)
- [URL Routes](#url-routes)
- [Authentication](#authentication)

---

## Overview

Netfix is a peer-to-peer service marketplace where:

- **Companies** register under a specific trade field (e.g., Plumbing, Electricity, Carpentry), create service listings with hourly rates, and receive booking requests from customers.
- **Customers** register, browse all available services (filtered by field or by popularity), and submit booking requests specifying the number of hours needed. The total cost is calculated automatically.

---

## Features

- Dual-role registration: separate flows for customers and companies
- Email-based authentication (instead of username)
- Companies can create services scoped to their registered trade field
- "All in One" companies can offer services across all fields
- Service discovery: browse all services, filter by field, or view the top 10 most requested
- Booking system: customers request services with custom hours; cost is auto-calculated (`price_hour × hours`)
- Customer profile: shows age (from date of birth) and booking history
- Company profile: shows all services they have listed
- Django admin panel at `/admin_panel/`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.1.5 |
| Database | SQLite3 |
| Frontend | HTML, CSS, Bootstrap |
| Auth | Custom email-based backend + Django `ModelBackend` |

---

## Project Structure

```
netfix/                  ← Django project config (settings, root URLs)
main/                    ← Core pages: home, login, logout, profiles
users/                   ← Custom user model, registration forms, Customer & Company models
services/                ← Service listings, service requests, filtering, analytics
```

### App Responsibilities

- **`main`** — Homepage, email login/logout, customer and company profile views
- **`users`** — Custom `User` model (extends `AbstractUser`), `Customer` and `Company` one-to-one models, registration forms and views
- **`services`** — `Service` and `RequestService` models, service CRUD, booking form, field filtering, most-requested view

---

## Data Models

### User
Extends Django's `AbstractUser`. Uses **email** as the login identifier.

| Field | Type | Notes |
|---|---|---|
| `email` | EmailField | Unique; used for login |
| `is_customer` | BooleanField | Marks customer accounts |
| `is_company` | BooleanField | Marks company accounts |

### Customer
One-to-one with `User`.

| Field | Type | Notes |
|---|---|---|
| `date_of_birth` | DateField | Optional; used to display age on profile |

### Company
One-to-one with `User`.

| Field | Type | Notes |
|---|---|---|
| `field` | CharField | Trade field (Plumbing, Electricity, Carpentry, etc.) |
| `rating` | IntegerField | 0–5 reputation score |

### Service
Belongs to a `Company`.

| Field | Type | Notes |
|---|---|---|
| `name` | CharField | Max 40 characters |
| `description` | TextField | |
| `price_hour` | DecimalField | Hourly rate |
| `field` | CharField | One of 11 service categories |
| `date` | DateTimeField | Auto-updated on save |

### RequestService
Links a `Customer`, a `Service`, and a `Company`.

| Field | Type | Notes |
|---|---|---|
| `service_hours` | DecimalField | Duration requested |
| `calculated_cost` | DecimalField | `price_hour × service_hours` |
| `requested_date` | DateTimeField | Auto-set on creation |

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd netfix

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install django

# Apply migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000`.

> **Note:** `DEBUG` is set to `False` in settings. Set it to `True` for local development.

---

## URL Routes

| URL | View | Description |
|---|---|---|
| `/` | `home` | Homepage |
| `/login/` | `login_user` | Email-based login |
| `/logout/` | `logout_user` | Logout |
| `/register/` | `register` | Choose user type |
| `/register/customer/` | `CustomerSignUpView` | Customer registration |
| `/register/company/` | `CompanySignUpView` | Company registration |
| `/services/` | `list_of_services` | All services |
| `/services/create/` | `create_service` | Create a service (companies) |
| `/services/<id>/` | `single_service` | Service detail |
| `/services/<id>/request_service/` | `request_service` | Book a service (customers) |
| `/services/<field>/` | `services_per_field` | Services filtered by field |
| `/most_requested/` | `most_requested` | Top 10 most booked services |
| `/customer/<username>/` | `customer_profile` | Customer profile |
| `/company/<username>/` | `company_profile` | Company profile |
| `/admin_panel/` | Django admin | Admin interface |

---

## Authentication

Login uses **email + password** via a custom authentication backend (`main/authentication.py`). The default Django `ModelBackend` is also enabled as a fallback.

Two authentication backends are active in settings:

```python
AUTHENTICATION_BACKENDS = [
    "main.authentication.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]
```

`LOGIN_URL` is set to `/login/` and profile views are decorated with `@login_required` and `@never_cache`.

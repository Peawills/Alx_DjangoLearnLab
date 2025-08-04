# Advanced Permissions and Groups

This module implements group-based permissions to control access to book management features.

## Permissions Defined in `Book` Model
- `can_view`: View book list
- `can_create`: Add new book
- `can_edit`: Edit existing book
- `can_delete`: Delete book

## User Groups
- **Viewers**: can only view books
- **Editors**: can view, create, and edit books
- **Admins**: have full permissions including delete

## Views
Each view is protected using `@permission_required` decorator. Unauthorized access raises `PermissionDenied`.

## Setup
1. Create groups in the Django admin.
2. Assign permissions as listed above.
3. Assign users to these groups.


# HTTPS and Security Configuration

## ✅ Enforced HTTPS and Secure Cookies

- `SECURE_SSL_REDIRECT = True`: Redirects all HTTP traffic to HTTPS.
- `SECURE_HSTS_SECONDS = 31536000`: Enforces HSTS for 1 year.
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: Applies to all subdomains.
- `SECURE_HSTS_PRELOAD = True`: Eligible for preload list.
- `SESSION_COOKIE_SECURE = True`: Prevents session hijacking.
- `CSRF_COOKIE_SECURE = True`: Protects CSRF tokens during transmission.

## ✅ Security Headers

- `X_FRAME_OPTIONS = "DENY"`: Prevents clickjacking.
- `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents content sniffing attacks.
- `SECURE_BROWSER_XSS_FILTER = True`: Enables browser XSS protection.

## ✅ Deployment

We configured our Nginx server to:
- Redirect HTTP to HTTPS
- Serve over SSL using Let's Encrypt
- Set secure headers

## 🔐 Outcome

This configuration protects our users from man-in-the-middle attacks, XSS, clickjacking, and session hijacking.

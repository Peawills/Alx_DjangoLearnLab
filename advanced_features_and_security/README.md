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

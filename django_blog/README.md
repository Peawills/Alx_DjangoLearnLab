## Comment System

- Model: `Comment(post FK, author FK, content, created_at, updated_at)`
- Create: POST to `/post/<post_id>/comments/new/` — authenticated users only
- Edit: GET/POST `/comments/<comment_id>/edit/` — only comment author
- Delete: POST `/comments/<comment_id>/delete/` — only comment author
- Inline form: Post detail page shows comments and an inline form for logged-in users.
- Permissions are enforced by `LoginRequiredMixin` (create) and `UserPassesTestMixin` (edit/delete).

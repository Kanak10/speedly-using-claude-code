# Spec: Registration

## Overview
Implements user registration so visitors can create an account on Spendly. The existing `GET /register` route already renders a form with name, email, and password fields. This step adds the `POST /register` handler that validates input, hashes the password, inserts the user into the database, and redirects to the login page. This is a prerequisite for login (Step 3) and all authenticated features.

## Depends on
- Step 1 — Database Setup (users table, `get_db()`, `init_db()`)

## Routes
- `POST /register` — validates form data, creates user, redirects to login — public

No new GET routes. The existing `GET /register` route will be updated to accept both GET and POST methods.

## Database changes
No schema changes. The `users` table already has the required columns (name, email, password_hash, created_at).

New function in `database/db.py`:
- `create_user(name, email, password)` — hashes password, inserts row, returns the new user's id. Raises an exception if email already exists.
- `get_user_by_email(email)` — returns user row or None. Needed to check for duplicate emails before insert.

## Templates
- **Modify:** `templates/register.html`
  - Fix form action to use `url_for('register')` instead of hardcoded `/register`
  - Preserve submitted name and email values on validation failure (via template variables)
  - Display flash messages for success feedback

- **Modify:** `templates/base.html`
  - Add a flash message block so any page can display flash messages

## Files to change
- `app.py` — update register route to handle POST, add `app.secret_key`, import `request`, `redirect`, `url_for`, `flash`
- `database/db.py` — add `create_user()` and `get_user_by_email()` functions
- `templates/register.html` — fix form action, add value preservation, flash messages
- `templates/base.html` — add flash message rendering block

## Files to create
None.

## New dependencies
No new dependencies. Uses `werkzeug.security.generate_password_hash` (already in requirements).

## Rules for implementation
- No SQLAlchemy or ORMs — raw sqlite3 only
- Parameterised queries only — never interpolate user input into SQL
- Passwords hashed with `werkzeug.security.generate_password_hash`
- Use CSS variables from `style.css` — never hardcode hex colour values
- All templates extend `base.html`
- DB logic stays in `database/db.py` — route functions only call helpers
- Use `url_for()` for all links and form actions — never hardcode URLs
- Use Flask `flash()` for success messages, template variable `error` for validation errors
- `app.secret_key` must be set (use `os.urandom(24)` or a fixed dev key)

## Validation rules
- **Name:** required, non-empty after stripping whitespace
- **Email:** required, must contain `@` and a `.` after the `@`
- **Password:** required, minimum 8 characters
- **Duplicate email:** check before insert, show friendly error

## Definition of done
- [ ] `POST /register` with valid data creates a user in the database with a hashed password
- [ ] Submitting the form redirects to `/login` with a flash message on success
- [ ] Submitting with a blank name shows an error on the register page
- [ ] Submitting with an invalid email shows an error on the register page
- [ ] Submitting with a password under 8 characters shows an error on the register page
- [ ] Submitting with a duplicate email shows a friendly error, not a crash
- [ ] Name and email fields retain their values after a validation error
- [ ] Form action uses `url_for('register')`, not a hardcoded path
- [ ] Flash messages render correctly in `base.html` on any page
- [ ] App starts without errors on port 5001
- [ ] No raw SQL in `app.py` — all DB access goes through `database/db.py`

# Spec: Login and Logout

## Overview
This step implements user authentication functionality for the Spendly expense tracker. Users will be able to log in with their email and password, and log out of their session. This builds upon the existing user registration system (Step 2) and enables personalized features like profile management and expense tracking. The login system will use Flask sessions with secure cookie handling, and passwords will be verified against hashed values stored in the database.

## Depends on
- Step 1: Database setup (users table with email, password_hash)
- Step 2: User registration (GET /register, POST /register, create_user function)

## Routes
- `POST /login` — processes login form submission, authenticates user, sets session — access level: public
- `GET /logout` — clears user session and redirects to landing page — access level: logged-in

## Database changes
No database changes required. The existing users table (from Step 1) contains all necessary fields:
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- email (TEXT UNIQUE NOT NULL)
- password_hash (TEXT NOT NULL)
- created_at (TEXT DEFAULT (datetime('now')))

## Templates
- **Create:** None
- **Modify:**
  - `base.html` — add navigation links for profile/logout when user is logged in
  - `login.html` — add form error handling and remember login state

## Files to change
- `app.py` — add POST /login route, implement GET /logout route, add session imports and configuration
- `database/db.py` — add get_user_by_email_with_password helper function (or similar)
- `templates/base.html` — add conditional navigation for logged-in users
- `templates/login.html` — add error display for invalid credentials

## Files to create
- None

## New dependencies
No new dependencies. Will use Flask's built-in session management and werkzeug.security for password checking (already imported in db.py).

## Rules for implementation
- No SQLAlchemy or ORMs — use parameterized queries only
- Passwords verified with werkzeug.security.check_password_hash
- Use Flask session for authentication state
- Set session.permanent = False (or appropriate timeout)
- Use CSS variables from existing stylesheet — never hardcode hex values
- All templates extend base.html
- Never hardcode URLs — use url_for() in templates
- Never put DB logic in route functions — use database/db.py helpers
- Error handling: use abort() for HTTP errors, flash messages for form validation
- Always validate and sanitize inputs
- Implement proper session security (consider session configuration)

## Definition of done
A specific testable checklist. Each item must be something that can be verified by running the app:
1. [ ] User can log in with valid credentials from the registration step
2. [ ] User sees appropriate error message for invalid email/password
3. [ ] After login, user is redirected to a appropriate page (profile or landing)
4. [ ] User's name appears in navigation when logged in
5. [ ] User can log out and is redirected to landing page
6. [ ] After logout, user sees login/signup options in navigation again
7. [ ] Session expires appropriately (browser close or timeout)
8. [ ] Passwords are verified using secure hashing (not plain text comparison)
9. [ ] No SQL injection vulnerabilities (parameterized queries only)
10. [ ] Access to profile/expense routes redirects to login when not authenticated (to be implemented in later steps)
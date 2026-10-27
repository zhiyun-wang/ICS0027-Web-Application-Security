# ICS0027-Web-Application-Security
Web-Based Secure Password Manager

## Project scope

This project is a web-based password manager. Registered users will be able to
add, view, update and delete their own vault entries. A vault entry contains a
website name, account username and account password. The application will
encrypt sensitive vault data on the server before storing it in the database.

## Planned routes

| Route | Purpose |
| --- | --- |
| `/register/` | Create an account |
| `/login/` | Log in with the master password |
| `/logout/` | End the session |
| `/vault/` | List the user's entries |
| `/vault/new/` | Add an entry |
| `/vault/<id>/` | View an owned entry |
| `/vault/<id>/edit/` | Update an owned entry |
| `/vault/<id>/delete/` | Delete an owned entry |

## Planned features

- Users can manage only their own entries.
- Account usernames and passwords will be encrypted on the server before
  being stored in the database.
- The application will include authentication, secure sessions, input
  validation, and protection against CSRF, XSS, and SQL injection.

## Run locally

To run the application locally, use the following commands from the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python dev_https.py
```

The application will then be available at https://localhost:8443/.

The browser will show a warning because the development server uses a
self-signed certificate. Continue to localhost to access the application.
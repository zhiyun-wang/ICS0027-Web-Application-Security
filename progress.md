# Checkpoint 2 Progress Note

I created a basic password manager using Django. Users can register,
log in, and add, view, edit and delete their own password entries.

The application stores login passwords as Argon2 hashes. The saved account
usernames and passwords are encrypted with AES-GCM before they are stored
in the database. Users need to enter their master password to view or
change an entry.

The application uses secure session cookies and runs over HTTPS in the
development setup. I tested the main functions by adding, viewing, editing
and deleting a test entry.

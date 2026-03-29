# Lab 2

## Setup

- Flask web app
- DB (Postgres)

### Web App Structure

Pages:

- Landing Page
- Login Page
- Register Page
- Dashboard

## Flows

### Login

1. Client POSTs credentials to server (include TLS so it doesnt get intercepted)\
2. Server fetches from DB user data (username and hashed password)
3. Server hashes received password
4. Server compares new hash with stored hash, if theyre the same it responds with a session ID or JWT

## Homework

- Implement logout function
- make use of role dropdown (add it to DB)
- add a link/button to dashboard thats visible only for admins and accessible only with admin role
- 
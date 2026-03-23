# Step 02: Database Setup and Login

## Goal

Initialize DVWA database and sign in.

## Manual Steps

1. Open `http://localhost:4280/setup.php`
2. Click `Create / Reset Database`
3. After setup, open `http://localhost:4280/login.php`
4. Login with:
- username: `admin`
- password: `password`

## Why This Step Is Required

`setup.php` creates or resets DVWA tables and seed users. If you skip this, login and module behavior may fail or be inconsistent.

## Expected Result

- Setup completes without critical database errors
- Login with `admin/password` works

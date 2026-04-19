# HW3 - JWT Authentication (Fixed)

This homework extends Lab 3 by fixing three issues in the original implementation.

## What Was Fixed

### 1. Role claim missing after token refresh

The original code never embedded the user's role in the JWT payload. After a refresh, the new access token had no role claim at all.

Fix: all calls to `create_access_token` now pass `additional_claims={"role": role}`. The `/api/refresh` endpoint re-fetches the role from the database before issuing the new token.

### 2. Token revocation (`is_token_revoked`) was unused

The original logout endpoint returned 200 without doing anything. A logged-out token could still be used indefinitely.

Fix: a `revoked_jtis` set is maintained in memory. `is_token_revoked` is registered via `@jwt.token_in_blocklist_loader`, which flask-jwt-extended calls automatically on every protected route. The logout endpoint now extracts the token's `jti` claim and adds it to the set.

### 3. Demonstration of revocation blocking a request

See the Postman section below.

## How to Start

1. Copy the environment file:

   ```bash
   cp .env.example .env
   ```

2. Start the containers:

   ```bash
   docker-compose up -d --build
   ```

3. Open your browser at <http://localhost:5000>

## How to Stop

```bash
docker-compose down
```

To also delete the database volume:

```bash
docker-compose down -v
```

## Postman Collection

### Import

1. Open Postman.
2. Click **Import** (top left).
3. Select the file `HW3.postman_collection.json` from this directory.
4. The collection **JWT Auth - HW3** will appear in your sidebar.

### Collection variables

The collection uses three variables that are set automatically by the test scripts:

| Variable | Set by |
| --- | --- |
| `base_url` | Pre-configured to `http://localhost:5000` |
| `access_token` | Login and Register requests |
| `refresh_token` | Login and Register requests |

You do not need to set these manually after a successful login or register.

### Demonstrating token revocation (Requirement 3)

Follow these steps in order:

1. Run **Register** or **Login** - the access token is saved automatically to `access_token`.
2. Run **Get Profile** - you should receive your user data (200 OK).
3. Run **Logout** - the server adds your token's JTI to the revoked set.
4. Run **Get Profile** again using the same token - you should receive a 401 with `"Token has been revoked"`.
5. Optionally, run **Refresh Token** then **Get Profile** again - the new token works because it has a different JTI and was not revoked.

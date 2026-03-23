# Web Security Basics

## What This README Is For

This file covers foundational web concepts needed to understand the CSRF attack in this lab.
Read this first if you are new to cookies, sessions, tokens, or browser storage.

For CSRF-specific theory and per-level analysis, see [README-CSRF.md](README-CSRF.md).

## HTTP Is Stateless

HTTP (HyperText Transfer Protocol) is the protocol your browser uses to talk to websites.
It is stateless by default, meaning every request is independent.
Without extra mechanisms, the server forgets you after every page load and you would have to log in again on every click.

Cookies, sessions, and tokens are the mechanisms that solve this problem.

## Cookies

A cookie is a small piece of key-value data (limited to about 4 kilobytes) stored by the browser for a specific website.

Key behavior: cookies are **automatically attached** to every request your browser makes to that website.
You do not have to write any code for this. The browser does it on its own based on rules like domain, path, expiry, and security attributes.

The server can create cookies (via HTTP response headers) or JavaScript running on the page can create them.

### Cookie Security Flags

Cookies can be configured with security flags:

- `HttpOnly`: JavaScript on the page cannot read the cookie, only the browser's internal networking code can access it
- `Secure`: the cookie is only sent over HTTPS (encrypted connections)
- `SameSite`: controls whether the cookie is sent on cross-site requests (see the SameSite section below)

### SameSite Attribute

`SameSite` is a cookie attribute that controls when cookies are sent in cross-site contexts.
This is directly relevant to CSRF because it determines whether a forged request from an attacker's page will include the victim's cookies.

The server sets `SameSite` through the `Set-Cookie` response header. For example:

```
Set-Cookie: PHPSESSID=abc123; SameSite=Strict; HttpOnly; Secure
```

If the server does not set `SameSite` at all, most modern browsers default to `Lax`.

### How SameSite Decides Whether to Send a Cookie

SameSite is not about which URLs the cookie is attached to (that is what the `Domain` and `Path` cookie attributes do).
SameSite is about **who initiated the request**.

"Site" here means the registrable domain.
So `example.com` is the same site regardless of whether you are on `example.com/page1` or `app.example.com/page2`.

The question SameSite answers is: does the site you are currently on match the site the cookie belongs to?

- If you are on `example.com` and your browser sends a request to `example.com`, that is **same-site**. The cookie is sent regardless of the SameSite setting.
- If you are on `attacker.com` and something on that page triggers a request to `example.com`, that is **cross-site**. Whether the cookie is sent depends on the SameSite value.

### SameSite Values

`SameSite=Strict`:
Cookie is never sent in cross-site contexts. Strong CSRF reduction, but can impact some navigation flows.
For example, if you click a link to `example.com` from an email or from `attacker.com`, the `Strict` cookie will not be sent on that first navigation. You would appear logged out until you navigate within the site again.

`SameSite=Lax`:
Cookie is sent for same-site requests and for top-level cross-site navigations (like clicking a link), but not for cross-site form submissions or background requests.
This is the default in most modern browsers.
It blocks most CSRF attacks while still letting normal link navigation work.

`SameSite=None`:
Cookie is always sent, even in cross-site contexts. Must also include `Secure` (HTTPS only), or modern browsers reject it.
This is the most permissive setting and offers no CSRF protection from the cookie itself.

### Where These Rules Come From

These behaviors come from the HTTP cookie standard and browser security model:
- Cookie model: RFC (Request for Comments) 6265 family
- Standardization body: IETF (Internet Engineering Task Force)
- `SameSite` behavior: modern browser implementations aligned with the evolving RFC 6265bis work

Browser defaults and edge behavior can change over time, so test in the browser versions you actually support.

## Local Storage

Local storage is another way browsers store data for a website, but with different rules.

- Larger capacity (typically 5 to 10 megabytes)
- **Never sent automatically** with requests. If you want to send something from local storage to a server, your JavaScript code must explicitly read it and attach it (usually as a request header)
- No expiration. Data stays until your code deletes it or the user clears browser data
- Only JavaScript running on that specific page can access it

## Cookies vs Local Storage

The critical difference is one word: **automatically**.
Cookies are sent whether you want them to be or not.
Local storage is only sent when your code explicitly does it.

Automatic sending:
- Cookies: yes
- Local storage: no

Readable by JavaScript:
- Cookies: only if the cookie is not marked `HttpOnly`
- Local storage: always

Size limit:
- Cookies: about 4 kilobytes
- Local storage: 5 to 10 megabytes

Expiration:
- Cookies: configurable (can expire after a set time, or on browser close)
- Local storage: never expires on its own

## Sessions

A session is a server-side record that keeps track of who you are across multiple requests.
Sessions rely on cookies to work.

The flow:

1. You log in with your username and password
2. The server creates a session record containing things like your user ID, role, and login timestamp
3. The server sends your browser a session ID (a long random string) inside a cookie
4. On every following request, your browser automatically sends that cookie back
5. The server reads the session ID, looks up the matching record, and knows it is you

What sessions are useful for:

- Staying logged in without re-entering credentials on every page
- Tracking user-specific state like a shopping cart, preferences, or (in DVWA) your current security level
- Access control, so the server can check your session to decide what you are allowed to do

Your browser never stores your actual password or role.
It only holds a session ID, which is a pointer the server uses to look up your real data on its end.

### Session Cookies

A session cookie is the cookie that stores the session ID.
It usually has no long-term expiry and lives until the browser closes (or until the server invalidates the session).
It does not contain your password. It is just a pointer to server-side session state.

### What DVWA Uses

DVWA uses traditional server-side sessions.
Your browser holds a `PHPSESSID` cookie (the default session ID name in PHP), and the server looks that up to identify you as the `admin` user.

## JWT (JSON Web Token)

A JWT solves the same problem as sessions (keeping you authenticated across requests) but stores the data differently.

With sessions, the server stores your data and your browser only holds a meaningless session ID.
With a JWT, the server packs your data (user ID, role, expiration time) directly into a token and signs it with a secret key.
Your browser stores the entire token and sends it with every request.
The server does not need to look anything up. It verifies the signature and reads the data straight from the token.

If someone tampers with the token contents, the signature check fails and the server rejects it.

### Session vs JWT Trade-offs

Server storage:
- Session: yes, the server must store every active session in memory or a database
- JWT: no, the server stores nothing because the data is inside the token

Invalidation (for example, logging out everywhere):
- Session: easy, delete the session record and the session ID becomes useless
- JWT: hard, the token remains valid until it expires because there is nothing to delete server-side

Scalability across multiple servers:
- Session: harder, all servers need access to the same session storage
- JWT: easier, any server with the secret key can verify the token independently

Size:
- Session cookie: tiny, it is just the session ID
- JWT: larger, it contains all your data plus the cryptographic signature

## How Token Storage Affects CSRF Risk

Where you store a JWT changes whether CSRF attacks work against it.

### JWT in a Cookie

Same CSRF risk as sessions.
The browser automatically sends the cookie containing the JWT with every request to that domain.
An attacker page can trigger a forged request and the browser will attach the JWT cookie.
The server sees a valid token and accepts the request.

### JWT in Local Storage

Not vulnerable to CSRF.
When your JavaScript makes a request, it manually reads the JWT from local storage and puts it in a request header (typically called `Authorization`).
An attacker page cannot do this because the browser blocks cross-site access to another site's local storage.
Even if the attacker triggers a request to the server, the JWT will not be included because no code on the attacker page can read it.

### The Trade-off: CSRF vs XSS

Local storage is not vulnerable to CSRF, but it is vulnerable to XSS (Cross-Site Scripting).
If an attacker injects malicious JavaScript into the page through a bug in the application, that script runs in the context of the page and can read local storage.
It could steal the JWT and send it to the attacker.

Cookies have a defense against this: the `HttpOnly` flag.
When a cookie is marked `HttpOnly`, JavaScript cannot read it at all.
Even if an attacker injects a script, they cannot steal an `HttpOnly` cookie.

Summary:
- Cookie storage: vulnerable to CSRF, protected from XSS theft (if `HttpOnly`)
- Local storage: protected from CSRF, vulnerable to XSS theft

There is no perfect option.
Each approach trades one risk for another.
That is why real applications layer multiple defenses together (anti-CSRF tokens, `HttpOnly` cookies, `SameSite` rules, XSS prevention) rather than relying on a single one.

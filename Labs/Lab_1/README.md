# Lab 1 Topics

## Comparison between Hash and Encryption


### Hash

- Fixed Output
- No key required
- irreversible

We usually salt the hash to prevent rainbow table attacks.

Hashing is  usually done for storing passwords in databases, we dont need to reverse them, thus we hash them, we only care about our input to result into the same hash as the original password.


### Encryption

- Variable output
- Symmetric ( One Key ) or Asymmetric ( Two Keys: Public and Private ) keys required
- Reversible



### Homework (Simulate Authentication)

1. Install bcrypt/argon2-cffi library
2. Write a function that hashes a string with a salt
3. Store some users (with HASHED passwords) in a DATABASE or FILE
4. Write a function that compares password and stored hash 
- a. If successful print "AUTHENTICATED"
- b. If not print "INVALID PASSWORD"

For the next lab: install Flask and Database Library for whatever DB you want to use (mysql, postgres, etc)
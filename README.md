# URL Shortener

This is a URL shortening service implemented in Python using the FastAPI framework.

## Description

The URL shortener service allows you to encode a long URL into a short URL and decode a short URL back to the original long URL.

## Features

- **Encode Endpoint:** Encodes a long URL into a short URL.
- **Decode Endpoint:** Decodes a short URL back to the original long URL.
- **Expiration:** Optionally supports expiration date for short URLs. (To Be Implemented)
- **Database Integration:** Stores URLs in an SQLite database.
- **Hashing Algorithm:** Uses sqids hashing algorithm for URL encoding/decoding.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NWProgramming00/URLShortener.git
   ```

2. Copy example.env to .env file
3. Configure .env according to your needs. example config is fully functional
4. Run project using
   ```bash
   docker compose up -d
   ```


## Research

**Random text?**

It is a bad idea to generate random text that will be correlated to shorten url.
This solution has many cons: relying on randomness does not ensure uniqueness; does not let you know instantly what 
is intended outcome - we must select from database record with original url using SELECT on random string. 
Just to name a few. Knowing this we should seek another approach.

**Hashing function?**

There are no physical limitation on url length whatsoever. But there are limits build in into the browsers itself. 
Knowing that the most popular browser is Chrome it is safe to assume that url will never be longer than 2083 characters 
or else it will cause browser crash.


| Browser           | Maximum URL Length |
|-------------------|--------------------|
| Chrome            | 2,083 characters   |
| Firefox           | 65,536 characters  |
| Safari            | 80,000 characters  |
| Internet Explorer | 2,083 characters   |
| Edge              | 2,083 characters   |


If we can define maximum number of characters that will be taken as an input then we can think of an algorithm that will be used to shorten the url.
Most obvious solution is using cryptographic hashing function. 
They could do the trick but CHF's do not generate unique hashes. There are no known case when hashes "collided" but
it should be assumed that they are not unique and in theory they will collide given infinite time.
Second con is that generated hashes (using SHA256 or other) based on urls itself would be very long strings.
Using irreversible hashing function does not make any sense either, because searching database will become less optimal.


I came up with the idea of generating a record in the database and then, based on the key index (ID) returned by the database, 
generate a short string representing this number. Using this method will ensure that generated representation of ID
will always be unique, deterministic and reversible. 


What's more string will get longer and longer as new records will have incremental ID's but will not be directly 
correlated with length of an url which is a big pros. Generated string can be tiny (we are talking 2 to few characters).
If we maintain database clean by setting expiry date for url we generated then we can talk about infinite number of urls.


Now we know what we need. Knowing that whatever it is that you came up with there is a high chance that someone already did too.
After some time researching, I discovered the "hashids" library in JavaScript that accomplishes this. 
Further investigation led me to the "Sqids" library, which is implemented in 42 programming languages, including Python.


After discovering that the algorithm explained above already exists, and it is mentioned as an ideal example for URL shortening, 
I have become firmly convinced that this is one of the top algorithms I can use for this task.

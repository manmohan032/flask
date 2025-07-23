## Problems that I have seen
- SQL injection could work with the string formating,
- No sepration of modules and routes,
- Routes should also be separated to maintain code,
- No Validity on anything.

## Changes Made(reason)
- Separated the modules and routes(to improve readability and maintainability).
- Used Hashed password storing technique which is used industry wide to store the password secured even after hacks.
- Used the placeholder rather than string formating to improve security .

### Note : I used AI : chatGPT free version to get the code into proper form like separation of Modules and routes as i dont have any knowledge on flask .But understand what and how the code changes worked.
- Accepted Changes from AI:
    1. Modules and Routes Separation.

- Rejected Changes from AI:
    1. Aeparate db connection file as we have only one module we could get Connection in that only but i know the extra db file is norm for a good project.


## Changes could be made:
- Validation on Email.
- Password limitation like (8 char,include @ or something)
- allow delete or put only with email and password validation to make it more secure.



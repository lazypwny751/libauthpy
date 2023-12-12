# libauthpy
simple authentication library written in python3.

![test](https://github.com/lazypwny751/libauthpy/assets/54551308/06c42f53-8da2-4f5f-b7ba-1b781b85c40a)

## Installation

### Using pip3
```sh
pip3 install git+https://github.com/lazypwny751/libauthpy.git
```

### Using make
```sh
git clone https://github.com/lazypwny751/libauthpy.git
cd libauthpy
make install
```

## Usage
General purpose of the library, manage your authentication requests from cathed by an automation tool or social media bots.

### register
this function sends registration request for admins, and admin can submit it using utility tools for tools.
```py
import libauth
auth = libauth.Auth("mydatabase.db")

auth.register("my user") # > bool
```

### inQueue
this function check up the user is in register table or not, so that's mean if the user has registered?
```py
import libauth
auth = libauth.Auth("mydatabase.db")

auth.inQueue("my user") # > bool
```

### dropRegister
after authentcation you delete the user from register table.
```py
import libauth
auth = libauth.Auth("mydatabase.db")

auth.dropRegister("my user") # > bool
```

### authenticate
this function allows to write a user to authenticated table, also it should take an boolean 
parameter called by "authlvl (authentication level)" 0 means allowed, 1 mean banned, default True.
```py
import libauth
auth = libauth.Auth("mydatabase.db")

auth.authenticate("my user", authlvl=True) # > bool
```

### inAuthentication
this function just check's the user in the auth table or not, it is not cheks for banned or not.
```py
import libauth
auth = libauth.Auth("mydatabase.db")

auth.inAuthentication("my user") # > bool
```

### isAuthenticated
this functions check's the user in the auth table and authlvl value is 0? because 0 means True
and 1 means False.
```py
import libauth
auth = libauth.Auth("mydatabase.db")

auth.isAuthenticated("my user") # > bool
```

### dropAuthentication
you can remove any user from authentication (you can ban any user).
```py
import libauth
auth = libauth.Auth("mydatabase.db")

auth.dropAuthentication("my user") # > bool
```

## Example
```py
import libauth
auth = libauth.Auth("mydatabase.db")

user = "my user"

auth.register(user)

if auth.inQueue(user):
    print(user, "is in queue.")

if auth.authenticate(user, authlvl=True):
    if auth.dropRegister(user):
        print(user, "authenticated.")

if auth.isAuthenticated(user):
    print(user, "is authenticated user.")
    if auth.dropAuthentication(user):
        print(user, "dropped himself from auth table.")
```

and you will see:
```
orange cat is in queue.
orange cat authenticated.
orange cat is authenticated user.
orange cat dropped himself from auth table.
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[GPL3](https://choosealicense.com/licenses/gpl-3.0/)

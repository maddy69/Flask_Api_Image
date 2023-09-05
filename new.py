####  used to create secret key for JWt token ####

import os
import secrets

print(secrets.token_hex(16))

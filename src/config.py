import os
from cryptography.fernet import Fernet

# Generate and store this key securely in production
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(ENCRYPTION_KEY)

import os

from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv('TEST_EMAIL')
PASSWORD = os.getenv('TEST_PASSWORD')


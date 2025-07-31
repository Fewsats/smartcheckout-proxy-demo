from browserbase import Browserbase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("BROWSERBASE_API_KEY")
extension_path = os.getenv("EXTENSION_PATH")

if not api_key or not extension_path:
    raise ValueError("BROWSERBASE_API_KEY and EXTENSION_PATH must be set")

bb = Browserbase(api_key=api_key)

# Upload the extension
with open(extension_path, "rb") as f:
    extension = bb.extensions.create(file=f)

extension_id = extension.id
print(f"Extension uploaded with ID: {extension_id}")

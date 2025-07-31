from browserbase import Browserbase
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("BROWSERBASE_API_KEY")
if not api_key:
    raise ValueError("BROWSERBASE_API_KEY must be set")

project_id = os.getenv("BROWSERBASE_PROJECT_ID")
if not project_id:
    raise ValueError("BROWSERBASE_PROJECT_ID must be set")

extension_id = os.getenv("BROWSERBASE_EXTENSION_ID")
if not extension_id:
    raise ValueError("BROWSERBASE_EXTENSION_ID must be set")

SC_PAYMENT_TOKEN = os.getenv("SC_PAYMENT_TOKEN")
if not SC_PAYMENT_TOKEN:
    raise ValueError("SC_PAYMENT_TOKEN must be set")


stripe_url = "https://buy.stripe.com/test_dRmcN7fC50Lo0g5fU60co00"

bb = Browserbase(api_key=api_key)

# Create a session with the extension
session = bb.sessions.create(
    project_id=project_id,
    extension_id=extension_id
)

print(f"Session created with ID: {session.id}")

# JavaScript to send the message to the extension's background script
js_code = f"""
// Dispatch a custom event that the extension's content script will listen for
const tokenEvent = new CustomEvent('browserbaseTokenSet', {{
  detail: {{
    token: "{SC_PAYMENT_TOKEN}",
    type: "SET_PAYMENT_TOKEN"
  }}
}});
window.dispatchEvent(tokenEvent);
console.log('Custom payment token set:', "{SC_PAYMENT_TOKEN}");
"""

# Connect to the session using Playwright and navigate to Stripe
with sync_playwright() as playwright:
    # Connect to the remote session
    chromium = playwright.chromium
    browser = chromium.connect_over_cdp(session.connect_url)
    context = browser.contexts[0]
    page = context.pages[0]
    
    try:
        # Navigate to the Stripe URL
        page.goto(stripe_url)
        print(f"Navigated to Stripe URL: {stripe_url}")
        
        # Execute the JavaScript to set the token
        page.evaluate(js_code)
        print(f"Attempted to set custom token: {SC_PAYMENT_TOKEN}")
        
        # Keep the session alive for manual testing
        print(f"Session is ready at Stripe checkout page.")
        print(f"Find your session here: https://www.browserbase.com/sessions")
        
        # Wait for user input to keep session alive
        input("Press Enter to close the session...")
        
    finally:
        page.close()
        browser.close()

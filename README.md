## Smartcheckout Browser Interceptor

## Setup

#### Upload the extension
- Create a `.env` using the format in `.env.example` with your [Browserbase](https://www.browserbase.com) API KEY.
- Add the path to the `.zip` with the latest version for our browser extension to `EXTENSION_PATH`
- Run `python upload_extension`. This script will upload the zip and print an `extension_id` that needs to be used when creating a browser session in Browserbase.


#### Create a session with our extension

- Make sure to update the .env to have the valid `BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID` and `BROWSERBASE_EXTENSION_ID`. The browser extension id must be the one from the previous steps.
- By default the extension loads a token that will substitute any CC data for a valid Stripe Sandbox url (using the valid `4242 4242 4242 4242` credit card number).
- You can use our [playground](https://playground.smartcheckout.dev) to tokenize credit card data and use that credit card token in our extension (`cct_sandbox_....`) with `SC_PAYMENT_TOKEN`.




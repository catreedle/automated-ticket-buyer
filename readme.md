# Automated Ticket Buyer

This script automates the process of purchasing tickets for events on a specified website. It logs in using predefined user credentials, navigates to the event page, and completes the purchase using stored payment details.

## Features
- Automates login and ticket purchasing.
- Handles multiple accounts concurrently.
- Uses Selenium with undetected Chrome driver for browser automation.
- Securely loads credentials from environment variables.

## Supported Website
- This script is designed to work with [MOMENTS](https://moments-mxkp.onrender.com/). Ensure that the website structure remains compatible with the script.

## Requirements
- Python 3.x
- Google Chrome
- ChromeDriver
- `undetected_chromedriver`, `selenium`, `python-dotenv`

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo.git](https://github.com/catreedle/automated-ticket-buyer.git
   cd automated-ticket-buyer
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```env
   EMAIL=your-email@example.com
   CARD_NUMBER=4242424242424242
   CARD_EXPIRY=12/34
   CARD_CVC=123
   CARD_NAME=Your Name
   URL=https://moments-mxkp.onrender.com/
   ```
4. Add user credentials in `accounts.json`:
   ```json
   {
       "user1@example.com": "password123",
       "user2@example.com": "securepass456"
   }
   ```

## Usage
Run the script:
```sh
python main.py
```

## Limitations
- This script **only works for accounts that are already signed up**.
- The website structure might change, requiring XPath adjustments.
- Ensure that Google login does not require additional verification.

## Payment Information
- The script uses stored payment details for checkout.
- You can test payments using [Stripe Test Cards](https://stripe.com/docs/testing).

## Disclaimer
This script is for educational purposes only. Use it responsibly and ensure compliance with website terms of service.


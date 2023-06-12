import requests
import smtplib
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()

EMAIL_PROVIDER_SMTP = os.getenv("EMAIL_PROVIDER_SMTP")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_email():
    with smtplib.SMTP(EMAIL_PROVIDER_SMTP, 587, timeout=120) as connection:
        message = f"Subject: Amazon Price Alert!\n"
        message += f"Instant Pot Duo Plus 9-in-1 Electric Pressure Cooker, Slow Cooker, Rice Cooker, Steamer, "
        message += f"Sauté, Yogurt Maker, Warmer & Sterilizer, Includes Free App with over 1900 Recipes, Stainless Steel, 3 Quart for $ {price}.\n"
        message += f"https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=RECEIVER_EMAIL,
                    msg=message.encode("utf-8")
        )


url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
}
response = requests.get(url=url, headers=header)
page_html = response.text

soup = BeautifulSoup(page_html, "html.parser")
price = float(soup.find(class_="a-offscreen").getText()[1:])

if price < 100:
    send_email()

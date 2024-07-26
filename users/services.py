import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name, description):
    product = stripe.Product.create(name=name, description=description)
    return product


def create_stripe_price(product_id, amount):
    price = stripe.Price.create(
        unit_amount=int(amount * 100), currency="usd", product=product_id
    )
    return price


def create_stripe_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
    )
    return session.id, session.url


def convert_rub_to_dollars(amount):
    """
    Конвертируем рубли в доллары
    """
    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)

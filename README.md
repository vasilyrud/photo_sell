# Photo Sell

Project to experiment with making a simple image sale service. While starting an image-sale service would have been tough a decade ago, it is easily achievable today with the numerous abstractions provided by friendly companies for ~~a fee~~ free! (as long as we don't start selling things for real) The program relies entirely on [Google Drive](https://www.google.com/drive) for image hosting, on Google's [OpenID Connect](https://openid.net/connect) support for login, [Stripe Connect](https://stripe.com/en-ca/connect) for payment routing, and [Stripe Payments](https://stripe.com/en-ca/payments) for payment itself (although the last one is still being integrated). Thus, the core program can remain simple.

## To run the app

1. Make a copy of `vars_template.py` and rename it to `vars.py`. Populate it with your Google and Stripe OAuth and API credentials.

2. Enable test mode in Google and Stripe to allow `redirect_uri` to go to localhost.

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Start the development flask server:

```
export FLASK_APP=photo_sell
python -m flask run
```

## To run tests 

```
python -m pytest
```

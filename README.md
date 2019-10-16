# Photo Sell

Project to experiment with making a lean image sale service.

To run the app:

1. Make a copy of `vars_template.py` and rename it to `vars.py`. Populate it with your Google and Stripe OAuth and API credentials.

2. Enable test mode in Google and Stripe to allow `redirect_uri` to go to localhost.

3. Run:

```
export FLASK_APP=photo_sell
flask run
```

## To run tests 

```
python -m pytest
```

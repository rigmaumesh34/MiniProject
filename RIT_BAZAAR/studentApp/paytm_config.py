# paytm_config.py
PAYTM_MERCHANT_KEY = 'YOUR_MERCHANT_KEY'
PAYTM_MERCHANT_ID = 'YOUR_MERCHANT_ID'
PAYTM_WEBSITE = 'WEBSTAGING'  # or 'DEFAULT' for production
PAYTM_CALLBACK_URL = 'http://127.0.0.1:8000/payment/handle-payment/'
PAYTM_TRANSACTION_URL = 'https://securegw-stage.paytm.in/order/process'  # for staging

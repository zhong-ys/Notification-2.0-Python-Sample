import logging
import os
import json
import websocket
import requests
from requests.auth import HTTPBasicAuth
import ssl


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
C8Y_BASEURL = 'https://{{Tenant-URL}}.eu-latest.cumulocity.com'
C8Y_TENANT = '{{Tenant-ID}}'
C8Y_USER = '{{Username}}'
C8Y_PASSWORD = '{{Password}}'
C8Y_AUTH = HTTPBasicAuth(C8Y_TENANT + '/' + C8Y_USER, C8Y_PASSWORD)
C8Y_HEADERS = {
    'Accept': 'application/json'
}
C8Y_BASEURL_WEBSOCKET = C8Y_BASEURL.replace('http://', 'ws://').replace('https://', 'wss://')

client = requests.Session()




def open_handler(ws):
    logging.info('Connected')


def message_handler(ws, message):
    parts = message.split('\n\n')
    headers = parts[0].split('\n')
    body = parts[1]
    # Send acknowledgement
    ws.send(headers[0])
    logging.info('New message: %s', headers[0])
    logging.info('Channel: %s', headers[1])
    logging.info('Action: %s', headers[2])
    logging.info('Body: %s', body)


def error_handler(ws, error):
    logging.error(error)


def close_handler(ws, close_status_code, close_msg):
    logging.info('Close websocket')


token = '{{Token-from-consumer1}}'


ws_client = websocket.WebSocketApp(
    C8Y_BASEURL_WEBSOCKET + '/notification2/consumer/?token=' + token + '&consumer=instance2',
    on_open = open_handler,
    on_message = message_handler,
    on_error = error_handler,
    on_close = close_handler
)

ws_client.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=60)

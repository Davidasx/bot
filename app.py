from flask import Flask, send_from_directory, request, jsonify, Response
import json
import time
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging_config import setup_logging

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

access_logger = setup_logging()
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.after_request
def log_request(response):
    ip = request.remote_addr
    method = request.method
    path = request.path
    status = response.status_code
    access_logger.info('', extra={
        'ip': ip,
        'method': method,
        'path': path,
        'status': status
    })
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8899)
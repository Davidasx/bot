from flask import Flask, send_from_directory, request, jsonify, Response, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from logging_config import setup_logging

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

access_logger = setup_logging()

@app.route('/')
def index():
    path = ""
    message = "You'll find nothing here, bot."
    ip = request.remote_addr
    ip = f"{ip}"
    return render_template('bot.html', path=path, message=message, ip=ip), 404

@app.route('/<path:path>')
def catch_all(path):
    ip = request.remote_addr
    if 'php' in path.lower():
        message = f"I know that you're trying to access {path} but I'll NEVER use PHP for my website!"
        ip = f"{ip}"
    else:
        message = f"I know that you're trying to access {path}!"
        ip = f"{ip}"
    return render_template('bot.html', path=path, message=message, ip=ip), 404

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
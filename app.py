"""
Simple Flask Web Application
Demonstrates docker-compose deployment to Kubernetes
"""
from flask import Flask, render_template, jsonify
import os
import socket
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Home page with deployment info"""
    return render_template('index.html',
                         hostname=socket.gethostname(),
                         timestamp=datetime.datetime.now().isoformat())

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/info')
def info():
    """API endpoint with system info"""
    return jsonify({
        'app': 'SimpleWebAppPython',
        'version': '1.0.0',
        'hostname': socket.gethostname(),
        'environment': os.getenv('FLASK_ENV', 'production'),
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

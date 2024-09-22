from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
REQUEST_COUNT = Counter('hello_world_requests_total', 'Total number of hello world requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('hello_world_request_latency_seconds', 'Request latency in seconds', ['endpoint'])
ERROR_COUNT = Counter('hello_world_errors_total', 'Total number of task manager API errors', ['method', 'endpoint', 'status_code'])

@app.route('/')
def hello_world():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()

    time.sleep(0.3) 
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)

    return "Hello, World!"

@app.route('/metrics')
def metrics():

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/error')
def error():
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/error').inc()
    time.sleep(0.2)
    REQUEST_LATENCY.labels(endpoint='/error').observe(time.time() - start_time)
    ERROR_COUNT.labels(method='GET', endpoint='/error', status_code='500').inc()
    
    return jsonify({"error": "Something went wrong!"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

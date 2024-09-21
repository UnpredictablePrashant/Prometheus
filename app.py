from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
REQUEST_COUNT = Counter('hello_world_requests_total', 'Total number of hello world requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('hello_world_request_latency_seconds', 'Request latency in seconds', ['endpoint'])

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import argparse
import os
from os import listdir
from os.path import isfile, join
import hashlib
from pipline import pedalboard_handler
from requests_toolbelt.multipart import decoder
import cgi
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # first we need to parse it
        parsed = urlparse(self.path)
        # get the query string
        query_string = parsed.query

        # send 200 response
        self.send_response(200)
        # send response headers
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_str = 'Please use post'
        self.wfile.write(json_str.encode(encoding='utf_8'))

    def do_POST(self):
        # Set the response status code
        self.send_response(200)

        # Set the Content-type header
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Get the request body
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})

        # Write the response content
        self.wfile.write(
            f'<html><body><h1>Received POST data: {form}</h1></body></html>'.encode('utf-8'))


def hash(str):
    return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)


def parse_args():
    parser = argparse.ArgumentParser(description='my description')
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    return parser.parse_args()


def main():
    # args = parse_args()
    httpd = HTTPServer(('0.0.0.0', 3000), MyHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()

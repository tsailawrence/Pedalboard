from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import argparse
import os
from os import listdir
from os.path import isfile, join
import hashlib
import msgpackrpc
from ec2_metadata import ec2_metadata


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # first we need to parse it
        parsed = urlparse(self.path)
        # get the query string
        query_string = parsed.query
        predecessor_ip = query_string

        # send 200 response
        self.send_response(200)
        # send response headers
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_str = '{"fileList": "' + '' + '  "}'
        self.wfile.write(json_str.encode(encoding='utf_8'))


def new_client(ip):
    return msgpackrpc.Client(msgpackrpc.Address(ip, 5057))


def hash(str):
    return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)


def parse_args():
    parser = argparse.ArgumentParser(description='my description')
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    httpd = HTTPServer((args.ip, args.port), MyHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import argparse
import os
from os import listdir
from os.path import isfile, join
import hashlib
from pipline import effect_pipline
from requests_toolbelt.multipart import decoder
import cgi
import json
from socketserver import ThreadingMixIn
import threading
from API.ipfs import upload2ipfs

class MyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
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
        self.send_header('Content-type', 'audio/mp3')
        #self.send_header('attachment; filename="my_filename.mp3"')
        self.end_headers()

        # Get the request body
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})

        # Body processing
        data_directory = IO_audio_read(form["file"])
        effect_string = json.loads(form["controls"].file.read())
        output_directory = effect_pipline(effect_string, data_directory)

        # Post to IPFS using pinata
        ipfs_string = json.loads(form["ipfs"].file.read())
        (_, ipfs_is_true), = ipfs_string.items()
        if ipfs_is_true:
            file_name = output_directory.split('/')[-1]
            cid = upload2ipfs(output_directory, file_name)
            # print('file: {}   cid: {}'.format(output_directory, cid))
            print('https link: {}'.format('https://gateway.pinata.cloud/ipfs/' + cid))

        # Write the response content
        try:
            with open(output_directory, 'rb') as file:
                self.wfile.write(file.read())
        except:
            self.wfile.write('return failed')



def hash(str):
    return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)


def parse_args():
    parser = argparse.ArgumentParser(description='my description')
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    return parser.parse_args()


def IO_audio_read(IO_audio):
    #data_directory = "backend/data/" + IO_audio.filename
    data_directory = "data/" + IO_audio.filename
    IO_audio_file = IO_audio.file.read()
    f = open(data_directory, "wb")
    f.write(IO_audio_file)
    f.close()
    return data_directory


# def main():
#     # args = parse_args()
#     httpd = HTTPServer(('0.0.0.0', 4000), MyHandler)
#     httpd.serve_forever()


# if __name__ == '__main__':
#     main()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 4000), MyHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
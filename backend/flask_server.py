from flask import Flask, request, Response
import os
from os import listdir
from os.path import isfile, join
import hashlib
from pipline import effect_pipline
from requests_toolbelt.multipart import decoder
import cgi
import json
from random import randint
from time import sleep
from API.ipfs import upload2ipfs

app = Flask(__name__)

# @app.route('/', methods=['OPTIONS'])
# def options_handler():
#     response = Response("ok")
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
#     response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     return response

@app.route('/', methods=['GET'])
def get_handler():
    response = Response('Please use post')
    response.headers.add('Content-Type', 'application/json')
    return response

@app.route('/', methods=['POST'])
def post_handler():

    response = Response()
    response.headers.add('Content-type', 'audio/mp3')

    # Get the request body
    # form = cgi.FieldStorage(
    #     fp=request.stream,
    #     headers=request.headers,
    #     environ={'REQUEST_METHOD': 'POST'})
    
    form = request.form
    file = request.files['file']
    controls=  form.get("controls")
    # print(request)
    # Body processing
    data_directory = IO_audio_read(file)
    effect_string = json.loads(controls)
    output_directory = effect_pipline(effect_string, data_directory)

    while not os.path.isfile(output_directory):
        continue

    # Post to IPFS using pinata
    ipfs_string = json.loads(form.get("ipfs"))
    (_, ipfs_is_true), = ipfs_string.items()
    if ipfs_is_true:
        file_name = output_directory.split('/')[-1]
        try:
            cid = upload2ipfs(output_directory, file_name)
            # print('file: {}   cid: {}'.format(output_directory, cid))
            print('https link: {}'.format('https://gateway.pinata.cloud/ipfs/' + cid))
        except:
            print('ipfs upload failed')

    # Write the response content
    # try:
    print("file has been processed successfully")
    sleep(randint(0, 5))
    
    def generate(output_directory):
        with open(output_directory, 'rb') as file:
            for file_chunk in read_in_chunks(file):
                data = file_chunk
                yield data 
                
    rs = Response(generate(output_directory), mimetype="audio/ogg")
    os.remove(data_directory)
    # os.remove(output_directory)
    # except:
    #     response.data = b'return failed'
    return rs

def IO_audio_read(IO_audio):
    filename = IO_audio.filename.split('.')
    data_directory = "backend/data/" + str(randint(0, 100000)) + "." + filename[1]
    # print(data_directory)
    # data_directory = "data/" + str(randint(0, 100000)) + "." + filename[1]
    IO_audio_file = IO_audio.read()
    f = open(data_directory, "wb")
    f.write(IO_audio_file)
    f.close()
    return data_directory

def read_in_chunks(file_object, chunk_size=102400):
    """Generator to read a file piece by piece. Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

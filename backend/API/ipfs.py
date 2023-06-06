import requests

def upload2ipfs(file_dir, file_name):
    # API KEY INFO
    API_Key = '0524c822339f8a4c939f'
    API_Secret = '2a6ce2a22dba4b6726d721119bd2ce8108465f90afb2fe93a6d8326b144f5d14'
    JWT = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI0NDYyMDE5Mi1jMGM4LTQ1NjAtOWI0OC1hZDM1ODMzYmJmOTAiLCJlbWFpbCI6InRhc2kuYWFyb25AZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjA1MjRjODIyMzM5ZjhhNGM5MzlmIiwic2NvcGVkS2V5U2VjcmV0IjoiMmE2Y2UyYTIyZGJhNGI2NzI2ZDcyMTExOWJkMmNlODEwODQ2NWY5MGFmYjJmZTkzYTZkODMyNmIxNDRmNWQxNCIsImlhdCI6MTY4NjA1OTIyNH0.K-zuedT-GoOozjwiaD9xlKgGFp2lILboE9avPkufiv8'

    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    payload={
        'pinataOptions': 
            '{"cidVersion": 1}',
        'pinataMetadata': 
            '{{"name": "{}", "keyvalues": {{"user": "AaronTsai"}}}}'.format(file_name),
    }

    files=[
        ('file',(file_name, open(file_dir,'rb'),'application/octet-stream'))
    ]

    headers = {
        'Authorization': "Bearer " + JWT,
        # 'pinata_api_key': API_Key,
        # 'pinata_secret_api_key': API_Secret,
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)

    return response.text.split('\"')[3]

def request_file(save_dir, cid):
    # Access Token
    Access_Token = 'IJVds5JJqLOJZZsgWO68uYFzR0NNaq6-8Yzb4ApNfyKIlPw8G23q17Z5fEcHp58b'
    # GateWay
    Gateways_domain = 'purple-supreme-frog-923.mypinata.cloud'

    ipfs_url = 'https://' + Gateways_domain + '/ipfs/' + cid + '?pinataGatewayToken=' + Access_Token

    # print(ipfs_url)

    r = requests.get(ipfs_url)

    with open(save_dir, 'wb') as f:
        f.write(r.content)

file_dir = "../data/demo.mp3"
file_name = file_dir.split('/')[-1]
save_dir = "../data/test.mp3"

cid = upload2ipfs(file_dir, file_name)
request_file(save_dir, cid)
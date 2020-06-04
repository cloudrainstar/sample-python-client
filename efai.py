import argparse
import sys
import requests
import json
import hashlib
import hmac
import base64

JSON_HEADER = {'Content-type': 'application/json'}
BASE_URL = "https://ai.everfortuneai.com.tw/api"

def login(username, password):
    try:
        # Get salt from system
        url = BASE_URL + "/session/salt?username=" + username
        r = requests.get(url)
        salt = r.json()['salt']
        # Hash password with salt
        dk = hmac.new(salt.encode('latin1'), (password+salt).encode('utf-8'), hashlib.sha512)
        hashed_pw = dk.hexdigest()
        # Login with hashed password
        url = BASE_URL + "/session/"
        r = requests.post(url,
                          data=json.dumps({'username': username,
                                           'password': hashed_pw}),
                          headers=JSON_HEADER)
        session_key = r.json()['session_key']
        return session_key
    except:
        print('Error: Login failed.')
        raise

def list_models():
    try:
        url = BASE_URL + "/model/"
        r = requests.get(url)
        return r.json()
    except:
        print('Error: Model request failed.')
        raise

def infer(session_key, model, filepath):
    try:
        with open(filepath, 'rb') as f:
            x = f.read()
    except:
        print('Error: Failed to read file.')
        raise
    try:
        url = BASE_URL + "/infer/"
        r = requests.post(url,
                          data=json.dumps({'session_key': session_key,
                                           'model': model,
                                           'data': [base64.b64encode(x).decode('latin1')]}),
                          headers=JSON_HEADER)
        infer_id = r.json()["id"]
        return infer_id
    except:
        print('Error: Failed to transfer data.')
        raise

def list_infer(session_key):
    try:
        url = BASE_URL + "/infer/" + "?session_key=" + session_key
        r = requests.get(url)
        return r.json()
    except:
        print('Error: Failed to transfer data.')
        raise

def get_infer(session_key, infer_id):
    try:
        url = BASE_URL + "/infer/" + infer_id + "?session_key=" + session_key
        r = requests.get(url)
        json_response = r.json()
        return [{'id':x,'txt':y,'img':z} for x,y,z in zip(json_response['id'],json_response['txt'],json_response['img'])]
    except:
        print('Error: Failed to transfer data.')
        raise

if __name__ == '__main__':
    # Create the parser and add arguments
    parser = argparse.ArgumentParser(description="A sample client application to use EFAI API.", epilog="""Example: python efai.py -a new -u demo -p demo -m boneage -f "/tmp/boneage.dcm" """)
    parser.add_argument('-a', '--action', choices=['models', 'list', 'get', 'new'], help='models will list all models, list will list all previous inferences (login required), get will get an old inference (login required), new will make a new inference (login required)')
    parser.add_argument('-u', '--username', type=str, help='Username (required for "list", "get" and "new")')
    parser.add_argument('-p', '--password', type=str, help='Password (required for "list", "get" and "new")')
    parser.add_argument('-i', '--id', type=str, help='ID (required for "get")')
    parser.add_argument('-m', '--model', type=str, help='Model name (required for "new")')
    parser.add_argument('-f', '--filepath', type=str, help='Full path of the file for inference (required for "new")')
    
    # Parse and print the results
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    if args.action == None:
        print('Error: An action is required!')
        sys.exit(1)
    elif args.action == 'models':
        row_format ="{:>20}{:>40}{:>10}"
        print(row_format.format("Name", "Long Name", "Cost"))
        for d in list_models():
            print(row_format.format(d['name'],d['longName'],d['cost']))
    elif args.action in ['list', 'get', 'new']:
        if args.username == None or args.password == None:
            print('Error: Login is required!')
            sys.exit(1)
        # Login
        username = args.username
        password = args.password
        session_key = login(username, password)
        if args.action == 'list':
            row_format ="{:>25}{:>25}{:>40}"
            print(row_format.format("DateTime", "Model", "ID"))
            for d in list_infer(session_key):
                print(row_format.format(d['timestamp'],d['model'],d['id']))
            sys.exit(1)
        if args.action == 'get':
            if args.id == None:
                print('Error: No ID to fetch')
                sys.exit(1)
            row_format ="{:>10}  {:<80}"
            print(row_format.format("ID", "Report"))
            for d in get_infer(session_key, args.id):
                print(row_format.format(d['id'],d['txt']))
            sys.exit(1)
        if args.action == 'new':
            if args.model == None:
                print('Error: Model name required.')
                sys.exit(1)
            if args.filepath == None:
                print('Error: File to inference required.')
                sys.exit(1)
            print('Inference ID:',infer(session_key, args.model, args.filepath))
            sys.exit(1)
        print('Error: Unknown Error.')
        sys.exit(1)
    else:
        print('Error: Invalid Action.')
        sys.exit(1)
    print(args)
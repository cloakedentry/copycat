# Send a GET request to an html archiving website, procure the html page, then CURL into a file

import getopt
import requests
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def wayback_call(url, output_dir):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(url=f"http://archive.org/wayback/available?url={url}", headers=headers, verify=False)
    curl_url = response.json()['archived_snapshots']['closest']['url']
    os.chdir(output_dir)
    filename = url.split("//")[1] if "//" in url else url
    os.system(f"curl -L {curl_url} --output {filename}.html")

    with open('response_dump.txt', 'a') as f:
        f.write(f"{url}:{response.status_code}\n")


def error_msg_1():
    print("Usage: python script.py -u single_url -o output_directory\n" +
          "       python script.py -f urls_file -o output_directory\n" +
          "       python script.py -h for help")
    sys.exit(2)


if __name__ == "__main__":
    url = None
    urlfile = None
    single_url = False
    multiple_url = False
    output_directory = os.getcwd()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:f:o:h")
    except getopt.GetoptError:
        print("Unknown option")
        error_msg_1()

    for opt, arg in opts:
        if opt == "-u":
            if multiple_url:
                print("ERROR: -u and -f inputs are mutually exclusive, use one or the other")
                sys.exit(2)
            else:
                single_url = True
                url = arg
        elif opt == "-f":
            if single_url:
                print("ERROR: -u and -f inputs are mutually exclusive, use one or the other")
                sys.exit(2)
            else:
                multiple_url = True
                urlfile = arg
        elif opt == "-o":
            output_directory = arg
        elif opt == "-h":
            error_msg_1()

    if not single_url and not multiple_url:
        print("ERROR: either -u or -f must be provided")
        error_msg_1()

    start_time = time.time()
    thread_count = os.cpu_count() * 5

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        if single_url:
            executor.submit(wayback_call, url, output_directory)
        else:
            with open(urlfile, "r") as f:
                urls = f.read().splitlines()
                for url in urls:
                    executor.submit(wayback_call, url, output_directory)
print("Elapsed time:", time.time() - start_time)

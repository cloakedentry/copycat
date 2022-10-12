# Send a GET request to an html archiving website, procure the html page, then CURL into a file
import json 
import getopt
import requests
import threading
import os
import sys
import xml.etree.ElementTree as ET
import json
import pathlib
import shutil
import multiprocessing
from multiprocessing import Pool
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from subprocess import DEVNULL, STDOUT, check_call
import time
def wayback_call_single(url,fhand2,output_dir):
    headers = {
        "Content-Type":"application/json",
        "Accept":"application/json"
    }
    get_response = requests.get(url=f"http://archive.org/wayback/available?url={url}",headers=headers,verify=False)
    fhand2.write(f"{url} : {get_response}\n")
    print(f"{url} : {get_response}")
    curl_url = get_response.json()['archived_snapshots']['closest']['url']
    os.chdir(output_dir)
    if "//" in url:
        url_split = url.split("//")[1]
        print(url_split)
        url = url_split
    os.system(f"curl -L {curl_url} --output {url}.html")

def wayback_call(url,fhand2,lock,output_dir): # 2
    headers = {
        "Content-Type":"application/json",
        "Accept":"application/json"
    }
    get_response = requests.get(url=f"http://archive.org/wayback/available?url={url}",headers=headers,verify=False)
    with lock: # Creates a Queue for within the with Lock Block
         fhand2.write(f"{url} : {get_response}\n")
         print(f"{url} : {get_response}")   
    curl_url = get_response.json()['archived_snapshots']['closest']['url']
    os.chdir(output_dir)
    os.system(f"curl -L {curl_url} --output {url}.html")
def error_msg_1():
    print(f"-u = single url \n-f = text file containing multiple urls\n-o destination folder\n{sys.argv[0]} -u single_url -o output_directory\n-h = help")
    sys.exit(2)
def error_msg_2():
    print("ERROR: -u and -f inputs \n-u and -f are mutually exclusive \nuse one or the other")
    sys.exit(2)
if __name__ == "__main__": # 1
    print("COPYCAT\n========================================================================")
    url = None
    urlfile = None
    single_url = False
    multiple_url = False
    output_directory = os.getcwd()
    try:
        opts, args = getopt.getopt(sys.argv[1:],"u:f:o:h:")
    except getopt.GetoptError:
        print("Unknown Operator Value")
        error_msg_1()
    for opt,arg in opts:
        if opt in ("-u"):
            if multiple_url == True:
                error_msg_2()
            else:
                single_url = True
                url_source = arg,"Single"
        if opt in ("-f"):
            if single_url == True:
                error_msg_2()
            else:
                multiple_url = True
                url_source = arg,"Text"
        if opt in ("-o"):
            print("Output directory")
            output_directory = arg
        if opt in ("-h"):
            print("HELP\n--------------------------------------------------------------------------------------------") 
            error_msg_1()
        print(f"{opt}:{arg}")
    start_time = time.time()
    debug_file = "response_dump.txt"
    fhand2 = open(debug_file,"w+")
#    file = "websites.txt"
    try:
        if url_source == False:
            print(sys.exit(2))
    except NameError:
        print("Url source has not been sourced, please provide the argument")
        sys.exit(2)
    if url_source[1] == "Text":
        counter = 0
        lock = threading.Lock()
        fhand = open(url_source[0],"r")
        core_count= multiprocessing.cpu_count()
        print(core_count)
        thread_count = core_count * 5 
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            jobs = []
            for line in fhand:
                line = line.strip()
                counter = counter + 1
                if counter == 110:
                    print("Backing off")
                    time.sleep(120)
                    counter = 0            
                executor.submit(wayback_call,line,fhand2,lock,output_directory)
        print(f"time:{time.time()-start_time}")
    if url_source[1] == "Single":
        wayback_call_single(url_source[0],fhand2,output_directory)
        print(f"time:{time.time()-start_time}")


import argparse
import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor


def wayback_call(url, output_dir):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.get(
        url=f"http://archive.org/wayback/available?url={url}", headers=headers, verify=False)
    curl_url = response.json()['archived_snapshots']['closest']['url']

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    os.chdir(output_dir)

    filename = url.split("//")[1] if "//" in url else url
    os.system(f"curl -L {curl_url} --output {filename}.html")

    with open('response_dump.txt', 'a') as f:
        f.write(f"{url}:{response.status_code}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Copycat script that downloads a webpage and its response from the Wayback Machine')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', type=str,
                       help='Single URL to download from Wayback Machine')
    group.add_argument('-f', '--file', type=str,
                       help='Text file with a list of URLs, one per line')
    parser.add_argument('-o', '--output', type=str,
                        default=os.getcwd(), help='Output directory path')
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    urls = []
    if args.url:
        urls.append(args.url)
    elif args.file:
        with open(args.file, "r") as f:
            urls = f.read().splitlines()

    start_time = time.time()
    thread_count = max(1, os.cpu_count() * 5)

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for url in urls:
            executor.submit(wayback_call, url, output_dir)

    print("Elapsed time:", time.time() - start_time)


if __name__ == '__main__':
    main()
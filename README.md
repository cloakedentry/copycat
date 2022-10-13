# copycat

A no touch research tool for web page OSINT.


### Technical Details
The script is using web archive as a proxy. Essentially the script is initiating the conversation with web archives which orders it to perform the webpage request. In return the web archives server is perfroming the request then returning the webpage back to you in the form of the url that you download as a local html copy. The only interaction is you telling web archives API to do the dirty work.

### The Why and How
Operational Security (OPSEC). Lots of things to consider when performing OSINT. Super cookies, Trackers, Browser Fingerprinting, Logs, VPNs, etc. This is just a tool and you still need to consider the other areas of OPSEC. I wanted to be able to view or perform OSINT on a targets current web page without allowing my machine to touch the web page. This tool takes the URL(s) and puts them into internet archives, saves the page and downloads the .html webpage locally. This eliminates the connection from your machine to the targets machine. Keep in mind the targets domain will see internet archives domain going to it. 



### Quick Start
```
git clone https://github.com/cloakedentry/copycat.git
```

You will need a URL or a file with the target URLs one per line. 

```
python copycat.py -h <help>
python copycat.py -u <for single url>
python copycat.py -f <txt file containing multiple URLS> 
python copycat.py -o <output directory for html not required>
```

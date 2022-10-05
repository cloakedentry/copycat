# copycat

A no touch research tool for web page recon.


### Technical Details
The script is using web archive as a proxy. Essentially the script is initiating the conversation with web archives which orders it to perform the recon. In return the web archives server is doing the requesting then getting it back to you in the form of the url that you download. The only interaction is you telling web archives API to do the dirty work.

### The Why and How
Operational Security (OPSEC). Lots of things to consider when performing OSINT. Trackers, Browsers, Logs, VPN, etc. This is just a tool and you still need to consider the other areas of OPSEC. I wanted to be able to view or perform recon on target web pages without ever physcially touching the web page. This tool takes the URL(s) and puts them into internet archives, saves the page and downloads the .html webpage locally. This eliminates the connection from your machine to the targets machine. Keep in mind the targets domain will see internet archives domain going to it. 



### Quick Start
```
git clone https://github.com/cloakedentry/copycat.git
```

You will need a URL or a file with the target URLs one per line. 

```
python3 copycat.py -h <help>
python3 copycat.py -u <-u is for single url>
python3 -f <txt file containing multiple URLS> 
python3 -o <output directory for html not required>
```

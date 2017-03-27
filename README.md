# proxyServer
 Caching, multi-threaded proxy webserver which handling prefetched requests 
 Author : Rishabh Hastu
 
What's Implemented?
a. HTTP/1.1
b. HTTP/1.0
c. Listening to the client
d. Parsing the information
e. Multithreading
f. Prefetching
g. Caching

Python Version : 3.5


Program Usage:
         $ python webproxy.py [port] [timeout]
port - [Mandatory] Enter port number between 
timeout - [Optional] Enter Timeout value for Cache


What's in the progrm?
1. Created a web proxy server which handles the requests from the Browser and servers as an intermediate between the browser and the target server
2. The requests are parsed and undergoes validity check of METHOD AND VERSION
3. The proxy then caches the responses for a prescribed amount of time and if the browser asks for the cached webpage in the stipulated amount of time, the request is    served form the cache. I have used the time.clock() mechanism to check validate the timeout. 
4. The main threads spaws a server thread which checks for the URI and then calls a function proxy_server client to ask for the response from the target server and    caches the response using dictionary and the response is stored wrt hash value
5. The browser if asks for the request within a timout value, the hash value is matched and cache is hit and the data is given to the brower using this cache.
6. The proxy also runs a thread prefetch thread which parses the HTML and looks for the hyperlinks and requests those hyperlinks from the target servers. 
7. These prefetched information is also stored in the cache and the next time user asks the same data within the timer, it gets responded from the cache.
8. This reduces network traffic 

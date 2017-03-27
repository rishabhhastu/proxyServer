import socket 
import hashlib
import time
import threading 
import sys
import re
def prefetching_thread(links , target_ip ):                                             #Assemble the links and appends the links to make the URL
    for link in links:
        if '://' not in link:
            if link[0]=='/':
                link = "http://" + target_ip+link
            else:
                link = "http://" + target_ip + '/' + link
        webserver = link.split('/')[2]
        port_pos = webserver.find(':')
        if port_pos == -1:
            target_port = 80
        else:
            target_port=webserver[(port_pos + 1):]
        fetching_thread = threading.Thread(target=fetch_URL , args=(link,webserver,target_port))
        fetching_thread.start()
        
def fetch_URL(link , target_ip, target_port):                                                       # Get the response form the target webserver
    try:
        proxy_fetch_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        target_address = (target_ip,target_port) 
        hash_generated = hashlib.sha256()
        hash_generated.update(link.encode() +client_address[0].encode())
        final_hash = hash_generated.hexdigest()
        query1 = "GET {key1} HTTP/1.0\r\nHost: {key2}\r\nConnection: keep-alive\r\n\r\n".format(key1 = link, key2=target_ip)
        proxy_fetch_socket.connect(target_address)
        proxy_fetch_socket.send(query1.encode())
        time_to_save = time.clock()
        to_be_added = b''
        while 1:
            message_received_fetch = proxy_fetch_socket.recv(Buffer)
            if len(message_received_fetch) > 0:
                to_be_added += message_received_fetch
                hash_dictionary[final_hash] = str(time_to_save).encode() + b"|||" + to_be_added             #Store the response in a dictionary
            else:
                break
    
    except socket.gaierror:
        print("The Interet Connectivity is down!")
        proxy_fetch_socket.close()
    except socket.error:
        print("The Socket is closed")
    
def request_target(proxy_client_socket, target_address, time_to_save , final_hash, client, client_address):
#     print("Im in REQUEST_TARGET")
    proxy_client_socket.connect(target_address)
    proxy_client_socket.send(data_encoded)
    to_be_added = b""
    while 1:
        message_encoded_target = proxy_client_socket.recv(Buffer)
        if len(message_encoded_target) > 0:
            to_be_added += message_encoded_target
            hash_dictionary[final_hash] = str(time_to_save).encode() + b"|" + to_be_added
            print("Data received for " + str(data_encoded) + "\t" + str(message_encoded_target))
        else:
            break
        
        client.send(to_be_added)
        print("Data Sent On " + str(client_address))
    print("IM OUT OF WHILE PROXY")

    client.close()
    proxy_client_socket.close()

def server_thread(client, client_address, data_encoded):                                                #Extracts the port number and URL and passes to the next function
    try:
        if len(data_encoded) > 0:
            data_decoded = data_encoded.decode('utf-8').split('\n')
            http_command = data_decoded[0].split()
            request_method = http_command[0]
            if request_method != 'GET':                                                             #Checks the METHOD
                print("invalid")
                reason = 'Invalid Method'
                status_code = 400
                to_send = '<html><body>'+ str(status_code)+ ' Bad Request Reason: ' + reason + '</body></html>'
                header = '{version} 400 Bad Request\n\n'.format(version = request_method)    
                client.send((header+to_send).encode())
                client.close()
            original_URL = http_command[1]
            request_URL = original_URL.split('/')[2]
            hash_generated = hashlib.sha256()
            hash_generated.update(original_URL.encode() +client_address[0].encode())
            final_hash = hash_generated.hexdigest()
            request_version = http_command[2]
            if request_version not in ['HTTP/1.1' , 'HTTP/1.0']:                                    #Checks the Version
                reason = 'Invalid VERSION'
                status_code = 400
                to_send = '<html><body>'+ str(status_code)+ ' Bad Request Reason: ' + reason + '</body></html>'
                header = '{version} 400 Bad Request\n\n'.format(version = request_version)    
                client.send((header+to_send).encode())
                client.close()
            target_ip_with_port = request_URL
            port_pos = target_ip_with_port.find(":")
            if port_pos == -1:
                target_ip = target_ip_with_port
                target_port = 80
            else:
                target_ip = target_ip_with_port[:port_pos]
                target_port=int(target_ip_with_port[(port_pos+1):])
            proxyserver_client(target_ip , target_port, client,client_address,data_encoded, final_hash)
    except IndexError as e:
        print("INDEX ERROR: " + str(e) )


def proxyserver_client(target_ip , target_port, client,client_address,data_encoded, final_hash):                #Requests the URL from the Target
    proxy_client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    target_address = (target_ip , target_port)
    if final_hash in hash_dictionary.keys():
        print("FOUND IN DICTIONARY")
        time_check = hash_dictionary[final_hash]
        in_time = time_check.split(b"|||")[0]
        in_time = in_time.decode()
        time_duration = time.clock() - float(in_time)
        print("TIME DURATION: " + str(time_duration))
        if time_duration > timeout:
            try:
                print("Deleting items from dictionary and Timer Expires")
                proxy_client_socket.connect(target_address)
                list_1 = data_encoded.split(b'\r\n')
                to_be_added = b""
                data_encoded=b""
                for line in list_1:
                    if b"Accept-Encoding" in line:
                        continue
                    else:
                        data_encoded += line + b"\r\n"
                data_encoded = data_encoded[0:len(data_encoded)-2]
                proxy_client_socket.send(data_encoded)
                time_to_save = time.clock()
                while 1:
                    message_encoded_target = proxy_client_socket.recv(Buffer)
                    if len(message_encoded_target) > 0:
                        to_be_added += message_encoded_target
                        hash_dictionary[final_hash] = str(time_to_save).encode() + b"|||" + to_be_added
                    else:
                        break
                client.send(to_be_added)
                print("IM OUT OF WHILE")
                list_2 = to_be_added.split(b'\r\n')
                if b"Content-Type: text/html; charset=utf-8" or b"Content-Type: text/html" in list_2:
                    links = re.findall(re.compile(r"href=\"(.+?)\""),to_be_added.decode())
                    if len(links) > 0:
                        prefetching_thread(links , target_ip )
            except socket.gaierror:
                print("Check Internet Conectivity")
                client.close()
                proxy_client_socket.close()
            except socket.error:
                print("The Socket is closed")
            except UnicodeDecodeError:
                print('')
        else:
            print("Taking Data from Dictionary" + str(time_duration))
            time_to_save = time.clock()
            data_sent = time_check.split(b"|||")[1]
            hash_dictionary[final_hash] = str(time_to_save).encode() + b"|||" + data_sent

            client.send(data_sent)

    else:
        try:
            print("Im ELSE")
            proxy_client_socket.connect(target_address)
            list_1 = data_encoded.split(b'\r\n')
            data_encoded=b""
            for line in list_1:
                if b"Accept-Encoding" in line:
                    continue
                else:
                    data_encoded += line + b"\r\n"
            data_encoded = data_encoded[0:len(data_encoded)-2]
            proxy_client_socket.send(data_encoded)
            
            to_be_added = b""
            time_to_save = time.clock()
            while 1:
                message_encoded_target = proxy_client_socket.recv(Buffer)
                if len(message_encoded_target) > 0:
                    to_be_added += message_encoded_target
                    hash_dictionary[final_hash] = str(time_to_save).encode() + b"|||" + to_be_added
                else:
                    break
            print("IM OUT OF WHILE")
            client.send(to_be_added)
            list_2 = to_be_added.split(b'\r\n')
            if b"Content-Type: text/html; charset=utf-8" or b"Content-Type: text/html" in list_2:
                links = re.findall(re.compile(r"href=\"(.+?)\""),to_be_added.decode())
                if len(links) > 0:
                    prefetching_thread(links , target_ip )                                          #Calls the prefetching thread
            else:
                print("Content type NOT FOUND TEXT/HTML")
            
        except socket.gaierror:
            print("Check Internet Conectivity")
            client.close()
            proxy_client_socket.close()
        
        except socket.error:
            print("The Socket is closed")
        
        except UnicodeDecodeError:
            print('')
        client.close()
        proxy_client_socket.close()
if __name__ == "__main__":
    try :
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        if len(sys.argv) == 2:
            port = int(sys.argv[1])
        
        if len(sys.argv) == 3:
            port = int(sys.argv[1])
            timeout = int(sys.argv[2])
        
        Buffer = 4096
        print('Server Started')
        s_socket.bind((host,port))
        s_socket.listen(1)
        hash_dictionary = {}
        links = []
        while 1:
            print("Waiting for new connection")
            client , client_address = s_socket.accept()
            print("A new Accept")
            print(client_address)
            data_encoded = client.recv(Buffer)    
            t=threading.Thread(target=server_thread, args= (client, client_address, data_encoded))
            t.start()
    except KeyboardInterrupt:
        s_socket.close()
        print("Server Socket Closed")
        sys.exit()    
sys.exit()
        
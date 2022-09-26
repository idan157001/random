import socket
import time
import string
import threading
import urllib3.request
import xmltodict
req = [
    'M-SEARCH * HTTP/1.1',
    'Host:239.255.255.250:1900',
    'Man:"ssdp:discover"',
    'MX:1',
    'ST: urn:dial-multiscreen-org:service:dial:1',
    '',
    '']
#urn:dial-multiscreen-org:service:dial:1
#urn:dial-multiscreen-org:device:dial:1
#upnp:rootdevice
devices = {}
req = '\r\n'.join(req)
multi_group = ("239.255.255.250",1900)


class SSDP:
    def __init__(self):
        self.COUNTER_SLEEP_TIME = 1
        
        self.data = ''
        self.current_device = ''
        self.urls = set()
        self.devices = dict()
        
        threading.Thread(target=self.counter,daemon=True).start()
        self.sock = self.config_socket()
    

    def counter(self):
        while True:
            before_devices_count = len(self.devices)
            time.sleep(self.COUNTER_SLEEP_TIME)
            now_devices_count = len(self.devices)

            if before_devices_count == now_devices_count:
                self.sock.close() # cause OSError 


    def config_socket(self):
        """Create the socket """
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        sock.bind(('192.168.1.120',0))
        sock.sendto(bytes(req.encode()),multi_group)
        return sock


    def driver(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                self.current_device += data
                self.find_xml_file()
                self.current_device = ''
                time.sleep(0.1)
                
            except OSError: # called when self.counter close socket connection
                break
        
        self.get_data_from_xml()
        return self.devices
        

    def find_xml_file(self):
        """Get device ip address from data and add it to the set > {'name': '192.168.1.1'}"""
        lines = self.current_device.split("LOCATION:")
        for line in self.current_device.split('\n'):
            if 'LOCATION:' in line:
                link = line.split('LOCATION:')[1].strip()
                if link.endswith('.xml'):
                    self.urls.add(link)
        
                
    def get_data_from_xml(self):
        http = urllib3.PoolManager()
        for url in self.urls:
            
            req = http.urlopen('GET',url)
            data = req.data.decode()
            data = xmltodict.parse(data)
            self.get_url_base(data)


    def get_url_base(self,data):
        try:
            friendlyName =  data['root']['device']['friendlyName']
            UDN = data['root']['device']['UDN']
            self.devices[friendlyName] = [UDN]

            URLBase = (data['root']['URLBase'])
            self.devices[friendlyName].append(URLBase)

        except Exception as e:
            pass


        
x = SSDP().driver()
print(x)

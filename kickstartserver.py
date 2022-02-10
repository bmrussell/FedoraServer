# Boot from the Fedora installation ISO
# At the boot menu, press UP then e to edit the install option
# Insert the kickstart directive into the the boot string before the quiet directive, e.g.:
#   inst.ks=http://192.168.1.6:8000/fedoraserver.ks
#
# Key sequence for typing blind:
#   {UP}e{DOWN}{DOWN}{END}{LEFTx6}{SPACE}inst.ks=http://192.168.1.6:8000/fedoraserver.ks{CTRL}x
#
# See kickstart reference:
# https://docs.fedoraproject.org/en-US/fedora/rawhide/install-guide/appendixes/Kickstart_Syntax_Reference/#appe-kickstart-syntax-reference

import os
import http.server
from re import T
import socketserver
import getpass
import glob
from io import BytesIO
from string import Template
import socket

LISTEN_PORT = 8000
this_nostname = socket.gethostname()
ipaddress = socket.gethostbyname(this_nostname)

try:
  default_user_name = os.environ['USERNAME']  # Windows
except KeyError:
  default_user_name = os.environ['USER']      # Linux 

fedora_hostname = ''
user_name = ''
user_password = ''

class FileServer(http.server.SimpleHTTPRequestHandler):
  Username = ''
  Password = ''
  Hostname = ''

  def send_head(self):
    for ksfile in glob.glob('*.ks'):    
      if self.translate_path(self.path).endswith(ksfile):
        with open(ksfile, 'r') as f:
          t = Template(f.read())
          body = t.safe_substitute(userpass=FileServer.Password, username=FileServer.Username, hostname=FileServer.Hostname)

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=ascii')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        return BytesIO(body.encode('ascii'))

    self.send_response(404)
    self.end_headers()

def main() -> None:

  input_hostname = ''
  while not input_hostname:
    input_hostname = input('Hostname:')

  input_username = input(f'Username ({default_user_name}):')
  if not input_username:
    input_username = default_user_name
  
  while True:                                       # if linux/ container, use
    input_password = getpass.getpass('Password:')   # input_password = crypt.crypt(userpass_input, crypt.mksalt())
    if input_password:                              # and pass --iscrypted as a parameter to the user entry in kickstart file
      break

  FileServer.Username = input_username
  FileServer.Password = input_password
  FileServer.Hostname = input_hostname
  with socketserver.TCPServer((ipaddress, LISTEN_PORT), FileServer) as httpd:
    print(f'Serving files from {this_nostname} on port {LISTEN_PORT}.')
    firstksfile = glob.glob('*.ks')[0]
    print(f'Add inst.ks=http://{ipaddress}:{LISTEN_PORT}/{firstksfile} to Fedora install boot options')
    try:
      httpd.serve_forever()
    except KeyboardInterrupt:
      print('Shutting down HTTP Server...')

if __name__ == '__main__':
    main()
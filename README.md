# FedoraServer 
🐧 as 🐄

Configure a new Fedora Server from kickstart files. Solution provides a simple python HTTP server to serve multiple kickstart files, substituting entered values for the hostname, user to create and password.

See the [reference](https://docs.fedoraproject.org/en-US/fedora/rawhide/install-guide/appendixes/Kickstart_Syntax_Reference/#appe-kickstart-syntax-reference) for details on kickstart parameters.

Supply the HTTP request for the relevant .ks file in the Fedora installation boot options (entered by 'e'). e.g. http://192.168.1.6:8000/fedoraserver.ks


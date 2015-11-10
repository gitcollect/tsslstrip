# Targeted SSLSTRIP (under development)
### A targeted MITM tool that implements Moxie Marlinspike's HTTPS stripping attacks.

> **Warning:** 
> **Use at your own risk** as the project is still under development and bugs might exist.

* * *

## 1. Installation
> **Note:** 
> Please follow the instructions below carefully to get the application up and running. Or as other people would say, RTFM before asking anything :)

### 1.1 Python
Python 2.5 or newer is required to run TSSLSTRIP. Please install Python using the instructions on [https://www.python.org/](https://www.python.org/).

### 1.2 Twisted Web
Twisted Web is a dependency for TSSLSTRIP and can be installed using `apt-get install python-twisted-web` (assuming you're using Linux).

### 1.3 TSSLSTRIP
There are three steps to get TSSLSTRIP working (assuming you're using Linux).

 - Make sure you're the man-in-the-middle
 - Enable forwarding mode (as root): `echo "1" > /proc/sys/net/ipv4/ip_forward`
 - Setup iptables to intercept HTTP requests (as root): `iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port <yourListenPort>`

## 2. Usage
Please run `python tsslstrip.py -h` to get the command-line options.

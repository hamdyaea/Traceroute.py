# Traceroute.py — Linux Network Path Inspector

**Developer:** Hamdy Abou El Anein  
**Contact:** info@daylightlinux.ch  
**License:** GPL v3 (see LICENSE).

A Python 3 command-line frontend for Linux `traceroute` or `tracepath`. The historical implementation required root-level raw ICMP sockets; the modern version invokes the installed system utility with a validated argument list and no shell interpolation. It supports configurable hop limits and timeouts.

```sh
python3 Traceroute.py example.com
python3 Traceroute.py 1.1.1.1 --max-hops 12
python3 -m unittest discover -s tests -v
```

Install `traceroute` or `tracepath` with your distribution's package manager. Actual network results depend on firewalls, routing and permissions. Unit tests mock external commands; no packets are sent by tests.

Original raw-socket implementation: [old branch](https://github.com/hamdyaea/Traceroute.py/tree/old).

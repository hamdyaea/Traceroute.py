# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com

# The idea of this software is to create a Traceroute in pure Python.
# I have tested it only in linux.

import socket
import os
import struct
import time
import random
from urllib.parse import urlparse


def create_socket(timeout):
    icmp = socket.getprotobyname('icmp')
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except PermissionError as e:
        raise PermissionError('Run this software as root or admin only !') from e
    sock.settimeout(timeout)
    return sock



def checksum(source_string):
    sum = 0
    max_count = (len(source_string) / 2) * 2
    count = 0
    while count < max_count:
        val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + val
        sum = sum & 0xffffffff
        count = count + 2

    if max_count < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_packet(id):
    header = struct.pack('bbHHh', 8, 0, 0, id, 1)
    data = 192 * b'Q'
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', 8, 0, socket.htons(my_checksum), id, 1)
    return header + data

def get_route(hostname, max_hops=30, timeout=1):
    try:
        parsed_url = urlparse(hostname)
        destination = socket.gethostbyname(parsed_url.hostname if parsed_url.hostname else hostname)
    except socket.gaierror:
        print(f"Erreur : Nom d'hôte invalide '{hostname}'")
        return

    print(f'Traceroute to {hostname} ({destination}), {max_hops} hops max')

    ttl = 1
    while True:
        sock = create_socket(timeout)
        sock.setsockopt(socket.SOL_IP, socket.IP_TTL, struct.pack('I', ttl))
        packet_id = random.randint(1, 65535)
        packet = create_packet(packet_id)

        sock.sendto(packet, (destination, 1))
        start_time = time.time()

        addr = None
        try:
            _, addr = sock.recvfrom(512)
            addr = addr[0]
            end_time = time.time()
            duration = round((end_time - start_time) * 1000, 2)
            print(f'{ttl}\t{addr}\t{duration}ms')
        except socket.timeout:
            print(f'{ttl}\t*\tTimeout')
        finally:
            sock.close()

        ttl += 1
        if addr == destination or ttl > max_hops:
            break

if __name__ == "__main__":
    target = input("Enter the Traceroute destination : ")
    get_route(target)


#!/usr/bin/env python3
import argparse
import socket
from urllib.parse import urlparse

def resolve_ip_and_print_domain(url, print_domain_with_ip, output_file):
    # Check if the URL has a scheme (e.g., http:// or https://)
    if not urlparse(url).scheme:
        # If scheme is missing, assume http:// by default
        url = 'http://' + url

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc

    try:
        # Use socket.getaddrinfo() to resolve the hostname
        addr_info = socket.getaddrinfo(hostname, None)

        # Extract the IP address from the first result (typically IPv4)
        ip = addr_info[0][4][0]

        if print_domain_with_ip:
            result = f"{hostname}: {ip}"
        else:
            result = ip
        
        if output_file:
            with open(output_file, 'a') as f:  # Use 'a' mode to append to the output file
                f.write(result + '\n')
            print(f"Result for '{url}' saved to '{output_file}'")
        else:
            print(result)
    except socket.error:
        print(f"Unable to resolve IP address for '{hostname}'")

def resolve_hosts_file(hosts_file, print_domain_with_ip, output_file):
    try:
        with open(hosts_file, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        
        for url in urls:
            resolve_ip_and_print_domain(url, print_domain_with_ip, output_file)
    
    except FileNotFoundError:
        print(f"Error: Hosts file '{hosts_file}' not found.")

def main():
    parser = argparse.ArgumentParser(description='Resolve IP addresses for domains or URLs specified via file or single URL')
    parser.add_argument('-u', '--url', type=str,
                        help='single URL to resolve (e.g., https://example.com)')
    parser.add_argument('-f', '--hosts_file', type=str,
                        help='file containing URLs or domains (one per line)')
    parser.add_argument('-ds', '--domain_with_ip', action='store_true',
                        help='print domain name with IP address')
    parser.add_argument('-o', '--output', type=str,
                        help='output file to save results')

    args = parser.parse_args()

    single_url = args.url
    hosts_file = args.hosts_file
    print_domain_with_ip = args.domain_with_ip
    output_file = args.output

    if single_url:
        resolve_ip_and_print_domain(single_url, print_domain_with_ip, output_file)
    elif hosts_file:
        resolve_hosts_file(hosts_file, print_domain_with_ip, output_file)
    else:
        print("Error: Please provide either a single URL (-u) or a hosts file (-f).")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import socket
from urllib.parse import urlparse

def extract_domain(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        return parsed_url.netloc
    else:
        return url  # Use the URL as-is if netloc is empty (for cases without scheme)

def resolve_ip_and_print_domain(domain, print_domain_with_ip, output_file):
    try:
        ip = socket.gethostbyname(domain)
        if print_domain_with_ip:
            result = f"{domain}: {ip}"
        else:
            result = ip
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(result + '\n')
            print(f"Result saved to '{output_file}'")
        else:
            print(result)
    except socket.error:
        print(f"Unable to resolve IP address for '{domain}'")

def main():
    parser = argparse.ArgumentParser(description='Resolve IP address for a domain or URL and optionally print domain with IP')
    parser.add_argument('-u', '--url', type=str, required=True,
                        help='domain or URL to resolve (e.g., example.com or http://example.com)')
    parser.add_argument('-ds', '--domain_with_ip', action='store_true',
                        help='print domain name with IP address')
    parser.add_argument('-o', '--output', type=str,
                        help='output file to save result')

    args = parser.parse_args()

    input_url = args.url
    print_domain_with_ip = args.domain_with_ip
    output_file = args.output

    domain = extract_domain(input_url)
    resolve_ip_and_print_domain(domain, print_domain_with_ip, output_file)

if __name__ == "__main__":
    main()

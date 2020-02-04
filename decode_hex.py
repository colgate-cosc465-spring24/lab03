#!/usr/bin/python3

import sys

def main():
    for line in sys.stdin:
        raw_hex = line.strip()
        if len(raw_hex) < 3 or raw_hex[2] != ':':
            continue
        cleaned_hex = raw_hex.replace(':','')
        raw_ascii = bytearray.fromhex(cleaned_hex).decode()
        pretty_ascii = repr(raw_ascii)
        print(pretty_ascii)

if __name__ == '__main__':
    main()

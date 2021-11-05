#!/usr/bin/env python3

import argparse
import base64
import json
import sys
import yaml

import cwt
import requests
import PIL.Image
import pyzbar.pyzbar


DID_URL = 'https://nzcp.identity.health.nz/.well-known/did.json'


def get_did_from_url():
    """Fetch DID document with public verification keys from URL"""
    try:
        r = requests.get(DID_URL)
        r.raise_for_status()
    except Exception:
        print("Got exception fetching DID")
    return r.json()


def get_verification_keys(did):
    """Get public verification keys from a DID document"""
    verification_keys = []
    for verification_method in did['verificationMethod']:
        if verification_method['type'] == 'JsonWebKey2020':
            kid = verification_method['id'].split('#')[1]
            verification_method['publicKeyJwk']['kid'] = kid
            verification_keys.append(
                cwt.COSEKey.from_jwk(verification_method['publicKeyJwk'])
            )
    return verification_keys


def main():
    parser = argparse.ArgumentParser(description='NZ COVID Pass Verifier.')
    parser.add_argument('--qrcode-file', type=str, required=True,
                        help='file name containing NZ COVID pass QR code')
    parser.add_argument('--did-file', type=str,
                        help='file name containing DID with verification keys')

    args = parser.parse_args()

    if args.did_file:
        # Get public verification keys from file
        with open(args.did_file, encoding='utf-8') as did_file:
            did = json.load(did_file)
    else:
        # Get public verification keys from URL
        did = get_did_from_url()

    verification_keys = get_verification_keys(did)

    # Decode any valid QR codes in the image file
    qrcodes = pyzbar.pyzbar.decode(PIL.Image.open(args.qrcode_file))

    for qrcode in qrcodes:
        qrcode_data_segments = qrcode.data.decode().split('/')

        if qrcode_data_segments[0] != 'NZCP:':
            # Invalid
            continue
        if qrcode_data_segments[1] != '1':
            # Invalid
            continue

        # Decode base32 payload inside QR code
        qrcode_payload = base64.b32decode(qrcode_data_segments[2])

        # Decode and verify CWT inside QR code
        qrcode_cwt = cwt.decode(qrcode_payload, keys=verification_keys)

        # Print CWT
        yaml.dump(qrcode_cwt, sys.stdout)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import cwt
import subprocess
from jwcrypto import jwk
import json

def get_did(kid, public_key):
    pubkey = public_key.copy()
    del pubkey['key_ops']
    did_id = "did:web:nzcp.covid19.health.nz"
    id = "%s#%s" % (did_id, kid)
    did = {
        "@context": "https://w3.org/ns/did/v1",
        "id": did_id,
        "verificationMethod": [
            {
                "id": id,
                "controller": did_id,
                "type": "JsonWebKey2020",
                "publicKeyJwk": pubkey,
            },
        ],
        "assertionMethod": [
            id
        ]
    }
    return did


def main():
    parser = argparse.ArgumentParser(description='NZ COVID Pass Generate Key.')
    parser.add_argument('--kid', type=str, default="01",
                        help='key id to assign to the generated key')
    parser.add_argument('--private-key-file', required=True, type=str,
                        help='file name to save private key')
    parser.add_argument('--did-file', required=True, type=str,
                        help='file name to save DID document')

    args = parser.parse_args()

    key = jwk.JWK.generate(kty='EC', crv='P-256', kid=args.kid, key_ops=['sign'])
    private_key_json = key.export(private_key=True)
    private_key = json.loads(private_key_json)

    with open(args.private_key_file, 'w') as f:
        json.dump(private_key, f, indent=2)

    public_key_json = key.export(private_key=False)
    public_key = json.loads(public_key_json)
    
    did = get_did(args.kid, public_key)

    with open(args.did_file, 'w') as f:
        json.dump(did, f, indent=2)


if __name__ == "__main__":
    main()

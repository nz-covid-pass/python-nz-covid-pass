#!/usr/bin/env python3

import argparse
import base64
import json
import uuid

import cwt
import cbor2
import qrcode
from datetime import datetime, timezone


class NZCOVIDPassCWT(cwt.CWT):
    def _set_default_value(self, claims):
        return


def main():
    parser = argparse.ArgumentParser(description='NZ COVID Pass Generator.')
    parser.add_argument('--signing-key-file', type=str, required=True,
                        help='filename containing private signing key in JWK format')
    parser.add_argument('--qrcode-file', type=str, required=True,
                        help='filename where QR code should be saved')
    parser.add_argument('--dob', type=str, required=True,
                        help='date of birth for COVID Pass')
    parser.add_argument('--given-name', type=str, required=True,
                        help='given name for COVID Pass')
    parser.add_argument('--family-name', type=str, required=True,
                        help='family name for COVID Pass')
    parser.add_argument('--nbf', type=int, default=None,
                        help='nbf of NZ COVID Pass, default: current time')
    parser.add_argument('--cti', type=str, default=None,
                        help='cti of NZ COVID Pass, default: uuidv4')
    parser.add_argument('--validity', type=int, default=365,
                        help='validity of NZ COVID Pass in days, default: 365')

    args = parser.parse_args()

    # Generate random CTI
    cti = uuid.uuid4().bytes if args.cti is None else uuid.UUID(args.cti).bytes

    # Valid from now
    nbf = int(datetime.utcnow().timestamp()) if args.nbf == None else args.nbf

    # Set expiry date
    exp = nbf + (60 * 60 * 24 * args.validity)

    # Verifiable Credential CWT claim
    vc = {
        '@context': [
            'https://www.w3.org/2018/credentials/v1',
            'https://nzcp.covid19.health.nz/contexts/v1'
        ],
        'credentialSubject': {
            'dob': args.dob,
            'familyName': args.family_name,
            'givenName': args.given_name
        },
        'type': [
            'VerifiableCredential',
            'PublicCovidPass'
        ],
        'version': '1.0.0'
    }

    # NZ COVID Pass CWT claims
    claims = {
            1: 'did:web:nzcp.covid19.health.nz',
            4: exp,
            5: nbf,
            7: cti,
            'vc': vc
        }
    cwt_claims = cwt.Claims.new(claims)

    with open(args.signing_key_file, encoding='utf8') as signing_key_file:
        # Get private signing key
        private_signing_key = cwt.COSEKey.from_jwk(json.load(signing_key_file))

    # Sign our CWT
    cwt_claims = cwt_claims.to_dict()
    cwt.Claims.validate(cwt_claims)

    ctx = cwt.COSE.new(alg_auto_inclusion=True, kid_auto_inclusion=True)
    b_claims = cbor2.dumps(cwt_claims)
    res = ctx.encode_and_sign(b_claims, private_signing_key, { 4: private_signing_key.kid }, {}, out="cbor2/CBORTag")
    cwt_token = cbor2.dumps(res)

    # Create QR code data segments
    qrcode_data_segments = [
        'NZCP:',
        '1',
    ]

    # Encode base32 payload for QR code
    qrcode_payload = base64.b32encode(cwt_token).decode()
    qrcode_data_segments.append(qrcode_payload)

    # Make QR code
    qrcode_data = '/'.join(qrcode_data_segments)
    qrcode_img = qrcode.make(qrcode_data)
    qrcode_img.save(args.qrcode_file)


if __name__ == "__main__":
    main()

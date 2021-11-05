# Python NZ COVID Pass Verifier

This is quick proof of concept verifier I coded up in ~2 hours using various libraries to
parse the [NZ COVID Pass format](https://nzcp.covid19.health.nz/) as best as I could.

**Important note**: I don't know anything about CWT or CBOR and I'm using libraries that perform
cryptographic functions that I haven't vetted. Do not use this code for anything other than
learning and experimentation.

## Installing

```
$ pip3 install -r requirements.txt
$ sudo apt-get install python3-zbar
```

## Usage


```
usage: nz_covid_pass_verifier.py [-h] --qrcode-file QRCODE_FILE [--did-file DID_FILE]
```

Supply a QR code filename and optional DID document containing verification keys, if you omit
a DID document the official Ministry of Health verification keys will be used.

You can try with the sample QR codes provided:

```
$ python3 nz_covid_pass_verifier.py --qrcode-file examples/valid/nzcp.png --did-file examples/valid/did.json

iss: did:web:nzcp.covid19.health.nz
nbf: 2021-11-02 20:05:30+00:00
exp: 2031-11-02 20:05:30+00:00
vc:
  '@context':
  - https://www.w3.org/2018/credentials/v1
  - https://nzcp.covid19.health.nz/contexts/v1
  credentialSubject:
    dob: '1960-04-16'
    familyName: Sparrow
    givenName: Jack
  type:
  - VerifiableCredential
  - PublicCovidPass
  version: 1.0.0
jti: urn:uuid:60a4f54d-4e30-4332-be33-ad78b1eafa4b
```

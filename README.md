# Python NZ COVID Pass Verifier/Generator

This is quick proof of concept verifier I coded up in a few hours using various libraries to
parse and generate QR codes in the [NZ COVID Pass format](https://nzcp.covid19.health.nz/).

**Important note**: I don't know anything about CWT or CBOR and I'm using libraries that perform
cryptographic functions that I haven't vetted. Do not use this code for anything other than
learning and experimentation.

## Installing

```
$ sudo apt-get install python3-zbar
$ pip3 install -r requirements.txt
```

## Docker

```
docker build -t nzcovidpass .
docker run -v $(pwd):/app/qr --rm nzcovidpass --qrcode-file /app/qr/Image.jpg
```

## Usage

### Verify NZ COVID Pass

```
usage: nz_covid_pass_verifier.py [-h] --qrcode-file QRCODE_FILE [--did-file DID_FILE]

NZ COVID Pass Verifier.

required arguments:
  --qrcode-file QRCODE_FILE
                        file name containing NZ COVID pass QR code

optional arguments:
  -h, --help            show this help message and exit
  --did-file DID_FILE   file name containing DID with verification keys
```

Supply a QR code filename and optional DID document containing verification keys, if you omit
a DID document the official Ministry of Health verification keys will be used.

You can try with the sample QR codes provided:

```
$ python3 nz_covid_pass_verifier.py --qrcode-file examples/moh/valid/nzcp.png --did-file examples/moh/valid/did.json

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

### Generate NZ COVID Pass

```
usage: nz_covid_pass_generator.py [-h] --signing-key-file SIGNING_KEY_FILE --qrcode-file QRCODE_FILE --dob DOB --given-name GIVEN_NAME --family-name FAMILY_NAME [--validity VALIDITY]

NZ COVID Pass Generator.

required arguments:
  --signing-key-file SIGNING_KEY_FILE
                        filename containing private signing key in JWK format
  --qrcode-file QRCODE_FILE
                        filename where QR code should be saved
  --dob DOB             date of birth for COVID Pass
  --given-name GIVEN_NAME
                        given name for COVID Pass
  --family-name FAMILY_NAME
                        family name for COVID Pass

optional arguments:
  -h, --help            show this help message and exit
  --validity VALIDITY   validity of NZ COVID Pass in days, default: 365
```

Example:

```
python3 nz_covid_pass_generator.py \
    --dob "1986-07-14" --given-name "SpongeBob" --family-name "SquarePants" \
    --signing-key-file examples/mine/private_signing_key.json \
    --qrcode-file examples/mine/spongebob-squarepants.png
```

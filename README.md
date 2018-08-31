#** ECIES For MassGrid Wallet Import Format**
Dependencies
---------------------

These dependencies are required:

 Library     | Purpose          | Description
 ------------|------------------|----------------------
 python-ecdsa| ECDSA            | ECDSA For MassGrid Address
 pycrypto    | CRYPTO           | use ECIES encrypty

#### HoW to Use
```
python massgrid-wif-ecies.py --help
```
Usage
-----
```
usage: massgrid-wif-ecies.py [-h] [-e] [-a ADDRESS] [-s SIGNATURE]
                             [-m MESSAGE] [-p PUBLIC_KEY] [-d] [--get-address]
                             [--get-public-key] [--generate-private-key] [-v]
                             [-i]
                             [text]

Encrypt messages to bitcoin address holders using Elliptic Curve Integrated
Encryption Scheme.

positional arguments:
  text                  String to encrypt, decrypt, sign or verify. If not
                        specified, standard input will be used.

optional arguments:
  -h, --help            show this help message and exit
  -e, --encrypt         Encrypt a string. Requires -a, -p or both -s and -m.
  -a ADDRESS, --with-address ADDRESS
                        Try to look up the public key to encrypt with from a
                        specified bitcoin address. This requires the
                        blockchain.info API to return the correct public key
                        and will disclose the address to them when we look it
                        up. We verify the data from blockchain.info before
                        trusting it. If specified along with -s and -m, no
                        look-up is done, but we verify that the public key
                        derived from the signed message is the one belonging
                        to the bitcoin address specified. If specified along
                        with -p, no look-up is done, but we verify that the
                        public key provided is the one belonging to the
                        bitcoin address specified.
  -s SIGNATURE, --with-signature SIGNATURE
                        Derive the public key to encrypt with from a message
                        signed by the target bitcoin address. Requires -m as
                        well.
  -m MESSAGE, --with-message MESSAGE
                        Derive the public key to encrypt with from a message
                        signed by the target bitcoin address. Requires -s as
                        well.
  -p PUBLIC_KEY, --with-public-key PUBLIC_KEY
                        Use the provided hex-encoded public key to encrypt
                        with from a message signed by the target bitcoin
                        address. If specified with both -s and -m, we verify
                        that the public key derived from the signed message is
                        the same one provided.
  -d, --decrypt         Decrypt a string. Provide private key in Wallet Import
                        Format (obtained with the dumpprivkey console command
                        in the bitcoin client) in standard input, or first
                        line of standard input if encrypted text is also
                        provided on standard input. DO NOT PUT YOUR PRIVATE
                        KEY ON THE COMMAND LINE.
  --get-address         Convert a private key to a bitcoin address. Provide
                        private key in Wallet Import Format in standard input.
                        DO NOT PUT YOUR PRIVATE KEY ON THE COMMAND LINE.
  --get-public-key      Convert a private key to a public key. Provide private
                        key in Wallet Import Format in standard input. DO NOT
                        PUT YOUR PRIVATE KEY ON THE COMMAND LINE.
  --generate-private-key
                        Generate a random private key in Wallet Import Format.
  -v, --verify          Verify a message. Requires both -a and -s. Provide
                        message in arguments or in standard input.
  -i, --sign            Sign a message. Provide private key in Wallet Import
                        Format in standard input. DO NOT PUT YOUR PRIVATE KEY
                        ON THE COMMAND LINE.
```
Algorithm
---------
ECIES as described at
[Wikipedia](http://en.wikipedia.org/wiki/Integrated_Encryption_Scheme) using a
variation of ANSI-X9.63-KDF that uses SHA-256 instead of SHA-1 and HMAC-SHA-256
as the MAC. The symmetric encryption used is AES-256-CTR with a randomly
generated 64-bit prefix.

License
-------
MIT License.


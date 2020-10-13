# (c) 2019 Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.
#
# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
# PARTICULAR PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT,
# SPECIAL, PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE
# OF ANY KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF
# MICROCHIP HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE
# FORESEEABLE. TO THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL
# LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED
# THE AMOUNT OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR
# THIS SOFTWARE.
import json
from base64 import b64decode, b16encode
from argparse import ArgumentParser
import jose.jws
from jose.utils import base64url_decode, base64url_encode
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

parser = ArgumentParser(
    description='Verify and decode secure element manifest'
)

parser.add_argument(
    '--manifest',
    help='Manifest file to process',
    nargs=1,
    type=str,
    required=True,
    metavar='file'
)

args = parser.parse_args()

# Load manifest as JSON
with open(args.manifest[0], 'rb') as f:
    manifest = json.load(f)

# Process all the entries in the manifest
for i, signed_se in enumerate(manifest):
    print('')
    print('Processing entry {} of {}:'.format(i+1, len(manifest)))
    print('uniqueId: {}'.format(
        signed_se['header']['uniqueId']
    ))
    # Decode the protected header
    se = json.loads(
        base64url_decode(
        signed_se['payload'].encode('ascii')
        )
    )
    # Decode public keys and certificates
    try:
        public_keys = se['publicKeySet']['keys']
    except KeyError:
        public_keys = []
    for jwk in public_keys:
        # Decode any available certificates
        dev = False
        for cert_b64 in jwk.get('x5c', []):
            if (dev == False):
                cert = x509.load_der_x509_certificate(
                    data=b64decode(cert_b64),
                    backend=default_backend()
                )
                print(cert.public_bytes(
                    encoding=serialization.Encoding.PEM
                ).decode('ascii'))
                with open ('certs/' + signed_se['header']['uniqueId'], mode='w') as f:
                    f.write(cert.public_bytes(
                    encoding=serialization.Encoding.PEM
                    ).decode('ascii'))
                dev = True
            else:  
                dev = False
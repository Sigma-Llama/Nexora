from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import datetime
import ipaddress
import os

BASE_DIR = os.path.dirname(__file__)
KEY_PATH = os.path.join(BASE_DIR, 'key.pem')
CERT_PATH = os.path.join(BASE_DIR, 'cert.pem')

def generate():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"State"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Locality"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Nexora"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"127.0.0.1"),
    ])

    alt_names = [
        x509.DNSName(u"localhost"),
        x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
    ]

    # include common local IP if available in network
    try:
        alt_names.append(x509.IPAddress(ipaddress.IPv4Address('192.168.1.2')))
    except Exception:
        pass

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow() - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
        .add_extension(x509.SubjectAlternativeName(alt_names), critical=False)
        .sign(key, hashes.SHA256(), default_backend())
    )

    with open(KEY_PATH, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    with open(CERT_PATH, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Wrote key: {KEY_PATH}")
    print(f"Wrote cert: {CERT_PATH}")


if __name__ == '__main__':
    generate()

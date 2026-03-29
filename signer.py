from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


# =========================
# Generate RSA Keys
# =========================
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    # save private key
    with open("keys/private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # save public key
    with open("keys/public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print("Keys generated successfully.")


# =========================
# Sign metadata.json
# =========================
def sign_file(file_path="output/metadata.json", private_key_path="keys/private.pem"):
    # load private key
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # read file
    with open(file_path, "rb") as f:
        data = f.read()

    # sign
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # save signature
    with open("output/signature.sig", "wb") as f:
        f.write(signature)

    print("File signed successfully.")


# =========================
# Verify Signature
# =========================
def verify_signature(
    file_path="output/metadata.json",
    signature_path="output/signature.sig",
    public_key_path="keys/public.pem"
):
    try:
        # load public key
        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        # read file
        with open(file_path, "rb") as f:
            data = f.read()

        # read signature
        with open(signature_path, "rb") as f:
            signature = f.read()

        # verify
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("Signature is VALID. File is authentic.")

    except Exception:
        print("Signature is INVALID. File may have been tampered!")
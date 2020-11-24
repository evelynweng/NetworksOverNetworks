import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = algorithms.AES.block_size // 8  # Bits to bytes


class SymmetricEncryption():
    def __init__(self, key):
        self.cipher = Cipher(algorithms.AES(key), modes.ECB())

    def encrypt(self, plaintext: bytes) -> bytes:
        """ Encrypt the plaintext.

        Automatically fill padding follwing the origanl data if the
        plaintext length does not algin to AES blcok size. The padding
        format shwon as below (slightly diffrent from the PKCS5) :
            - Last padding bytes = number of padding bytes
            - Other: b'/0'

        If the plaintext length is 0, treat as a single 16 byte padding
        blocks.
        """
        blocks = len(plaintext) // 16
        padding_bytes = 16
        if plaintext:
            padding_bytes = (16 - (len(plaintext) - blocks*16)) % 16

        if padding_bytes:
            plaintext = plaintext.ljust((blocks+1)*BLOCK_SIZE - 1, b'\0')
            plaintext += bytes([padding_bytes])

        encryptor = self.cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

    def decrypt(self, ciphertext):
        """ Decrypt the ciphertext.

        Automatically remove the padding filled by the encrypt().
        """
        decryptor = self.cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding after decryption
        num_padding_zeros = 0
        for i in range(-2, -17, -1):
            if plaintext[i] != 0:  # At least have 1 block
                break
            num_padding_zeros += 1

        padding_bytes = plaintext[-1]
        if padding_bytes and padding_bytes <= num_padding_zeros + 1:
            if padding_bytes == len(plaintext):
                plaintext = b""
            else:
                plaintext = plaintext[:-padding_bytes]
        return plaintext


if __name__ == "__main__":
    # Simple Test
    from key_exchange import KeyExchange, DummyTarget
    target = DummyTarget("dummy")
    ke1, ke2 = KeyExchange(), KeyExchange()
    ke1.send(target)
    ke2.receive(target, target.payload)
    ke1.receive(target, target.payload)
    assert(ke1.get_key(target) == ke2.get_key(target))

    cipher = SymmetricEncryption(ke1.get_key(target))
    original = b"123"
    ciphertext = cipher.encrypt(original)
    plaintext = cipher.decrypt(ciphertext)
    assert(original == plaintext)

    original = ""
    for i in range(100):
        plaintext = cipher.decrypt(cipher.encrypt(original.encode())).decode()
        if original != plaintext:
            print("original:", original.encode())
            print("plaintext:", plaintext.encode())
            assert(False)
        original += chr(0)

    original = ""
    for i in range(255):
        plaintext = cipher.decrypt(cipher.encrypt(original.encode())).decode()
        if original != plaintext:
            print("original:", original.encode())
            print("plaintext:", plaintext.encode())
            assert(False)
        original += chr(i)

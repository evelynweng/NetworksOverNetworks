from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import UnsupportedAlgorithm




# Fix p and g
p = 9181996267556879192162191726499719294487423948474190238433087774282892382333874960175213074523555018329553686338367641297927841579321711497871729066844563
g = 2


class DiffieHellman():
    def __init__(self):
        self.parameter = dh.DHParameterNumbers(p, g).parameters()
        self._private = self.parameter.generate_private_key()
        self._public = self._private.public_key()

    def get_public(self) -> bytes:
        return self._public.public_bytes(
            encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)

    def share_secret(self, peer: bytes) -> bytes:
        return self._private.exchange(load_pem_public_key(peer))

class DummyTarget():
    def __init__(self, name: str):
        self.payload = None
        self.name = name

    def send(self, payload):
        self.payload = payload

    def __str__(self):
        return self.name

class KeyExchange:
    def __init__(self, callback=None, key_bits=256):
        self.dh = DiffieHellman()
        self.key_bits = key_bits
        # self.shared_keys = dict()

    def key_exchange_payload (self,target,shared_keys,init=True):
        # target should support __str__() and send()
        payload = self.dh.get_public()
        print("shared_keys type:",type(shared_keys))
        print("target type(str):",type(target))
        
        if init:
            print("shared_keys type:",type(shared_keys))
            print("target type(str):",type(target))
            shared_keys[str(target)] = None
        
        return payload

    def ack_key_exchange_payload(self, source,shared_keys, payload: bytes):
        #store shared_keys and return public_key
        try:
            share_secret = self.dh.share_secret(payload)
        except (ValueError, UnsupportedAlgorithm) as e:
            print(payload)
            raise

        derived_key = HKDF(
            algorithm=hashes.SHA256(), length=(self.key_bits//8),
            salt=None, info=b'handshake data',).derive(share_secret)
        print("save derived_key:",derived_key)
        shared_keys[str(source)] = derived_key
        
        return self.dh.get_public()

    
    def send(self, target, init=True):
        # target should support __str__() and send()
        target.send(self.dh.get_public())
        if init:
            self.shared_keys[str(target)] = None

    def receive(self, target, payload: bytes):
        # target should support __str__() and send()
        need_send = bool(shared_keys.get(str(target), 0) == 0)
        try:
            share_secret = self.dh.share_secret(payload)
        except (ValueError, UnsupportedAlgorithm) as e:
            print(payload)
            raise

        derived_key = HKDF(
            algorithm=hashes.SHA256(), length=(self.key_bits//8),
            salt=None, info=b'handshake data',).derive(share_secret)
        shared_keys[str(target)] = derived_key
        if need_send:
            self.send(target, init=False)

    def get_key(self, target):
        # Return fixed 256-bit key
        return shared_keys.get(str(target), None)

if __name__ == "__main__":
    # Simple Test
    target = DummyTarget("dummy")
    print("ke1 init key exchange with ke2.")
    ke1, ke2 = KeyExchange(), KeyExchange()

    print("\n=== Step 1 === ke1 -> ke2")
    ke1.send(target)
    ke2.receive(target, target.payload)
    print("ke2[target] = ", ke2.get_key(target))

    print("\n=== Step 2 === ke1 <- ke2")
    ke1.receive(target, target.payload)
    print("ke1[target] = ", ke1.get_key(target))

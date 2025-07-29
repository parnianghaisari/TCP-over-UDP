import struct
from caesar import CaesarCipher

class Packet:
    HEADER_FORMAT = '!II B H H'  # Format: seq_num (4), ack_num (4), flags (1), payload_len (2), window_size (2)
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, seq_num=0, ack_num=0, syn=False, ack=False, fin=False,
                 payload=b'', window_size=4096, encrypt=True):
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.syn = syn
        self.ack = ack
        self.fin = fin
        self.window_size = window_size

        if encrypt:
            try:
                # Attempt to decode payload as UTF-8 and encrypt it using Caesar cipher
                text = payload.decode('utf-8')
                encrypted = CaesarCipher.encrypt(text)
                self.payload = encrypted.encode('utf-8')
            except UnicodeDecodeError:
                # If decoding fails, treat as raw binary data
                self.payload = payload
        else:
            # If not encrypting (i.e., decrypting), use raw payload
            self.payload = payload

    def to_bytes(self):
        # Encode control flags into a single byte
        flags = (self.syn << 2) | (self.ack << 1) | self.fin

        # Pack header fields into bytes
        header = struct.pack(
            self.HEADER_FORMAT,
            self.seq_num,
            self.ack_num,
            flags,
            len(self.payload),
            self.window_size
        )

        return header + self.payload

    @classmethod
    def from_bytes(cls, data):
        # Extract header and payload from incoming byte stream
        header = data[:cls.HEADER_SIZE]
        payload = data[cls.HEADER_SIZE:]

        # Unpack header fields
        seq_num, ack_num, flags, payload_len, window_size = struct.unpack(cls.HEADER_FORMAT, header)
        syn = bool((flags >> 2) & 1)
        ack = bool((flags >> 1) & 1)
        fin = bool(flags & 1)
        payload = payload[:payload_len]

        # Attempt to decrypt payload using Caesar cipher
        try:
            text = payload.decode('utf-8')
            decrypted = CaesarCipher.decrypt(text)
            payload = decrypted.encode('utf-8')
        except Exception as e:
            print(f"[ERROR] Payload decryption failed: {e}")

        return cls(seq_num, ack_num, syn, ack, fin, payload, window_size, encrypt=False)

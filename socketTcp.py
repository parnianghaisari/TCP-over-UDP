from enum import Enum
import threading
import time
from packet import Packet

class SocketState(Enum):
    CLOSED = 0
    LISTEN = 1
    SYN_SENT = 2
    SYN_RECEIVED = 3
    ESTABLISHED = 4
    FIN_WAIT_1 = 5
    FIN_WAIT_2 = 6
    CLOSE_WAIT = 7
    LAST_ACK = 8
    TIME_WAIT = 9

class TCPSocket:
    def __init__(self, local_ip, local_port, remote_ip=None, remote_port=None, sock=None):
        self.local_ip = local_ip
        self.local_port = local_port
        self.remote_ip = remote_ip
        self.remote_port = remote_port

        self.state = SocketState.CLOSED
        self.seq_num = 1000
        self.ack_num = 0

        self.running = True
        self.send_lock = threading.Lock()
        self.recv_buffer = b""
        self.socket = sock

        # Start listening for incoming packets
        self.receiver_thread = threading.Thread(target=self.receive_loop)
        self.receiver_thread.start()

    def send_packet(self, pkt):
        """Sends a serialized packet over the UDP socket"""
        data = pkt.to_bytes()
        self.socket.sendto(data, (self.remote_ip, self.remote_port))

    def receive_loop(self):
        """Continuously receive packets and handle them"""
        while self.running:
            try:
                data, addr = self.socket.recvfrom(4096)
                packet = Packet.from_bytes(data)
                self.handle_packet(packet)
            except Exception:
                continue

    def handle_packet(self, packet):
        """Handles incoming packets based on current TCP-like state"""
        # Handle ACK for our FIN
        if packet.flags.get("ACK") and self.state == SocketState.FIN_WAIT_1:
            print("[INFO] Received ACK for our FIN. Waiting for peer's FIN...")
            self.state = SocketState.FIN_WAIT_2

        # Handle incoming FIN
        elif packet.flags.get("FIN"):
            print("[INFO] Received FIN from peer.")
            ack_pkt = Packet(
                src_port=self.local_port,
                dst_port=self.remote_port,
                seq_num=self.seq_num,
                ack_num=packet.seq_num + 1,
                flags={"ACK": True}
            )
            self.send_packet(ack_pkt)

            if self.state == SocketState.ESTABLISHED:
                # We're the passive closer — send our own FIN
                print("[INFO] Sending FIN to close connection.")
                fin_pkt = Packet(
                    src_port=self.local_port,
                    dst_port=self.remote_port,
                    seq_num=self.seq_num,
                    ack_num=packet.seq_num + 1,
                    flags={"FIN": True}
                )
                self.send_packet(fin_pkt)
                self.seq_num += 1
                self.state = SocketState.LAST_ACK

            elif self.state == SocketState.FIN_WAIT_2:
                # We're the active closer and now received FIN
                print("[INFO] FIN/ACK complete. Entering TIME_WAIT.")
                self.state = SocketState.TIME_WAIT
                self.running = False

        # Handle final ACK after sending our FIN
        elif packet.flags.get("ACK") and self.state == SocketState.LAST_ACK:
            print("[INFO] Received final ACK. Connection now closed.")
            self.state = SocketState.CLOSED
            self.running = False

    def close(self):
        """Initiates a graceful connection closure using FIN handshake"""
        print("[CLOSE] Sending FIN to initiate connection termination...")
        fin_pkt = Packet(
            src_port=self.local_port,
            dst_port=self.remote_port,
            seq_num=self.seq_num,
            ack_num=self.ack_num,
            flags={"FIN": True}
        )
        self.send_packet(fin_pkt)
        self.state = SocketState.FIN_WAIT_1
        self.seq_num += 1

        # Wait for connection to gracefully close
        timeout = 3
        start_time = time.time()
        while self.running and (time.time() - start_time < 30):
            time.sleep(1)

        # If not closed by timeout, force close
        if self.state != SocketState.CLOSED:
            print("[CLOSE] Timeout reached. Forcing connection closed.")
            self.running = False

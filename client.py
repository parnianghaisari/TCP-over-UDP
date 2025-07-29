import socket
import threading
from connection import TCPConnection
import time
def receive_loop(conn):
    while True:
        data = conn.recv()
        if data == b'':
            break
        if data:
            print(f"\n[SERVER] {data.decode(errors='replace')}")


def send_loop(conn):
    while True:
        try:
            msg = input("[CLIENT] Type message: ")
            if msg.lower() == "exit":
                conn.closed = True  # Signal to recv thread to stop reading
                time.sleep(0.2) 
                conn.close()
                break
            conn.send(msg.encode())
        except Exception:
            break


def send_test_scenario_1(conn):
    print("[SCENARIO 1] Cumulative ACK test with first segment dropped.")
    data = b"segment1segment2segment3"
    first_seq = conn.next_seq_num
    drop_seq = [first_seq]
    conn.send(data, drop_seq_nums=drop_seq)

def send_test_scenario_2(conn):
    print("[SCENARIO 2] Timeout retransmission by dropping first segment and waiting.")
    data = b"segment1"
    drop_seq = [conn.next_seq_num]
    conn.send(data, drop_seq_nums=drop_seq)

def send_test_scenario_3(conn):
    print("[SCENARIO 3] Fast retransmit with 3 duplicate ACKs (drop first segment).")
    data = b"segment1segment2segment3segment4"
    first_seq = conn.next_seq_num
    drop_seq = [first_seq]
    conn.send(data, drop_seq_nums=drop_seq)

def send_test_scenario_4(conn):
    print("[SCENARIO 4] Out-of-order delivery by reversing segment order.")
    segments = [b"segment1", b"segment2"]

    # Send segment 2 first
    conn.send(segments[1])
    time.sleep(0.2)

    # Then send segment 1
    conn.send(segments[0])
    time.sleep(0.2)

def send_test_scenario_5(conn):
    segment = b"segment1"

    print("[TEST] Sending segment 1")
    conn.send(segment)

    print("[TEST] Waiting to simulate ACK loss (drop ACK on server side or network)")
    time.sleep(5)

    print("[TEST] Done. Duplicate data should be handled gracefully.")

# def main():
#     SERVER_IP = "127.0.0.1"
#     SERVER_PORT = 12345
#     LOCAL_PORT = 54321
#     BUFFER_SIZE = 4096

#     # udp_socket.bind(("", LOCAL_PORT))
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.bind(("", 0))  # OS picks an available port
#     udp_socket.settimeout(1.0)

#     conn = TCPConnection(udp_socket, (SERVER_IP, SERVER_PORT))
#     conn.handle_handshake_client()

#     print(f"[CLIENT] Connected to server at {SERVER_IP}:{SERVER_PORT}")

#     time.sleep(0.1)  # Allow server to process ACK

    
#     recv_thread = threading.Thread(target=receive_loop, args=(conn,))
#     send_thread = threading.Thread(target=send_loop, args=(conn,))
#     recv_thread.start()
#     send_thread.start()

#     recv_thread.join()
#     send_thread.join()

#     print("[CLIENT] Connection closed.")

# if __name__ == "__main__":
#     main()


def main():
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 12345

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 0))
    udp_socket.settimeout(1.0)

    conn = TCPConnection(udp_socket, (SERVER_IP, SERVER_PORT))
    conn.handle_handshake_client()
    print(f"[CLIENT] Connected to {SERVER_IP}:{SERVER_PORT}")

    time.sleep(0.2)

    # فقط یکی از این‌ها را فعال کن:
    # send_test_scenario_1(conn)  # ACK تجمعی
    # send_test_scenario_2(conn)  # تایم‌اوت و بازارسال
    # send_test_scenario_3(conn)  # بازارسال سریع
    send_test_scenario_4(conn)  # دریافت خارج از ترتیب

    receive_loop(conn)

    conn.close()
    print("[CLIENT] Connection closed. Goodbye!")
if __name__ == "__main__":
    main()
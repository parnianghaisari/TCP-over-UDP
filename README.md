A Python implementation of TCP-like reliable data transfer over UDP. Supports:

Retransmissions and ACK handling
Cumulative ACKs and fast retransmit
Basic congestion control (AIMD)
Simulated packet loss and out-of-order delivery
RUN:
python receiver.py  # Start receiver
python sender.py 
Files
sender.py: Sends data over UDP with reliability and congestion control
receiver.py: Receives packets and sends ACKs
packet.py: Defines packet format and utilities


# TCP-over-UDP

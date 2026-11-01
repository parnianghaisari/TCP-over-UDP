# TCP-over-UDP – Reliable Data Transfer Protocol

**Computer Networks Course Project | Python**

## Overview

TCP-over-UDP is a Python-based implementation of TCP-like reliable data transfer over UDP. The project demonstrates how reliability and congestion control mechanisms can be built on top of an inherently unreliable transport protocol.

It implements key transport-layer mechanisms to ensure reliable packet delivery, handle packet loss, and manage data transmission under varying network conditions.

## Features

- **Reliable Data Transfer:** Implements retransmissions and acknowledgment (ACK) handling to ensure reliable packet delivery.
- **Cumulative Acknowledgments:** Uses cumulative ACKs to track successfully received data.
- **Fast Retransmit:** Detects potential packet loss and triggers retransmission without waiting for a timeout.
- **Congestion Control:** Implements a basic Additive Increase/Multiplicative Decrease (AIMD) mechanism to regulate the transmission rate.
- **Network Simulation:** Supports simulated packet loss and out-of-order packet delivery to test protocol reliability.

## Project Structure

| File | Description |
|---|---|
| `sender.py` | Sends data over UDP, handling retransmissions, acknowledgments, and congestion control. |
| `receiver.py` | Receives packets, processes incoming data, and sends acknowledgments. |
| `packet.py` | Defines the packet format and provides packet-related utilities. |

## How to Run

**1. Start the receiver:**

```bash
python receiver.py
```

**2. Start the sender in a separate terminal:**

```bash
python sender.py
```





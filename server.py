import socket
import os
import logging


logger = logging.getLogger(__name__)

BUFF_SIZE = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
sock.bind(("0.0.0.0", int(os.getenv("PROXY_PORT"))))
logger.info("Proxy server running")

while True:
    format_, sender = sock.recvfrom(BUFF_SIZE)
    format_ = format_.decode().strip()
    logger.info(f"Got request {format_}")
    is_big = 0
    if len(format_.split("_")) > 1:
        format_, is_big = format_.split("_")
        is_big = int(is_big)
    if format_ == "ALL":
        sock.sendto(b"1" if is_big else b"0", (os.getenv("MULTICAST_HOST"), int(os.getenv("MULTICAST_PORT"))))
        for _ in range(7):
            data, _ = sock.recvfrom(BUFF_SIZE)
            sock.sendto(data, sender)
            logger.info(f"Response {data} sent")
    else:
        sock.sendto(b"1" if is_big else b"0", (os.getenv(format_ + "_HOST"), int(os.getenv(format_ + "_PORT"))))
        data, _ = sock.recvfrom(BUFF_SIZE)
        sock.sendto(data, sender)
        logger.info(f"Response {data} sent")

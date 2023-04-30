import os
import socket
import struct
import logging
from tester import Tester
import serializers


logger = logging.getLogger(__name__)


BUFF_SIZE = 1024


if __name__ == "__main__":
    serializer_name = os.getenv("SERIALIZER_TYPE")
    tester = Tester(getattr(serializers, f"{serializer_name}Serializer"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("0.0.0.0", int(os.getenv("PORT", "2001"))))

    mreq = struct.pack('4sL', socket.inet_aton(os.getenv("MULTICAST_HOST")), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        is_big, sender = sock.recvfrom(BUFF_SIZE)
        logger.info(f"Got request: {is_big}")
        answer = tester.get_result(int(is_big))
        sock.sendto(answer.encode(), sender)

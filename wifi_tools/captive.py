"""Minimal captive redirection for the isolated training AP."""

import socket
import struct
import subprocess
import threading
import shutil


class WildcardDns:
    def __init__(self, address="10.42.0.1", port=5353):
        self.address = address
        self.port = port
        self._socket = None
        self._thread = None
        self._running = False

    def start(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(("0.0.0.0", self.port))
        self._running = True
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def _serve(self):
        while self._running:
            try:
                packet, client = self._socket.recvfrom(2048)
                if len(packet) < 12:
                    continue
                question_end = self._question_end(packet)
                if question_end is None:
                    continue
                question = packet[12:question_end]
                header = struct.pack("!HHHHHH", struct.unpack("!H", packet[:2])[0], 0x8180, 1, 1, 0, 0)
                answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 60, 4) + socket.inet_aton(self.address)
                self._socket.sendto(header + question + answer, client)
            except (OSError, struct.error):
                if self._running:
                    continue

    @staticmethod
    def _question_end(packet):
        index = 12
        while index < len(packet):
            length = packet[index]
            if length == 0:
                return index + 5
            if length & 0xC0 or index + length + 1 >= len(packet):
                return None
            index += length + 1
        return None

    def stop(self):
        self._running = False
        if self._socket:
            self._socket.close()
            self._socket = None


class RedirectRules:
    def __init__(self, interface="wlan0", http_port=8081, dns_port=5353):
        self.interface = interface
        self.http_port = str(http_port)
        self.dns_port = str(dns_port)
        self.binary = shutil.which("iptables-legacy") or "iptables"
        self.rules = [
            ["-t", "nat", "-A", "PREROUTING", "-i", interface, "-p", "udp", "--dport", "53", "-j", "REDIRECT", "--to-ports", self.dns_port],
            ["-t", "nat", "-A", "PREROUTING", "-i", interface, "-p", "tcp", "--dport", "53", "-j", "REDIRECT", "--to-ports", self.dns_port],
            ["-t", "nat", "-A", "PREROUTING", "-i", interface, "-p", "tcp", "--dport", "80", "-j", "REDIRECT", "--to-ports", self.http_port],
        ]
        self.applied = []

    def start(self):
        try:
            for rule in self.rules:
                subprocess.run([self.binary] + rule, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                self.applied.append(rule)
        except (OSError, subprocess.CalledProcessError):
            self.stop()
            raise RuntimeError("não foi possível configurar o redirecionamento do portal")

    def stop(self):
        for rule in reversed(self.applied):
            delete_rule = list(rule)
            delete_rule[2] = "-D"
            subprocess.run([self.binary] + delete_rule, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.applied = []

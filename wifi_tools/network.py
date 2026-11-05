"""Small, bounded wrappers around NetworkManager and Linux networking."""

import re
import subprocess


class CommandError(RuntimeError):
    pass


def run(args, timeout=15):
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip()
        raise CommandError(message or "command failed")
    return result.stdout.strip()


def status(interface="wlan0"):
    fields = run([
        "nmcli", "-t", "-f",
        "GENERAL.STATE,GENERAL.CONNECTION,GENERAL.HWADDR,IP4.ADDRESS,IP4.GATEWAY",
        "device", "show", interface,
    ])
    values = {}
    for line in fields.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key] = value.replace("\\:", ":")
    return values


def scan(interface="wlan0"):
    output = run([
        "nmcli", "-t", "-f", "SSID,BSSID,CHAN,SIGNAL,SECURITY",
        "device", "wifi", "list", "ifname", interface,
    ], timeout=30)
    networks = []
    for line in output.splitlines():
        parts = re.split(r"(?<!\\):", line)
        if len(parts) < 5:
            continue
        networks.append({
            "ssid": parts[0].replace("\\:", ":") or "<hidden>",
            "bssid": parts[1].replace("\\:", ":"),
            "channel": parts[2],
            "signal": parts[3],
            "security": parts[4] or "open",
        })
    return networks


def disconnect(interface="wlan0"):
    run(["nmcli", "device", "disconnect", interface])


def connect(ssid, password=None, interface="wlan0"):
    args = ["nmcli", "device", "wifi", "connect", ssid, "ifname", interface]
    if password:
        args.extend(["password", password])
    return run(args, timeout=30)


def hotspot_start(ssid, password, interface="wlan0"):
    if len(password) < 8:
        raise CommandError("AP password must have at least 8 characters")
    return run([
        "nmcli", "device", "wifi", "hotspot",
        "ifname", interface, "con-name", "WiFiTools-AP",
        "ssid", ssid, "password", password,
    ], timeout=30)


def hotspot_stop():
    return run(["nmcli", "connection", "down", "id", "WiFiTools-AP"], timeout=20)

"""Midterm Part 2: Scan TCP ports 20 through 443 on approved hosts only."""

import errno
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

START_PORT = 20
END_PORT = 443
TIMEOUT_SECONDS = 0.5
MAX_WORKERS = 32

# Add only IP addresses that you own or have explicit permission to scan.
APPROVED_HOSTS = {"127.0.0.1"}


def validate_target(user_input):
    """Validate an IP address and confirm that it is approved."""
    try:
        target = ipaddress.ip_address(user_input.strip())
    except ValueError as error:
        raise ValueError("Enter a valid IP address (example: 127.0.0.1).") from error

    if target.version != 4:
        raise ValueError("This scanner supports IPv4 addresses only.")

    if str(target) not in APPROVED_HOSTS:
        raise ValueError("Host is not approved. Add it to APPROVED_HOSTS only with permission.")

    return str(target)


def scan_port(host, port):
    """Return (port, status) for a single TCP connection attempt."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(TIMEOUT_SECONDS)
            result = sock.connect_ex((host, port))

        if result == 0:
            return port, "OPEN"
        if result == errno.ECONNREFUSED:
            return port, "CLOSED"
        if result in (errno.ETIMEDOUT, errno.EHOSTUNREACH, errno.ENETUNREACH):
            return port, "NO RESPONSE / FILTERED"
        return port, f"ERROR ({errno.errorcode.get(result, result)})"
    except socket.timeout:
        return port, "NO RESPONSE / FILTERED"
    except OSError as error:
        return port, f"ERROR ({error})"


def main():
    print("TCP Port Scanner | Ports 20-443 (inclusive)")
    print("Only scan systems you own or are authorized to test.")

    try:
        host = validate_target(input("Approved IPv4 address [127.0.0.1]: ") or "127.0.0.1")
        print(f"\nScanning {host} on TCP ports {START_PORT}-{END_PORT}...\n")

        results = {}
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(scan_port, host, port)
                       for port in range(START_PORT, END_PORT + 1)]
            for future in as_completed(futures):
                port, status = future.result()
                results[port] = status

        counts = {"OPEN": 0, "CLOSED": 0, "NO RESPONSE / FILTERED": 0, "ERROR": 0}
        for port in range(START_PORT, END_PORT + 1):
            status = results[port]
            print(f"Port {port:3d}: {status}")
            key = status if status in counts else "ERROR"
            counts[key] += 1

        print("\nScan complete.")
        print(f"Open: {counts['OPEN']} | Closed: {counts['CLOSED']} | "
              f"No response/filtered: {counts['NO RESPONSE / FILTERED']} | "
              f"Errors: {counts['ERROR']}")
        print("Note: 'No response/filtered' does not prove that a port is closed.")
    except ValueError as error:
        print(f"Input error: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nScan canceled by user.")
    except OSError as error:
        print(f"System error: {error}")


if __name__ == "__main__":
    main()

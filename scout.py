import socket # For the port scanning 
import requests # For talking to the Brain (Door 2)

# 1. UPDATE THIS with your Replit URL + /scout
BRAIN_URL = "https://c1ca03a5-32dd-4011-85a3-a80295f549be-00-1k9sg4r58b1as.riker.replit.dev/scout"

def scan_local_ports():
    target = "127.0.0.1" # Your own computer
    common_ports = [22, 80, 443, 8080, 5000]
    found_ports = []

    print(f"[Scout] Scanning {target} for open doors...")

    for port in common_ports:
        # Create a tiny connection attempt (the "knock")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1) # Fast scan
        result = s.connect_ex((target, port))

        if result == 0:
            print(f" [!] Port {port} is OPEN")
            found_ports.append(port)
        s.close()

def radio_home(findings):
    # Prepare the payload for Door 2
    payload = {
        "target_ip": "127.0.0.1",
            "status": f"Scan Complete. Open Ports: {findings}" if findings else "Secure: No open ports found."
    }

    try:
       response = requests.post(BRAIN_URL, json=payload)
       print(f"[Scout] Brain Response: {response.json().get('message')}")
    except Exception as e:
        print(f"[Scout] Error: {e}")

if __name__ == "__main__":
    results = scan_local_ports()
    radio_home(results)
                    
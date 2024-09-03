from scapy.all import sniff, TCP

def process_packet(packet):
    if packet.haslayer(TCP) and packet.haslayer('Raw'):
        # Extract HTTP headers and HTML content from the packet
        tcp_payload = packet['Raw'].load.decode('utf-8', errors='ignore')
        if 'HTTP' in tcp_payload:
            headers, _, html_content = tcp_payload.partition('\r\n\r\n')
            print("HTTP Headers:")
            print(headers)
            print("HTML Content:")
            print(html_content)

# Sniff network traffic on the specified interface (change 'eth0' to your interface)
sniff(filter="tcp port 443", prn=process_packet, iface="eth0")

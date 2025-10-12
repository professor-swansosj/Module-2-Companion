#!/usr/bin/env python3
"""
Module 2 - Script 9: F-Strings for Network Output Formatting
Purpose: Learn to use f-strings to format network command outputs professionally

This script demonstrates:
- F-string basics and syntax
- Formatting network data with f-strings
- Number formatting (IP addresses, percentages, etc.)
- Text alignment and padding
- Creating professional reports
- Combining f-strings with network automation

Learning Objectives:
- Master f-string syntax and capabilities
- Format network data professionally
- Create aligned tables and reports
- Use f-strings for network monitoring output
- Combine parsing with formatted output
- Build reusable formatting functions

Note: F-strings require Python 3.6 or later
"""

import json
import os
import datetime
from netmiko import ConnectHandler

def load_device_config():
    """Load device configuration from JSON file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, '..', '..', 'sample_data', 'devices.json')
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data['devices'][0]
    except FileNotFoundError:
        return {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'cisco123',
            'secret': 'enable123',
            'timeout': 20
        }

def demonstrate_fstring_basics():
    """
    Demonstrate basic f-string syntax and capabilities
    """
    
    print("="*70)
    print("F-STRING BASICS DEMONSTRATION")
    print("="*70)
    
    # Basic variable insertion
    hostname = "Router1"
    ip_address = "192.168.1.1"
    uptime_days = 45
    
    print("1. Basic Variable Insertion:")
    print("-" * 30)
    
    # Old ways (for comparison)
    print("Old % formatting:", "Device %s at %s has uptime %d days" % (hostname, ip_address, uptime_days))
    print("Old .format():", "Device {} at {} has uptime {} days".format(hostname, ip_address, uptime_days))
    
    # F-string way (Python 3.6+)
    print("F-string:", f"Device {hostname} at {ip_address} has uptime {uptime_days} days")
    
    # 2. Expression evaluation
    print("\n2. Expression Evaluation:")
    print("-" * 30)
    
    memory_used = 412542  # KB
    memory_total = 1048576  # KB
    
    print(f"Memory usage: {memory_used} KB / {memory_total} KB")
    print(f"Memory percentage: {(memory_used/memory_total)*100:.1f}%")
    print(f"Available memory: {memory_total - memory_used:,} KB")
    
    # 3. Function calls in f-strings
    print("\n3. Function Calls:")
    print("-" * 30)
    
    print(f"Current time: {datetime.datetime.now()}")
    print(f"Device name (upper): {hostname.upper()}")
    print(f"IP octets: {len(ip_address.split('.'))}")

def demonstrate_number_formatting():
    """
    Show number formatting options useful for network data
    """
    
    print("\n" + "="*70)
    print("NUMBER FORMATTING FOR NETWORK DATA")
    print("="*70)
    
    # Interface statistics
    bytes_in = 1234567890
    bytes_out = 987654321
    packets_in = 5678901
    utilization = 23.456789
    
    print("1. Basic Number Formatting:")
    print("-" * 30)
    
    print(f"Bytes in (raw): {bytes_in}")
    print(f"Bytes in (comma): {bytes_in:,}")
    print(f"Bytes in (underscore): {bytes_in:_}")
    print(f"Packets in (raw): {packets_in}")
    print(f"Packets in (comma): {packets_in:,}")
    
    print("\n2. Decimal Places:")
    print("-" * 30)
    
    print(f"Utilization (raw): {utilization}")
    print(f"Utilization (1 decimal): {utilization:.1f}%")
    print(f"Utilization (2 decimals): {utilization:.2f}%")
    
    print("\n3. Padding and Zero-filling:")
    print("-" * 30)
    
    vlan_id = 42
    interface_num = 5
    
    print(f"VLAN ID (padded): {vlan_id:4d}")
    print(f"VLAN ID (zero-filled): {vlan_id:04d}")
    print(f"Interface: GigE0/0/{interface_num:02d}")
    
    print("\n4. Data Size Formatting:")
    print("-" * 30)
    
    def format_bytes(bytes_value):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    print(f"Bytes in: {format_bytes(bytes_in)}")
    print(f"Bytes out: {format_bytes(bytes_out)}")

def demonstrate_text_alignment():
    """
    Show text alignment options for creating tables
    """
    
    print("\n" + "="*70)
    print("TEXT ALIGNMENT FOR TABLES")
    print("="*70)
    
    # Sample interface data
    interfaces = [
        {"name": "GigE0/0", "ip": "192.168.1.1", "status": "up", "speed": 1000},
        {"name": "GigE0/1", "ip": "10.0.0.1", "status": "down", "speed": 100},
        {"name": "Serial0/0", "ip": "172.16.1.1", "status": "up", "speed": 2},
        {"name": "Loopback0", "ip": "1.1.1.1", "status": "up", "speed": 8000}
    ]
    
    print("1. Left Alignment (default):")
    print("-" * 30)
    
    for intf in interfaces:
        print(f"{intf['name']:<12} {intf['ip']:<15} {intf['status']:<6} {intf['speed']} Mbps")
    
    print("\n2. Right Alignment:")
    print("-" * 30)
    
    for intf in interfaces:
        print(f"{intf['name']:>12} {intf['ip']:>15} {intf['status']:>6} {intf['speed']:>8} Mbps")
    
    print("\n3. Center Alignment:")
    print("-" * 30)
    
    for intf in interfaces:
        print(f"{intf['name']:^12} {intf['ip']:^15} {intf['status']:^6} {intf['speed']:^8} Mbps")
    
    print("\n4. Professional Table:")
    print("-" * 30)
    
    # Table header
    print(f"{'Interface':<12} {'IP Address':<15} {'Status':<8} {'Speed':>10}")
    print("-" * 50)
    
    # Table data with proper formatting
    for intf in interfaces:
        status_display = "UP" if intf['status'] == 'up' else "DOWN"
        print(f"{intf['name']:<12} {intf['ip']:<15} {status_display:<8} {intf['speed']:>7} Mbps")

def create_device_summary_report():
    """
    Create a comprehensive device summary using f-strings
    """
    
    print("\n" + "="*70)
    print("DEVICE SUMMARY REPORT EXAMPLE")
    print("="*70)
    
    # Sample device data (would come from actual device)
    device_data = {
        'hostname': 'CORE-SWITCH-01',
        'model': 'Cisco Catalyst 9300',
        'ios_version': '16.12.05',
        'uptime_days': 127,
        'uptime_hours': 14,
        'uptime_minutes': 23,
        'cpu_usage': 8.5,
        'memory_used': 445678,
        'memory_total': 1048576,
        'temperature': 42,
        'interfaces_total': 48,
        'interfaces_up': 24,
        'interfaces_down': 24,
        'power_usage': 125.7,
        'power_budget': 200.0
    }
    
    # Calculate derived values
    memory_percent = (device_data['memory_used'] / device_data['memory_total']) * 100
    uptime_str = f"{device_data['uptime_days']}d {device_data['uptime_hours']}h {device_data['uptime_minutes']}m"
    power_percent = (device_data['power_usage'] / device_data['power_budget']) * 100
    
    # Generate timestamp
    report_time = datetime.datetime.now()
    
    # Create formatted report
    report = f"""
┌{'─' * 68}┐
│{' NETWORK DEVICE STATUS REPORT ':^68}│
├{'─' * 68}┤
│ Device Information                                                 │
├{'─' * 68}┤
│ Hostname: {device_data['hostname']:<25} │ Model: {device_data['model']:<20} │
│ IOS Version: {device_data['ios_version']:<21} │ Uptime: {uptime_str:<19} │
├{'─' * 68}┤
│ Performance Metrics                                                │
├{'─' * 68}┤
│ CPU Usage: {device_data['cpu_usage']:>5.1f}%                    │ Memory: {memory_percent:>5.1f}% ({device_data['memory_used']:,} KB) │
│ Temperature: {device_data['temperature']:>3d}°C                     │ Power: {power_percent:>5.1f}% ({device_data['power_usage']:.1f}W) │
├{'─' * 68}┤
│ Interface Summary                                                  │
├{'─' * 68}┤
│ Total Interfaces: {device_data['interfaces_total']:>2d}              │ Up: {device_data['interfaces_up']:>2d}   Down: {device_data['interfaces_down']:>2d} │
├{'─' * 68}┤
│ Report Generated: {report_time.strftime('%Y-%m-%d %H:%M:%S')}                          │
└{'─' * 68}┘
    """
    
    print(report)

def format_interface_status_table(interfaces_data):
    """
    Create a formatted interface status table
    
    Args:
        interfaces_data (list): List of interface dictionaries
    """
    
    print("\n" + "="*70)
    print("INTERFACE STATUS TABLE")
    print("="*70)
    
    # Table header with f-string formatting
    header = f"{'Interface':<15} {'IP Address':<16} {'Status':<8} {'Protocol':<10} {'Description':<20}"
    print(header)
    print("─" * len(header))
    
    # Format each interface
    for intf in interfaces_data:
        # Color coding for status (simple text-based)
        status_display = "🟢 UP" if intf['status'].lower() == 'up' else "🔴 DOWN"
        protocol_display = "🟢 UP" if intf['protocol'].lower() == 'up' else "🔴 DOWN"
        
        row = f"{intf['interface']:<15} {intf['ip_address']:<16} {status_display:<8} {protocol_display:<10} {intf['description']:<20}"
        print(row)

def format_routing_table():
    """
    Format a routing table with f-strings
    """
    
    print("\n" + "="*70)
    print("ROUTING TABLE REPORT")
    print("="*70)
    
    # Sample routing data
    routes = [
        {"network": "0.0.0.0/0", "next_hop": "192.168.1.1", "interface": "GigE0/0", "metric": 1},
        {"network": "10.0.0.0/8", "next_hop": "10.1.1.1", "interface": "GigE0/1", "metric": 5},
        {"network": "172.16.0.0/12", "next_hop": "172.16.1.1", "interface": "Serial0/0", "metric": 10},
        {"network": "192.168.1.0/24", "next_hop": "0.0.0.0", "interface": "GigE0/0", "metric": 0}
    ]
    
    print(f"{'Network':<18} {'Next Hop':<15} {'Interface':<12} {'Metric':>8}")
    print("─" * 60)
    
    for route in routes:
        # Special formatting for directly connected routes
        next_hop_display = "Directly Connected" if route['next_hop'] == "0.0.0.0" else route['next_hop']
        
        print(f"{route['network']:<18} {next_hop_display:<15} {route['interface']:<12} {route['metric']:>8}")

def demo_with_real_device_data():
    """
    Demonstrate f-string formatting with real device data
    """
    
    print("\n" + "="*70)
    print("F-STRINGS WITH REAL DEVICE DATA")
    print("="*70)
    
    device = load_device_config()
    
    response = input(f"Connect to {device['host']} for real data demo? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Using sample data for demonstration...")
        demo_sample_data_formatting()
        return
    
    try:
        print(f"Connecting to {device['host']}...")
        connection = ConnectHandler(**device)
        print("✓ Connected successfully!")
        
        # Get device information
        hostname = connection.find_prompt().replace('#', '').replace('>', '')
        
        # Get show version info (simplified parsing)
        version_output = connection.send_command('show version')
        uptime_line = next((line for line in version_output.split('\n') if 'uptime' in line.lower()), "")
        
        # Get interface brief
        intf_output = connection.send_command('show ip interface brief')
        
        # Simple parsing for demo
        interface_lines = [line for line in intf_output.split('\n') 
                          if line.strip() and 'Interface' not in line and 'IP-Address' not in line]
        
        # Format device report
        print(f"\nDevice Report for {hostname}")
        print("─" * 50)
        print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Host IP: {device['host']}")
        
        if uptime_line:
            print(f"Uptime: {uptime_line.strip()}")
        
        print(f"Total interfaces found: {len(interface_lines)}")
        
        # Format interface summary
        print("\nInterface Summary:")
        print(f"{'Interface':<15} {'IP Address':<16} {'Status':<10}")
        print("─" * 45)
        
        for line in interface_lines[:5]:  # Show first 5 interfaces
            parts = line.split()
            if len(parts) >= 6:
                intf_name = parts[0]
                ip_addr = parts[1]
                status = parts[4]
                
                print(f"{intf_name:<15} {ip_addr:<16} {status:<10}")
        
        if len(interface_lines) > 5:
            print(f"... and {len(interface_lines) - 5} more interfaces")
        
        connection.disconnect()
        print("\n✓ Disconnected successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Using sample data instead...")
        demo_sample_data_formatting()

def demo_sample_data_formatting():
    """
    Demonstrate formatting with sample network data
    """
    
    # Sample interface data
    sample_interfaces = [
        {"interface": "GigE0/0", "ip_address": "192.168.1.1", "status": "up", "protocol": "up", "description": "WAN Connection"},
        {"interface": "GigE0/1", "ip_address": "unassigned", "status": "administratively down", "protocol": "down", "description": "Unused"},
        {"interface": "Loopback0", "ip_address": "1.1.1.1", "status": "up", "protocol": "up", "description": "Management"},
        {"interface": "Loopback100", "ip_address": "100.100.100.100", "status": "up", "protocol": "up", "description": "OSPF Router ID"}
    ]
    
    # Format the interface table
    format_interface_status_table(sample_interfaces)
    
    # Format routing table
    format_routing_table()

def main():
    """
    Main function - entry point
    """
    
    print("Module 2 - F-Strings for Network Output Formatting")
    print("Learn to create professional network reports with f-strings")
    
    try:
        # Basic f-string demonstrations
        demonstrate_fstring_basics()
        demonstrate_number_formatting()
        demonstrate_text_alignment()
        
        # Advanced formatting examples
        create_device_summary_report()
        
        # Real device demo (optional)
        demo_with_real_device_data()
        
        print("\n" + "="*70)
        print("F-STRINGS DEMO COMPLETE!")
        print("="*70)
        print("Key learning points:")
        print("1. F-strings provide clean, readable string formatting")
        print("2. Use formatting options for alignment and padding")
        print("3. Number formatting is essential for network data")
        print("4. F-strings work great for creating tables and reports") 
        print("5. Combine with network automation for professional output")
        print("6. F-strings are faster than older formatting methods")
        print("7. Expression evaluation makes f-strings very powerful")
        
        print("\nF-string formatting cheat sheet:")
        print("  {variable:<10}    - Left align, 10 characters wide")
        print("  {variable:>10}    - Right align, 10 characters wide")
        print("  {variable:^10}    - Center align, 10 characters wide")
        print("  {number:.2f}      - 2 decimal places")
        print("  {number:,}        - Thousands separator")
        print("  {number:04d}      - Zero-padded, 4 digits")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
    except Exception as e:
        print(f"\nScript error: {e}")

if __name__ == "__main__":
    main()
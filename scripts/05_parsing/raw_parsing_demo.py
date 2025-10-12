#!/usr/bin/env python3
"""
Module 2 - Script 7: Parsing Raw Output
Purpose: Learn to parse plain text command output from network devices

This script demonstrates:
- Challenges with parsing plain text output
- String manipulation techniques
- Regular expressions for pattern matching
- Extracting specific data from command output
- Converting text data to structured data

Learning Objectives:
- Understand difficulties of parsing unstructured text
- Use string methods (split, strip, find, etc.)
- Apply regular expressions for pattern matching
- Extract specific values from command output
- Convert parsed data to Python data structures
"""

import re
import json
import os
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

def demonstrate_parsing_challenges():
    """
    Show examples of common parsing challenges with raw text
    """
    
    print("="*70)
    print("PARSING CHALLENGES WITH RAW TEXT OUTPUT")
    print("="*70)
    
    # Sample raw output from 'show ip interface brief'
    sample_output = """Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         192.168.1.1     YES NVRAM  up                    up      
GigabitEthernet0/1         unassigned      YES NVRAM  administratively down down    
GigabitEthernet0/2         10.1.1.1        YES manual up                    up      
Loopback0                  1.1.1.1         YES NVRAM  up                    up      
Loopback100                100.100.100.100 YES manual up                    up      """
    
    print("Sample 'show ip interface brief' output:")
    print("-" * 50)
    print(sample_output)
    
    print("\n" + "="*70)
    print("PARSING CHALLENGES:")
    print("="*70)
    
    challenges = [
        "1. Inconsistent spacing between columns",
        "2. Variable length interface names", 
        "3. Header lines need to be skipped",
        "4. Some fields may contain spaces", 
        "5. Alignment issues with different data lengths",
        "6. Need to handle 'unassigned' vs IP addresses",
        "7. Status fields contain multiple words"
    ]
    
    for challenge in challenges:
        print(challenge)

def parse_with_string_methods(output):
    """
    Parse interface output using basic string methods
    
    Args:
        output (str): Raw command output
        
    Returns:
        list: List of interface dictionaries
    """
    
    print("\n" + "="*70)
    print("PARSING WITH STRING METHODS")
    print("="*70)
    
    interfaces = []
    lines = output.strip().split('\n')
    
    print(f"Total lines in output: {len(lines)}")
    
    # Skip header line(s)
    data_lines = []
    for line in lines:
        # Skip empty lines and header lines
        if line.strip() and 'Interface' not in line and 'IP-Address' not in line:
            data_lines.append(line)
    
    print(f"Data lines (after skipping headers): {len(data_lines)}")
    
    for i, line in enumerate(data_lines):
        print(f"\nParsing line {i+1}: '{line}'")
        
        # Method 1: Split by whitespace (problematic)
        parts = line.split()
        print(f"  Split by whitespace: {parts}")
        
        if len(parts) >= 6:
            interface_data = {
                'interface': parts[0],
                'ip_address': parts[1], 
                'ok': parts[2],
                'method': parts[3],
                'status': parts[4],
                'protocol': parts[5]
            }
            
            # Handle multiple word status
            if len(parts) > 6:
                interface_data['status'] = ' '.join(parts[4:-1])
                interface_data['protocol'] = parts[-1]
            
            interfaces.append(interface_data)
            print(f"  Parsed: {interface_data}")
        else:
            print("  ❌ Not enough parts to parse")
    
    return interfaces

def parse_with_fixed_positions(output):
    """
    Parse using fixed character positions (column-based)
    
    Args:
        output (str): Raw command output
        
    Returns:
        list: List of interface dictionaries  
    """
    
    print("\n" + "="*70)
    print("PARSING WITH FIXED POSITIONS")
    print("="*70)
    
    interfaces = []
    lines = output.strip().split('\n')
    
    # Define column positions based on header
    # Interface                  IP-Address      OK? Method Status                Protocol
    # 0        1         2         3         4         5         6         7
    # 012345678901234567890123456789012345678901234567890123456789012345678901234567890
    
    col_positions = {
        'interface': (0, 27),      # Interface name
        'ip_address': (27, 43),    # IP Address  
        'ok': (43, 47),            # OK status
        'method': (47, 54),        # Method
        'status': (54, 75),        # Status
        'protocol': (75, 85)       # Protocol
    }
    
    print("Column positions defined:")
    for field, (start, end) in col_positions.items():
        print(f"  {field}: positions {start}-{end}")
    
    for i, line in enumerate(lines):
        if 'Interface' in line or 'IP-Address' in line or not line.strip():
            continue
            
        print(f"\nParsing line {i+1}: '{line}'")
        
        # Extract data using fixed positions
        interface_data = {}
        
        for field, (start, end) in col_positions.items():
            if len(line) > start:
                value = line[start:end].strip()
                interface_data[field] = value
                print(f"  {field}: '{value}'")
            else:
                interface_data[field] = ""
                
        if interface_data.get('interface'):
            interfaces.append(interface_data)
    
    return interfaces

def parse_with_regex(output):
    """
    Parse using regular expressions for more robust parsing
    
    Args:
        output (str): Raw command output
        
    Returns:
        list: List of interface dictionaries
    """
    
    print("\n" + "="*70)
    print("PARSING WITH REGULAR EXPRESSIONS")
    print("="*70)
    
    interfaces = []
    
    # Regex patterns for different data types
    interface_pattern = r'^(\S+)\s+'                    # Interface name (non-whitespace)
    ip_pattern = r'(\d+\.\d+\.\d+\.\d+|unassigned)\s+'  # IP or 'unassigned'
    ok_pattern = r'(YES|NO)\s+'                          # OK status
    method_pattern = r'(\S+)\s+'                         # Method
    status_pattern = r'(.*?)\s+'                         # Status (may contain spaces)
    protocol_pattern = r'(\S+)$'                        # Protocol (end of line)
    
    # Combined regex pattern
    full_pattern = (interface_pattern + ip_pattern + ok_pattern + 
                   method_pattern + status_pattern + protocol_pattern)
    
    print(f"Regex pattern: {full_pattern}")
    
    lines = output.strip().split('\n')
    
    for i, line in enumerate(lines):
        if 'Interface' in line or 'IP-Address' in line or not line.strip():
            continue
            
        print(f"\nParsing line {i+1}: '{line}'")
        
        match = re.match(full_pattern, line)
        if match:
            groups = match.groups()
            print(f"  Regex groups: {groups}")
            
            interface_data = {
                'interface': groups[0],
                'ip_address': groups[1],
                'ok': groups[2], 
                'method': groups[3],
                'status': groups[4].strip(),
                'protocol': groups[5]
            }
            
            interfaces.append(interface_data)
            print(f"  Parsed: {interface_data}")
        else:
            print("  ❌ No regex match")
    
    return interfaces

def extract_specific_data(output):
    """
    Extract specific information from command output
    
    Args:
        output (str): Raw command output
        
    Returns:
        dict: Extracted statistics
    """
    
    print("\n" + "="*70)
    print("EXTRACTING SPECIFIC DATA")
    print("="*70)
    
    stats = {
        'total_interfaces': 0,
        'up_interfaces': 0,
        'down_interfaces': 0, 
        'assigned_ips': [],
        'unassigned_interfaces': []
    }
    
    lines = output.strip().split('\n')
    
    for line in lines:
        if 'Interface' in line or 'IP-Address' in line or not line.strip():
            continue
            
        stats['total_interfaces'] += 1
        
        # Check if interface is up
        if 'up' in line.lower():
            stats['up_interfaces'] += 1
        else:
            stats['down_interfaces'] += 1
        
        # Extract IP addresses
        ip_match = re.search(r'\b(\d+\.\d+\.\d+\.\d+)\b', line)
        if ip_match:
            stats['assigned_ips'].append(ip_match.group(1))
        elif 'unassigned' in line:
            # Extract interface name for unassigned interfaces
            interface_match = re.match(r'^(\S+)', line)
            if interface_match:
                stats['unassigned_interfaces'].append(interface_match.group(1))
    
    return stats

def compare_parsing_methods():
    """
    Compare different parsing methods on sample data
    """
    
    print("="*70)
    print("MODULE 2 - PARSING RAW OUTPUT COMPARISON")
    print("="*70)
    
    # Sample output for testing
    sample_output = """Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         192.168.1.1     YES NVRAM  up                    up      
GigabitEthernet0/1         unassigned      YES NVRAM  administratively down down    
GigabitEthernet0/2         10.1.1.1        YES manual up                    up      
Loopback0                  1.1.1.1         YES NVRAM  up                    up      
Loopback100                100.100.100.100 YES manual up                    up      """
    
    # Show the challenges first
    demonstrate_parsing_challenges()
    
    # Method 1: String methods
    print("\n" + "="*70)
    print("METHOD 1: STRING METHODS")
    print("="*70)
    string_result = parse_with_string_methods(sample_output)
    
    # Method 2: Fixed positions  
    print("\n" + "="*70)
    print("METHOD 2: FIXED POSITIONS")
    print("="*70)
    position_result = parse_with_fixed_positions(sample_output)
    
    # Method 3: Regular expressions
    print("\n" + "="*70)
    print("METHOD 3: REGULAR EXPRESSIONS")
    print("="*70)
    regex_result = parse_with_regex(sample_output)
    
    # Extract statistics
    print("\n" + "="*70)
    print("METHOD 4: EXTRACTING SPECIFIC DATA")
    print("="*70)
    stats = extract_specific_data(sample_output)
    print("Extracted statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Compare results
    print("\n" + "="*70)
    print("COMPARISON OF PARSING METHODS")
    print("="*70)
    print(f"String methods found: {len(string_result)} interfaces")
    print(f"Fixed positions found: {len(position_result)} interfaces")
    print(f"Regex method found: {len(regex_result)} interfaces")
    
    print("\nFirst interface comparison:")
    if string_result:
        print(f"String method: {string_result[0]}")
    if position_result:
        print(f"Position method: {position_result[0]}")
    if regex_result:
        print(f"Regex method: {regex_result[0]}")

def demo_with_real_device():
    """
    Demonstrate parsing with real device output
    """
    
    print("\n" + "="*70)
    print("PARSING WITH REAL DEVICE OUTPUT")
    print("="*70)
    
    device = load_device_config()
    print(f"Connecting to: {device['host']}")
    
    try:
        connection = ConnectHandler(**device)
        print("✓ Connected successfully!")
        
        # Get real output
        output = connection.send_command('show ip interface brief')
        
        print("\nRaw output from device:")
        print("-" * 50)
        print(output)
        
        # Parse with different methods
        print("\nParsing real output with regex method:")
        interfaces = parse_with_regex(output)
        
        print(f"\nFound {len(interfaces)} interfaces:")
        for interface in interfaces:
            print(f"  {interface['interface']}: {interface['ip_address']} ({interface['status']})")
        
        # Extract statistics from real data
        stats = extract_specific_data(output)
        print("\nReal device statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        connection.disconnect()
        print("\n✓ Disconnected successfully!")
        
    except Exception as e:
        print(f"❌ Error connecting to device: {e}")
        print("Using sample data for demonstration...")
        compare_parsing_methods()

def main():
    """
    Main function - entry point
    """
    
    print("Module 2 - Parsing Raw Output")
    print("Learn to extract data from plain text command output")
    
    try:
        # First show comparison with sample data
        compare_parsing_methods()
        
        # Then try with real device (if available)
        response = input("\nTry parsing with real device output? (yes/no): ").lower().strip()
        if response == 'yes':
            demo_with_real_device()
        
        print("\n" + "="*70)
        print("PARSING DEMO COMPLETE!")
        print("="*70)
        print("Key learning points:")
        print("1. Raw text parsing is challenging and error-prone")
        print("2. String methods work for simple, consistent formats")
        print("3. Fixed positions work when output is well-formatted")
        print("4. Regular expressions provide flexible pattern matching")
        print("5. Always validate parsing results")
        print("6. Consider using structured parsing libraries (next: NTC-Templates)")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
    except Exception as e:
        print(f"\nScript error: {e}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Module 2 - Script 4: Pretty Print Output
Purpose: Learn to format command output for better readability

This script demonstrates:
- Using pprint module for formatted output
- Creating custom formatting functions
- Comparing raw vs formatted output
- Organizing output for better analysis

Learning Objectives:
- Use Python's pprint module
- Create custom output formatting
- Structure command output
- Make output more readable
"""

import json
import os
import pprint
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

def pretty_print_command_output(command, output):
    """
    Format command output with headers and borders
    
    Args:
        command (str): The command that was executed
        output (str): The command output
    """
    
    border_char = "="
    border_length = 70
    
    print(f"\n{border_char * border_length}")
    print(f"COMMAND: {command}")
    print(f"{border_char * border_length}")
    print(output)
    print(f"{border_char * border_length}")

def pretty_print_with_line_numbers(command, output):
    """
    Print output with line numbers for easy reference
    
    Args:
        command (str): The command that was executed  
        output (str): The command output
    """
    
    print(f"\n{'='*70}")
    print(f"COMMAND (with line numbers): {command}")
    print(f"{'='*70}")
    
    lines = output.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        print(f"{line_num:3d}: {line}")
    
    print(f"{'='*70}")
    print(f"Total lines: {len(lines)}")

def format_interface_output(output):
    """
    Parse and format 'show ip interface brief' output
    
    Args:
        output (str): Raw command output
        
    Returns:
        list: List of interface dictionaries
    """
    
    interfaces = []
    lines = output.split('\n')
    
    # Skip header lines and process interface data
    for line in lines:
        line = line.strip()
        if not line or 'Interface' in line or 'IP-Address' in line:
            continue
            
        # Simple parsing - split by whitespace
        parts = line.split()
        if len(parts) >= 6:
            interface_data = {
                'interface': parts[0],
                'ip_address': parts[1],
                'ok': parts[2],
                'method': parts[3], 
                'status': parts[4],
                'protocol': parts[5]
            }
            interfaces.append(interface_data)
    
    return interfaces

def demo_pretty_printing():
    """
    Demonstrate various pretty printing techniques
    """
    
    print("="*70)
    print("MODULE 2 - PRETTY PRINTING OUTPUT DEMO")
    print("="*70)
    
    device = load_device_config()
    print(f"Connecting to: {device['host']}")
    
    try:
        connection = ConnectHandler(**device)
        print("✓ Connected successfully!")
        
        # 1. Basic pretty printing with borders
        print("\n" + "="*70)
        print("1. BASIC PRETTY PRINTING WITH BORDERS")
        print("="*70)
        
        output = connection.send_command('show clock')
        pretty_print_command_output('show clock', output)
        
        # 2. Pretty printing with line numbers
        print("\n" + "="*70)
        print("2. OUTPUT WITH LINE NUMBERS")
        print("="*70)
        
        output = connection.send_command('show version')
        pretty_print_with_line_numbers('show version', output)
        
        # 3. Structured data formatting
        print("\n" + "="*70) 
        print("3. STRUCTURED DATA FORMATTING")
        print("="*70)
        
        output = connection.send_command('show ip interface brief')
        interfaces = format_interface_output(output)
        
        print("Parsed interface data:")
        pprint.pprint(interfaces, width=100, depth=2)
        
        # 4. Custom formatting for specific data
        print("\n" + "="*70)
        print("4. CUSTOM FORMATTED TABLE")
        print("="*70)
        
        print(f"{'Interface':<20} {'IP Address':<15} {'Status':<10} {'Protocol':<10}")
        print("-" * 65)
        
        for interface in interfaces:
            print(f"{interface['interface']:<20} "
                  f"{interface['ip_address']:<15} "
                  f"{interface['status']:<10} "
                  f"{interface['protocol']:<10}")
        
        # 5. Dictionary output formatting
        print("\n" + "="*70)
        print("5. DEVICE INFORMATION DICTIONARY")
        print("="*70)
        
        device_info = {
            'hostname': connection.find_prompt().replace('#', '').replace('>', ''),
            'device_type': device['device_type'],
            'host': device['host'],
            'connection_time': 'Connected',
            'interfaces_count': len(interfaces),
            'up_interfaces': len([i for i in interfaces if i['status'].lower() == 'up'])
        }
        
        print("Device information:")
        pprint.pprint(device_info, width=50)
        
        # 6. Multiple commands with organized output
        print("\n" + "="*70)
        print("6. MULTIPLE COMMANDS - ORGANIZED OUTPUT")
        print("="*70)
        
        commands_to_run = [
            'show users',
            'show processes cpu | include CPU',
            'show memory statistics | include Total'
        ]
        
        for i, command in enumerate(commands_to_run, 1):
            output = connection.send_command(command)
            
            print(f"\n[{i}] {command}")
            print("-" * 50)
            print(output)
        
        connection.disconnect()
        print("\n✓ Disconnected successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def demo_pprint_module():
    """
    Demonstrate Python's pprint module features
    """
    
    print("\n" + "="*70)
    print("PYTHON PPRINT MODULE DEMONSTRATION")
    print("="*70)
    
    # Sample network data structure
    network_data = {
        'devices': [
            {
                'name': 'Router1',
                'interfaces': ['GigE0/0', 'GigE0/1', 'Loopback0'],
                'vlans': [1, 10, 20, 30],
                'neighbors': {
                    'Router2': {'interface': 'GigE0/1', 'ip': '192.168.1.2'},
                    'Switch1': {'interface': 'GigE0/0', 'ip': '192.168.1.10'}
                }
            },
            {
                'name': 'Switch1', 
                'interfaces': ['GigE1/0/1', 'GigE1/0/2', 'Vlan1'],
                'vlans': [1, 10, 20, 30, 40, 50],
                'neighbors': {
                    'Router1': {'interface': 'GigE1/0/1', 'ip': '192.168.1.1'}
                }
            }
        ]
    }
    
    # Regular print vs pprint
    print("1. Regular print():")
    print(network_data)
    
    print("\n2. Using pprint.pprint():")
    pprint.pprint(network_data)
    
    print("\n3. Using pprint with custom width:")
    pprint.pprint(network_data, width=60)
    
    print("\n4. Using pprint with limited depth:")
    pprint.pprint(network_data, depth=2)

def main():
    """
    Main function - entry point
    """
    
    print("Module 2 - Pretty Printing Output")
    print("Learn to format command output for better readability")
    
    try:
        # Demonstrate pprint module first
        demo_pprint_module()
        
        # Then demonstrate with real network commands
        demo_pretty_printing()
        
        print("\n" + "="*70)
        print("PRETTY PRINTING DEMO COMPLETE!")
        print("="*70)
        print("Key learning points:")
        print("1. Use borders and headers to organize output")
        print("2. Line numbers help with debugging and analysis") 
        print("3. Parse raw output into structured data")
        print("4. pprint module formats complex data structures")
        print("5. Custom formatting creates professional output")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
    except Exception as e:
        print(f"\nScript error: {e}")

if __name__ == "__main__":
    main()
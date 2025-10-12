#!/usr/bin/env python3
"""
Module 2 - Script 11: Functions for Network Automation
Purpose: Learn to structure network automation code with functions

This script demonstrates:
- Creating reusable functions for network tasks
- Function parameters and return values
- Docstring documentation standards
- Error handling within functions
- Function composition and modularity
- Creating a network automation library

Learning Objectives:
- Write functions for common network tasks
- Use proper function documentation
- Understand parameter passing and return values
- Create modular, reusable code
- Build a personal network automation library
- Apply DRY (Don't Repeat Yourself) principles
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Union, Optional

# Add path to import our network library
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def load_devices_from_json(json_path: str = None) -> List[Dict]:
    """
    Load device configurations from JSON file
    
    Args:
        json_path (str, optional): Path to JSON file. If None, uses default path.
        
    Returns:
        List[Dict]: List of device configuration dictionaries
        
    Raises:
        FileNotFoundError: If JSON file doesn't exist
        json.JSONDecodeError: If JSON file is malformed
        
    Example:
        >>> devices = load_devices_from_json('devices.json')
        >>> print(f"Loaded {len(devices)} devices")
    """
    
    if json_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', '..', 'sample_data', 'devices.json')
    
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            
        if 'devices' in data:
            return data['devices']
        else:
            return [data]  # Single device format
            
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        # Return sample device for demonstration
        return [{
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'cisco123',
            'secret': 'enable123',
            'name': 'Sample Router'
        }]
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {json_path}: {e}")
        return []

def create_connection_dict(host: str, username: str, password: str, 
                         device_type: str = 'cisco_ios', 
                         secret: str = None, timeout: int = 20) -> Dict:
    """
    Create a standardized connection dictionary for Netmiko
    
    Args:
        host (str): Device IP address or hostname
        username (str): Username for authentication
        password (str): Password for authentication
        device_type (str): Netmiko device type (default: cisco_ios)
        secret (str, optional): Enable secret password
        timeout (int): Connection timeout in seconds (default: 20)
        
    Returns:
        Dict: Connection parameters dictionary for Netmiko
        
    Example:
        >>> conn_params = create_connection_dict('192.168.1.1', 'admin', 'pass')
        >>> print(conn_params['host'])
        192.168.1.1
    """
    
    connection = {
        'device_type': device_type,
        'host': host,
        'username': username,
        'password': password,
        'timeout': timeout
    }
    
    if secret:
        connection['secret'] = secret
        
    return connection

def validate_ip_address(ip_string: str) -> bool:
    """
    Validate IPv4 address format
    
    Args:
        ip_string (str): IP address string to validate
        
    Returns:
        bool: True if valid IPv4 address, False otherwise
        
    Example:
        >>> validate_ip_address('192.168.1.1')
        True
        >>> validate_ip_address('999.999.999.999')
        False
    """
    
    try:
        import socket
        socket.inet_aton(ip_string)
        return True
    except socket.error:
        return False

def parse_interface_status(show_ip_int_brief_output: str) -> List[Dict]:
    """
    Parse 'show ip interface brief' output into structured data
    
    Args:
        show_ip_int_brief_output (str): Raw output from show ip interface brief
        
    Returns:
        List[Dict]: List of interface dictionaries with parsed data
        
    Example:
        >>> output = "Interface      IP-Address      OK? Method Status                Protocol\\nGigE0/0        192.168.1.1     YES NVRAM  up                    up"
        >>> interfaces = parse_interface_status(output)
        >>> print(interfaces[0]['interface'])
        GigE0/0
    """
    
    interfaces = []
    lines = show_ip_int_brief_output.strip().split('\n')
    
    # Skip header lines
    data_lines = []
    for line in lines:
        if ('Interface' in line and 'IP-Address' in line) or line.startswith('-'):
            continue
        if line.strip():
            data_lines.append(line)
    
    for line in data_lines:
        # Split by whitespace and handle variable spacing
        parts = line.split()
        if len(parts) >= 6:
            interface_data = {
                'interface': parts[0],
                'ip_address': parts[1] if parts[1] != 'unassigned' else None,
                'ok': parts[2],
                'method': parts[3],
                'status': parts[4],
                'protocol': parts[5]
            }
            interfaces.append(interface_data)
    
    return interfaces

def format_uptime(uptime_string: str) -> Dict[str, Union[int, str]]:
    """
    Parse and format device uptime from show version output
    
    Args:
        uptime_string (str): Uptime string from show version
        
    Returns:
        Dict[str, Union[int, str]]: Formatted uptime information
        
    Example:
        >>> uptime_info = format_uptime("Router uptime is 2 weeks, 3 days, 4 hours, 5 minutes")
        >>> print(f"{uptime_info['total_days']} days")
    """
    
    uptime_info = {
        'raw': uptime_string,
        'weeks': 0,
        'days': 0, 
        'hours': 0,
        'minutes': 0,
        'total_days': 0
    }
    
    # Extract numeric values using basic parsing
    import re
    
    week_match = re.search(r'(\d+)\s+week', uptime_string, re.IGNORECASE)
    if week_match:
        uptime_info['weeks'] = int(week_match.group(1))
    
    day_match = re.search(r'(\d+)\s+day', uptime_string, re.IGNORECASE) 
    if day_match:
        uptime_info['days'] = int(day_match.group(1))
        
    hour_match = re.search(r'(\d+)\s+hour', uptime_string, re.IGNORECASE)
    if hour_match:
        uptime_info['hours'] = int(hour_match.group(1))
        
    minute_match = re.search(r'(\d+)\s+minute', uptime_string, re.IGNORECASE)
    if minute_match:
        uptime_info['minutes'] = int(minute_match.group(1))
    
    # Calculate total days
    uptime_info['total_days'] = (uptime_info['weeks'] * 7 + 
                                uptime_info['days'] + 
                                uptime_info['hours'] / 24)
    
    return uptime_info

def generate_loopback_config(loopback_number: int, ip_address: str, 
                           subnet_mask: str = '255.255.255.255', 
                           description: str = None) -> List[str]:
    """
    Generate configuration commands for a loopback interface
    
    Args:
        loopback_number (int): Loopback interface number
        ip_address (str): IP address for the loopback
        subnet_mask (str): Subnet mask (default: /32)
        description (str, optional): Interface description
        
    Returns:
        List[str]: Configuration commands for the loopback interface
        
    Example:
        >>> commands = generate_loopback_config(100, '10.1.1.1', description='Test Loopback')
        >>> for cmd in commands:
        ...     print(cmd)
    """
    
    commands = [
        f'interface loopback {loopback_number}',
        f'ip address {ip_address} {subnet_mask}'
    ]
    
    if description:
        commands.insert(1, f'description {description}')
    
    commands.append('no shutdown')
    
    return commands

def create_vlan_config(vlan_id: int, vlan_name: Optional[str] = None) -> List[str]:
    """
    Generate VLAN configuration commands
    
    Args:
        vlan_id (int): VLAN ID number
        vlan_name (str, optional): VLAN name
        
    Returns:
        List[str]: VLAN configuration commands
        
    Example:
        >>> commands = create_vlan_config(100, 'Engineering')
        >>> print(commands)
    """
    
    commands = [f'vlan {vlan_id}']
    
    if vlan_name:
        commands.append(f'name {vlan_name}')
    
    return commands

def backup_filename_generator(device_name: str, config_type: str = 'running') -> str:
    """
    Generate standardized backup filename with timestamp
    
    Args:
        device_name (str): Name or hostname of the device
        config_type (str): Type of configuration (default: 'running')
        
    Returns:
        str: Formatted backup filename
        
    Example:
        >>> filename = backup_filename_generator('Router1', 'startup')
        >>> print(filename)
        Router1_startup_20231215_143022.cfg
    """
    
    # Clean device name (remove invalid filename characters)
    clean_name = "".join(c for c in device_name if c.isalnum() or c in ('-', '_'))
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    return f"{clean_name}_{config_type}_{timestamp}.cfg"

def calculate_subnet_info(network: str, subnet_mask: str) -> Dict[str, str]:
    """
    Calculate basic subnet information
    
    Args:
        network (str): Network address (e.g., '192.168.1.0')
        subnet_mask (str): Subnet mask (e.g., '255.255.255.0')
        
    Returns:
        Dict[str, str]: Subnet information including network, broadcast, etc.
        
    Example:
        >>> info = calculate_subnet_info('192.168.1.0', '255.255.255.0')
        >>> print(info['network'])
        192.168.1.0
    """
    
    # Basic subnet calculation (simplified for demonstration)
    try:
        import ipaddress
        
        # Convert to CIDR notation
        mask_parts = subnet_mask.split('.')
        cidr = sum([bin(int(part)).count('1') for part in mask_parts])
        
        network_obj = ipaddress.IPv4Network(f"{network}/{cidr}", strict=False)
        
        return {
            'network': str(network_obj.network_address),
            'broadcast': str(network_obj.broadcast_address),
            'netmask': subnet_mask,
            'cidr': f"/{cidr}",
            'num_hosts': network_obj.num_addresses - 2,
            'first_host': str(network_obj.network_address + 1),
            'last_host': str(network_obj.broadcast_address - 1)
        }
    except Exception:
        # Fallback for basic info
        return {
            'network': network,
            'netmask': subnet_mask,
            'error': 'Could not calculate subnet details'
        }

def filter_interfaces_by_status(interfaces: List[Dict], 
                              status: str = 'up') -> List[Dict]:
    """
    Filter interfaces by their operational status
    
    Args:
        interfaces (List[Dict]): List of interface dictionaries
        status (str): Status to filter by ('up', 'down', 'admin-down')
        
    Returns:
        List[Dict]: Filtered list of interfaces
        
    Example:
        >>> up_interfaces = filter_interfaces_by_status(all_interfaces, 'up')
        >>> print(f"Found {len(up_interfaces)} up interfaces")
    """
    
    return [intf for intf in interfaces 
            if intf.get('status', '').lower() == status.lower()]

def create_device_summary(device_info: Dict, interface_count: int, 
                         uptime_days: float) -> str:
    """
    Create a formatted device summary report
    
    Args:
        device_info (Dict): Device information dictionary
        interface_count (int): Number of interfaces
        uptime_days (float): Device uptime in days
        
    Returns:
        str: Formatted device summary
        
    Example:
        >>> summary = create_device_summary(device, 24, 45.5)
        >>> print(summary)
    """
    
    summary = f"""
Device Summary Report
=====================
Device: {device_info.get('name', device_info.get('host', 'Unknown'))}
IP Address: {device_info.get('host', 'N/A')}
Device Type: {device_info.get('device_type', 'N/A')}
Interface Count: {interface_count}
Uptime: {uptime_days:.1f} days
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
=====================
"""
    
    return summary.strip()

def demo_basic_functions():
    """
    Demonstrate basic utility functions
    """
    
    print("="*60)
    print("BASIC UTILITY FUNCTIONS DEMO")
    print("="*60)
    
    # Device loading function
    print("\n1. Loading Device Configuration:")
    print("-" * 40)
    devices = load_devices_from_json()
    print(f"Loaded {len(devices)} device(s)")
    
    if devices:
        device = devices[0]
        print(f"First device: {device.get('name', device.get('host'))}")
    
    # Connection dictionary creation
    print("\n2. Creating Connection Parameters:")
    print("-" * 40)
    conn_params = create_connection_dict(
        host='192.168.1.1',
        username='admin', 
        password='cisco123',
        secret='enable123'
    )
    print(f"Connection for: {conn_params['host']}")
    print(f"Device type: {conn_params['device_type']}")
    
    # IP address validation
    print("\n3. IP Address Validation:")
    print("-" * 40)
    test_ips = ['192.168.1.1', '10.0.0.1', '999.999.999.999', '192.168.1']
    
    for ip in test_ips:
        valid = validate_ip_address(ip)
        status = "✓ Valid" if valid else "✗ Invalid"
        print(f"{ip:15s} - {status}")

def demo_parsing_functions():
    """
    Demonstrate parsing and data processing functions
    """
    
    print("\n" + "="*60)
    print("PARSING FUNCTIONS DEMO")
    print("="*60)
    
    # Interface parsing
    print("\n1. Interface Status Parsing:")
    print("-" * 40)
    
    sample_output = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up      
GigabitEthernet0/1     unassigned      YES NVRAM  administratively down down    
Loopback0              10.1.1.1        YES NVRAM  up                    up      
Loopback100            172.16.1.1      YES manual up                    up"""
    
    interfaces = parse_interface_status(sample_output)
    print(f"Parsed {len(interfaces)} interfaces:")
    
    for intf in interfaces:
        status_icon = "🟢" if intf['status'] == 'up' else "🔴"
        print(f"  {status_icon} {intf['interface']:20s} {intf['ip_address'] or 'No IP':15s} {intf['status']}")
    
    # Uptime parsing
    print("\n2. Uptime Parsing:")
    print("-" * 40)
    
    uptime_samples = [
        "Router uptime is 2 weeks, 3 days, 4 hours, 23 minutes",
        "Switch uptime is 45 minutes",
        "System uptime: 1 day, 12 hours, 30 minutes"
    ]
    
    for uptime_str in uptime_samples:
        uptime_info = format_uptime(uptime_str)
        print(f"Raw: {uptime_str}")
        print(f"  -> {uptime_info['total_days']:.1f} total days")
        print(f"  -> {uptime_info['weeks']}w {uptime_info['days']}d {uptime_info['hours']}h {uptime_info['minutes']}m")

def demo_configuration_functions():
    """
    Demonstrate configuration generation functions
    """
    
    print("\n" + "="*60)
    print("CONFIGURATION FUNCTIONS DEMO") 
    print("="*60)
    
    # Loopback configuration
    print("\n1. Loopback Interface Configuration:")
    print("-" * 40)
    
    loopback_configs = [
        (100, '10.100.1.1', 'Management Loopback'),
        (200, '172.16.200.1', 'BGP Router ID'),
        (0, '1.1.1.1', None)  # No description
    ]
    
    for lo_num, lo_ip, lo_desc in loopback_configs:
        commands = generate_loopback_config(lo_num, lo_ip, description=lo_desc)
        print(f"Loopback {lo_num} configuration:")
        for cmd in commands:
            print(f"  {cmd}")
        print()
    
    # VLAN configuration
    print("2. VLAN Configuration:")
    print("-" * 40)
    
    vlans = [
        (10, 'Engineering'),
        (20, 'Sales'), 
        (100, None)  # No name
    ]
    
    for vlan_id, vlan_name in vlans:
        commands = create_vlan_config(vlan_id, vlan_name)
        print(f"VLAN {vlan_id} configuration:")
        for cmd in commands:
            print(f"  {cmd}")
        print()

def demo_utility_functions():
    """
    Demonstrate utility and helper functions
    """
    
    print("\n" + "="*60)
    print("UTILITY FUNCTIONS DEMO")
    print("="*60)
    
    # Filename generation
    print("\n1. Backup Filename Generation:")
    print("-" * 40)
    
    devices_names = ['Router-1', 'Core Switch #1', 'firewall@site-a']
    config_types = ['running', 'startup']
    
    for device_name in devices_names:
        for config_type in config_types:
            filename = backup_filename_generator(device_name, config_type)
            print(f"{device_name:20s} ({config_type:7s}) -> {filename}")
    
    # Subnet calculations
    print("\n2. Subnet Information:")
    print("-" * 40)
    
    subnets = [
        ('192.168.1.0', '255.255.255.0'),
        ('10.0.0.0', '255.255.0.0'),
        ('172.16.100.0', '255.255.255.240')
    ]
    
    for network, mask in subnets:
        info = calculate_subnet_info(network, mask)
        print(f"Network: {network}/{info.get('cidr', 'N/A')}")
        if 'num_hosts' in info:
            print(f"  Hosts: {info['num_hosts']}")
            print(f"  Range: {info['first_host']} - {info['last_host']}")
        print()

def demo_data_processing():
    """
    Demonstrate data filtering and processing functions
    """
    
    print("\n" + "="*60)
    print("DATA PROCESSING FUNCTIONS DEMO")
    print("="*60)
    
    # Create sample interface data
    sample_interfaces = [
        {'interface': 'GigE0/0', 'status': 'up', 'ip_address': '192.168.1.1'},
        {'interface': 'GigE0/1', 'status': 'down', 'ip_address': None},
        {'interface': 'GigE0/2', 'status': 'up', 'ip_address': '10.1.1.1'},
        {'interface': 'Loopback0', 'status': 'up', 'ip_address': '1.1.1.1'},
        {'interface': 'Serial0/0', 'status': 'admin-down', 'ip_address': None}
    ]
    
    print(f"\n1. Interface Filtering ({len(sample_interfaces)} total interfaces):")
    print("-" * 40)
    
    # Filter by different statuses
    statuses = ['up', 'down', 'admin-down']
    
    for status in statuses:
        filtered = filter_interfaces_by_status(sample_interfaces, status)
        print(f"{status.upper()} interfaces ({len(filtered)}):")
        for intf in filtered:
            print(f"  - {intf['interface']}")
    
    # Device summary
    print("\n2. Device Summary Report:")
    print("-" * 40)
    
    sample_device = {
        'name': 'Core-Router-1',
        'host': '192.168.1.1', 
        'device_type': 'cisco_ios'
    }
    
    summary = create_device_summary(sample_device, len(sample_interfaces), 45.7)
    print(summary)

def main():
    """
    Main function demonstrating network automation functions
    """
    
    print("Module 2 - Functions for Network Automation")
    print("Learn to create reusable, modular network automation code")
    
    # Run all demonstrations
    demo_basic_functions()
    demo_parsing_functions()
    demo_configuration_functions() 
    demo_utility_functions()
    demo_data_processing()
    
    print("\n" + "="*70)
    print("FUNCTIONS DEMO COMPLETE!")
    print("="*70)
    print("Key learning points:")
    print("1. Break complex tasks into smaller functions")
    print("2. Use descriptive function names and parameters")
    print("3. Write comprehensive docstrings for all functions")
    print("4. Use type hints to improve code clarity") 
    print("5. Return consistent data types")
    print("6. Handle errors appropriately within functions")
    print("7. Make functions testable and reusable")
    print("8. Follow the single responsibility principle")
    print("9. Use meaningful parameter and variable names")
    print("10. Consider default parameter values for common use cases")
    
    print("\nNext steps:")
    print("- Create your own network automation function library")
    print("- Practice writing functions for common tasks")
    print("- Test functions with different input scenarios")
    print("- Document functions thoroughly for future use")

if __name__ == "__main__":
    main()
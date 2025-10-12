#!/usr/bin/env python3
"""
Module 2 - Script 8: NTC-Templates Parsing
Purpose: Learn to use NTC-Templates for structured parsing of command output

This script demonstrates:
- Installing and using ntc-templates
- Structured parsing vs raw text parsing
- Available templates for common commands
- Converting unstructured text to structured data
- Benefits of using parsing libraries

Learning Objectives:
- Understand benefits of structured parsing
- Use ntc-templates library
- Compare structured vs raw parsing results
- Work with parsed data as Python objects
- Handle parsing errors gracefully

Note: This requires 'ntc-templates' package to be installed
"""

import json
import os
from netmiko import ConnectHandler

# Try to import ntc-templates
try:
    from ntc_templates.parse import parse_output
    NTC_AVAILABLE = True
except ImportError:
    from typing import Any, Dict, List
    NTC_AVAILABLE = False
    def parse_output(*args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        raise ImportError("ntc-templates not installed. Install with: pip install ntc-templates")
    print("❌ ntc-templates not installed. Install with: pip install ntc-templates")

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

def demonstrate_sample_parsing():
    """
    Demonstrate NTC parsing with sample data
    """
    
    if not NTC_AVAILABLE:
        print("NTC-Templates not available for demonstration")
        return
        
    print("="*70)
    print("NTC-TEMPLATES PARSING DEMONSTRATION")
    print("="*70)
    
    # Sample 'show version' output
    sample_version_output = """Cisco IOS Software, C2900 Software (C2900-UNIVERSALK9-M), Version 15.1(4)M4, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2012 by Cisco Systems, Inc.
Compiled Tue 20-Mar-12 17:58 by prod_rel_team

ROM: System Bootstrap, Version 15.0(1r)M15, RELEASE SOFTWARE (fc1)

Router1 uptime is 1 day, 2 hours, 15 minutes
System returned to ROM by power-on
System image file is "flash0:c2900-universalk9-mz.SPA.151-4.M4.bin"


This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

Cisco CISCO2911/K9 (revision 1.0) with 487424K/36864K bytes of memory.
Processor board ID FTX1628835W
3 Gigabit Ethernet interfaces
2 Serial interfaces
1 terminal line
DRAM configuration is 64 bits wide with parity disabled.
255K bytes of non-volatile configuration memory.
249856K bytes of ATA System CompactFlash 0 (Read/Write)


Technology Package License Information:

Technology    Technology-package           Technology-package
              Current       Type           Next reboot
-----------------------------------------------------------------
ipbase        ipbasek9      Permanent      ipbasek9
security      None          None           None
uc            None          None           None
data          None          None           None

Configuration register is 0x2102"""

    print("Sample 'show version' output (truncated):")
    print("-" * 50)
    print(sample_version_output[:500] + "...")
    
    try:
        # Parse with NTC-Templates
        parsed_data = parse_output(
            platform="cisco_ios",
            command="show version", 
            data=sample_version_output
        )
        
        print("\n✓ Successfully parsed with NTC-Templates!")
        print(f"Parsed data type: {type(parsed_data)}")
        print(f"Number of parsed elements: {len(parsed_data)}")
        
        if parsed_data and isinstance(parsed_data, list) and len(parsed_data) > 0:
            device_info = parsed_data[0]  # First (usually only) element
            
            print("\nParsed device information:")
            print(f"Hostname: {device_info.get('hostname', 'Not found')}")
            print(f"Version: {device_info.get('version', 'Not found')}")
            print(f"Uptime: {device_info.get('uptime', 'Not found')}")
            print(f"Serial: {device_info.get('serial', 'Not found')}")
            print(f"Model: {device_info.get('hardware', 'Not found')}")
            
            print("\nAll available parsed fields:")
            for key, value in device_info.items():
                print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"❌ Parsing failed: {e}")

def parse_interface_brief_sample():
    """
    Parse sample 'show ip interface brief' output with NTC-Templates
    """
    
    if not NTC_AVAILABLE:
        return
        
    print("\n" + "="*70)
    print("PARSING 'SHOW IP INTERFACE BRIEF' WITH NTC-TEMPLATES")
    print("="*70)
    
    sample_interface_output = """Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         192.168.1.1     YES NVRAM  up                    up      
GigabitEthernet0/1         unassigned      YES NVRAM  administratively down down    
GigabitEthernet0/2         10.1.1.1        YES manual up                    up      
Serial0/0/0                unassigned      YES NVRAM  administratively down down    
Serial0/0/1                unassigned      YES NVRAM  administratively down down    
Loopback0                  1.1.1.1         YES NVRAM  up                    up      
Loopback100                100.100.100.100 YES manual up                    up      """
    
    print("Sample interface brief output:")
    print("-" * 50)
    print(sample_interface_output)
    
    try:
        # Parse with NTC-Templates
        parsed_interfaces = parse_output(
            platform="cisco_ios",
            command="show ip interface brief",
            data=sample_interface_output
        )
        
        print(f"\n✓ Successfully parsed {len(parsed_interfaces)} interfaces!")
        
        print("\nParsed interfaces:")
        for i, interface in enumerate(parsed_interfaces, 1):
            print(f"{i:2d}. {interface.get('intf', 'Unknown')}: "
                  f"{interface.get('ipaddr', 'unassigned')} "
                  f"({interface.get('status', 'Unknown')}/{interface.get('proto', 'Unknown')})")
        
        # Show detailed structure
        if parsed_interfaces:
            print("\nDetailed structure of first interface:")
            first_interface = parsed_interfaces[0]
            for key, value in first_interface.items():
                print(f"  {key}: '{value}'")
        
        # Demonstrate data manipulation
        print("\nData analysis:")
        up_interfaces = [intf for intf in parsed_interfaces 
                        if intf.get('status', '').lower() == 'up']
        print(f"Interfaces that are up: {len(up_interfaces)}")
        
        assigned_interfaces = [intf for intf in parsed_interfaces 
                             if intf.get('ipaddr') != 'unassigned']
        print(f"Interfaces with IP addresses: {len(assigned_interfaces)}")
        
    except Exception as e:
        print(f"❌ Interface parsing failed: {e}")

def compare_raw_vs_structured_parsing():
    """
    Compare raw text parsing vs NTC-Templates parsing
    """
    
    print("\n" + "="*70)
    print("RAW PARSING VS STRUCTURED PARSING COMPARISON")
    print("="*70)
    
    sample_output = """Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         192.168.1.1     YES NVRAM  up                    up      
GigabitEthernet0/1         unassigned      YES NVRAM  administratively down down    """
    
    # Raw parsing (simple approach)
    print("1. RAW PARSING APPROACH:")
    print("-" * 30)
    
    lines = sample_output.strip().split('\n')
    raw_parsed = []
    
    for line in lines[1:]:  # Skip header
        if line.strip():
            parts = line.split()
            if len(parts) >= 6:
                interface_data = {
                    'interface': parts[0],
                    'ip_address': parts[1],
                    'status': parts[4],
                    'protocol': parts[5]
                }
                raw_parsed.append(interface_data)
    
    print("Raw parsing results:")
    for interface in raw_parsed:
        print(f"  {interface}")
    
    # Structured parsing with NTC-Templates
    if NTC_AVAILABLE:
        print("\n2. NTC-TEMPLATES STRUCTURED PARSING:")
        print("-" * 30)
        
        try:
            structured_parsed = parse_output(
                platform="cisco_ios",
                command="show ip interface brief",
                data=sample_output
            )
            
            print("Structured parsing results:")
            for interface in structured_parsed:
                print(f"  {interface}")
            
            print("\n3. COMPARISON:")
            print("-" * 30)
            print(f"Raw parsing found: {len(raw_parsed)} interfaces")
            print(f"Structured parsing found: {len(structured_parsed)} interfaces")
            
            print("\nAdvantages of structured parsing:")
            advantages = [
                "✓ Consistent field names across different commands",
                "✓ Handles edge cases and formatting variations",
                "✓ Maintained by network automation community",
                "✓ Reduces parsing code complexity",
                "✓ More reliable and tested",
                "✓ Supports many network platforms and commands"
            ]
            
            for advantage in advantages:
                print(f"  {advantage}")
                
        except Exception as e:
            print(f"❌ Structured parsing failed: {e}")
    else:
        print("\n2. NTC-TEMPLATES NOT AVAILABLE")
        print("Install with: pip install ntc-templates")

def demo_with_real_device():
    """
    Demonstrate NTC-Templates parsing with real device
    """
    
    if not NTC_AVAILABLE:
        print("NTC-Templates not available for real device demo")
        return
        
    print("\n" + "="*70)
    print("NTC-TEMPLATES WITH REAL DEVICE")
    print("="*70)
    
    device = load_device_config()
    print(f"Connecting to: {device['host']}")
    
    try:
        connection = ConnectHandler(**device)
        print("✓ Connected successfully!")
        
        # Commands to test with NTC-Templates
        test_commands = [
            'show version',
            'show ip interface brief',
            'show cdp neighbors'
        ]
        
        for command in test_commands:
            print("\n" + "-"*50)
            print(f"Testing: {command}")
            print("-"*50)
            
            try:
                # Get raw output
                raw_output = connection.send_command(command)
                
                # Parse with NTC-Templates
                parsed_data = parse_output(
                    platform=device['device_type'],
                    command=command,
                    data=raw_output
                )
                
                print(f"✓ Parsed {len(parsed_data)} items")
                
                # Show sample of parsed data
                if parsed_data:
                    print("Sample parsed data (first item):")
                    if isinstance(parsed_data[0], dict):
                        for key, value in list(parsed_data[0].items())[:5]:
                            print(f"  {key}: {value}")
                        if len(parsed_data[0]) > 5:
                            print(f"  ... and {len(parsed_data[0]) - 5} more fields")
                    else:
                        print(f"  {parsed_data[0]}")
                        
            except Exception as e:
                print(f"❌ Failed to parse '{command}': {e}")
        
        connection.disconnect()
        print("\n✓ Disconnected successfully!")
        
    except Exception as e:
        print(f"❌ Device connection error: {e}")

def show_available_templates():
    """
    Show information about available NTC-Templates
    """
    
    print("\n" + "="*70)
    print("AVAILABLE NTC-TEMPLATES")
    print("="*70)
    
    if not NTC_AVAILABLE:
        print("NTC-Templates not installed")
        return
    
    print("Common Cisco IOS templates include:")
    common_templates = [
        "show version",
        "show ip interface brief", 
        "show interfaces",
        "show ip route",
        "show cdp neighbors",
        "show cdp neighbors detail",
        "show vlan",
        "show spanning-tree",
        "show inventory",
        "show processes cpu",
        "show memory statistics"
    ]
    
    for template in common_templates:
        print(f"  ✓ {template}")
    
    print("\nSupported platforms include:")
    platforms = [
        "cisco_ios", "cisco_xe", "cisco_nxos", "cisco_asa",
        "juniper", "arista_eos", "fortinet", "paloalto_panos",
        "hp_procurve", "dell_force10", "extreme", "vyos"
    ]
    
    for platform in platforms:
        print(f"  ✓ {platform}")
    
    print("\nTo see all available templates:")
    print("  Visit: https://github.com/networktocode/ntc-templates")

def main():
    """
    Main function - entry point
    """
    
    print("Module 2 - NTC-Templates Structured Parsing")
    print("Learn to parse command output using structured templates")
    
    if not NTC_AVAILABLE:
        print("\n❌ ERROR: ntc-templates package not installed")
        print("Install with: pip install ntc-templates")
        print("Then run this script again.")
        return
    
    try:
        # Demonstrate with sample data
        demonstrate_sample_parsing()
        parse_interface_brief_sample()
        compare_raw_vs_structured_parsing()
        show_available_templates()
        
        # Option for real device demo
        response = input("\nTry NTC-Templates with real device? (yes/no): ").lower().strip()
        if response == 'yes':
            demo_with_real_device()
        
        print("\n" + "="*70)
        print("NTC-TEMPLATES DEMO COMPLETE!")
        print("="*70)
        print("Key learning points:")
        print("1. NTC-Templates converts text to structured data")
        print("2. Reduces parsing code complexity significantly")
        print("3. Handles edge cases and formatting variations")
        print("4. Community-maintained and tested templates")
        print("5. Supports many network platforms and commands")
        print("6. Returns consistent Python data structures")
        print("7. Much more reliable than custom text parsing")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
    except Exception as e:
        print(f"\nScript error: {e}")

if __name__ == "__main__":
    main()
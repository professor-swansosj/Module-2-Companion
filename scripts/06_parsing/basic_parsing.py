#!/usr/bin/env python3
"""
📊 Basic Parsing with NTC-Templates
Turn messy raw text into beautiful structured data!

Complete the TODOs to see the magic of structured parsing.
"""

import getpass
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output

def get_connection():
    """Reuse your connection code"""
    # TODO: Copy your secure connection code here
    pass

def demonstrate_raw_vs_parsed(connection):
    """
    Show the difference between raw and parsed output
    """
    print("📊 Raw vs Parsed Output Comparison")
    print("=" * 50)
    
    # TODO: Get show version output
    # raw_output = connection.send_command('show version')
    
    print("😵 RAW OUTPUT (messy):")
    print("-" * 30)
    # TODO: Print first 200 characters of raw output
    
    print("\n🎯 PARSED OUTPUT (structured):")  
    print("-" * 30)
    # TODO: Parse the output using ntc_templates
    # parsed = parse_output(platform='cisco_ios', command='show version', data=raw_output)
    
    # TODO: Print the hostname and version from parsed data
    # print(f"Hostname: {parsed[0]['hostname']}")
    # print(f"Version: {parsed[0]['version']}")

def extract_device_info(connection):
    """
    Extract specific device information
    """
    print("\n🎯 Extracting Device Information")
    print("=" * 40)
    
    # TODO: Get and parse show version
    
    # TODO: Extract and display:
    # - Hostname
    # - IOS Version  
    # - Model number
    # - Serial number
    # - Uptime
    
    pass

def parse_interface_data(connection):
    """
    Parse interface information into structured data
    """
    print("\n🔌 Parsing Interface Data") 
    print("=" * 30)
    
    # TODO: Get 'show ip interface brief' output
    
    # TODO: Parse it with NTC-Templates
    
    # TODO: Loop through interfaces and show:
    # - Interface name
    # - IP address  
    # - Status
    
    print("💡 Notice how easy it is to work with structured data!")

def main():
    """
    Demonstrate the power of parsing
    """
    print("📊 TextFSM and NTC-Templates Demo")
    print("=" * 50)
    
    try:
        connection = get_connection()
        
        demonstrate_raw_vs_parsed(connection)
        extract_device_info(connection) 
        parse_interface_data(connection)
        
        connection.disconnect()
        print("\n🎉 Parsing complete! Structured data is amazing!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
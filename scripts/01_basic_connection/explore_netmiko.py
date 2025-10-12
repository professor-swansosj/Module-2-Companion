#!/usr/bin/env python3
"""
Module 2 - Script 1: Exploring Netmiko Objects
Purpose: Learn to use dir(), help(), and inspect to understand Netmiko

This script demonstrates how to explore Python objects and their methods
before using them. This is a crucial skill for learning new libraries.

Learning Objectives:
- Use dir() to see available methods and attributes
- Use help() to read documentation 
- Use inspect module for detailed object information
- Understand Netmiko's ConnectHandler class structure
"""

# Import required modules
from netmiko import ConnectHandler
import inspect

def explore_netmiko():
    """
    Explore the Netmiko ConnectHandler class using Python's introspection tools
    """
    print("="*60)
    print("EXPLORING NETMIKO WITH PYTHON INTROSPECTION TOOLS")
    print("="*60)
    
    # 1. Use dir() to see all available methods and attributes
    print("\n1. Using dir() to see ConnectHandler methods:")
    print("-" * 50)
    
    methods = dir(ConnectHandler)
    
    # Filter to show only public methods (not starting with underscore)
    public_methods = [method for method in methods if not method.startswith('_')]
    
    print("Public methods available in ConnectHandler:")
    for i, method in enumerate(public_methods, 1):
        print(f"{i:2d}. {method}")
    
    # 2. Use help() to get detailed documentation
    print("\n\n2. Using help() to get documentation:")
    print("-" * 50)
    print("Getting help for ConnectHandler.send_command method...")
    print("(This will show detailed documentation)")
    
    # Uncomment the line below to see full help documentation
    # help(ConnectHandler.send_command)
    
    # Instead, let's show the docstring
    print("Docstring for send_command method:")
    print(ConnectHandler.send_command.__doc__)
    
    # 3. Use inspect to get method signatures
    print("\n\n3. Using inspect to examine method signatures:")
    print("-" * 50)
    
    # Get signature of send_command method
    try:
        sig = inspect.signature(ConnectHandler.send_command)
        print(f"send_command signature: {sig}")
    except ValueError:
        print("Could not get signature for send_command")
    
    # Get signature of send_config_set method  
    try:
        sig = inspect.signature(ConnectHandler.send_config_set)
        print(f"send_config_set signature: {sig}")
    except ValueError:
        print("Could not get signature for send_config_set")
        
    # 4. Explore specific method groups
    print("\n\n4. Categorizing methods by functionality:")
    print("-" * 50)
    
    # Connection methods
    connection_methods = [method for method in public_methods 
                         if 'connect' in method.lower() or 'disconnect' in method.lower()]
    print("Connection related methods:")
    for method in connection_methods:
        print(f"  - {method}")
    
    # Send methods  
    send_methods = [method for method in public_methods if 'send' in method.lower()]
    print("\nSend command methods:")
    for method in send_methods:
        print(f"  - {method}")
        
    # Config methods
    config_methods = [method for method in public_methods if 'config' in method.lower()]
    print("\nConfiguration methods:")
    for method in config_methods:
        print(f"  - {method}")
    
    # 5. Show some important attributes
    print("\n\n5. Examining class attributes and properties:")
    print("-" * 50)
    
    # Get all attributes that don't start with underscore
    attributes = [attr for attr in dir(ConnectHandler) 
                 if not attr.startswith('_') and not callable(getattr(ConnectHandler, attr, None))]
    
    if attributes:
        print("Class attributes:")
        for attr in attributes:
            print(f"  - {attr}")
    else:
        print("No public attributes found (most functionality is in methods)")

def explore_device_dictionary():
    """
    Show the structure of a device connection dictionary
    """
    print("\n\n" + "="*60)
    print("DEVICE CONNECTION DICTIONARY STRUCTURE")  
    print("="*60)
    
    # Example device dictionary
    device_example = {
        'device_type': 'cisco_ios',    # Type of device
        'host': '192.168.1.1',        # IP address or hostname
        'username': 'admin',          # Username for login
        'password': 'password',       # Password for login
        'secret': 'enable_secret',    # Enable password (optional)
        'port': 22,                   # SSH port (optional, default 22)
        'timeout': 20,                # Connection timeout (optional)
        'session_log': 'session.txt', # Log file (optional)
        'verbose': False,             # Debug output (optional)
    }
    
    print("\nRequired and optional parameters for device connection:")
    print("-" * 50)
    
    for key, value in device_example.items():
        if key in ['device_type', 'host', 'username', 'password']:
            required = "REQUIRED"
        else:
            required = "OPTIONAL"
            
        print(f"{key:15s}: {value:20s} ({required})")
    
    print("\nCommon device_type values:")
    device_types = [
        'cisco_ios', 'cisco_xe', 'cisco_nxos', 'cisco_asa',
        'juniper', 'arista_eos', 'hp_comware', 'fortinet'
    ]
    
    for device_type in device_types:
        print(f"  - {device_type}")

def main():
    """
    Main function - demonstrates exploration of Netmiko
    """
    print("Module 2 - Exploring Netmiko Objects")
    print("Learning to use dir(), help(), and inspect")
    
    try:
        # Explore the Netmiko library
        explore_netmiko()
        
        # Show device dictionary structure
        explore_device_dictionary()
        
        print("\n\n" + "="*60)
        print("EXPLORATION COMPLETE")
        print("="*60)
        print("Now you understand how to explore Python objects!")
        print("Next: Try creating a connection to a real device")
        
    except Exception as e:
        print(f"Error during exploration: {e}")

if __name__ == "__main__":
    main()
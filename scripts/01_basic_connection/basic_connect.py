#!/usr/bin/env python3
"""
Module 2 - Script 2: Basic Connection Script
Purpose: Create a basic connection to a Cisco device and test connectivity

This script demonstrates:
- How to define device connection parameters
- Establishing a connection with ConnectHandler
- Sending a simple command to verify connectivity
- Proper connection cleanup

Learning Objectives:
- Create device dictionary with connection parameters
- Use ConnectHandler to establish SSH connection
- Send basic show command
- Handle connection cleanup
- Basic error handling
"""

# Import required modules
from netmiko import ConnectHandler

def create_device_connection():
    """
    Define device connection parameters
    
    Returns:
        dict: Device connection parameters
    """
    
    # Device connection dictionary
    # MODIFY THESE VALUES FOR YOUR LAB ENVIRONMENT
    device = {
        'device_type': 'cisco_ios',        # Device type for Cisco IOS
        'host': '192.168.1.1',             # IP address - CHANGE THIS
        'username': 'admin',               # Username - CHANGE THIS  
        'password': 'cisco123',            # Password - CHANGE THIS
        'secret': 'enable123',             # Enable password - CHANGE THIS
        'timeout': 20,                     # Connection timeout in seconds
        'session_log': 'connection.log',   # Optional: log all interactions
    }
    
    return device

def test_basic_connection():
    """
    Test basic connection to device and run a simple command
    """
    
    print("="*60)
    print("MODULE 2 - BASIC NETMIKO CONNECTION TEST")
    print("="*60)
    
    # Get device connection parameters
    device = create_device_connection()
    
    print(f"Attempting to connect to: {device['host']}")
    print(f"Device type: {device['device_type']}")
    print(f"Username: {device['username']}")
    
    try:
        # Step 1: Establish connection
        print("\nStep 1: Establishing SSH connection...")
        connection = ConnectHandler(**device)
        print("✓ Connection successful!")
        
        # Step 2: Send a simple command to test connectivity
        print("\nStep 2: Testing connectivity with 'show clock' command...")
        output = connection.send_command('show clock')
        print("✓ Command executed successfully!")
        
        # Step 3: Display the output
        print("\nStep 3: Command output:")
        print("-" * 40)
        print(output)
        print("-" * 40)
        
        # Step 4: Get device prompt (optional)
        print(f"\nStep 4: Device prompt: {connection.find_prompt()}")
        
        # Step 5: Check if we're in enable mode
        print(f"In enable mode: {connection.check_enable_mode()}")
        
        # Step 6: Disconnect from device
        print("\nStep 6: Disconnecting from device...")
        connection.disconnect()
        print("✓ Disconnected successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed with error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check device IP address is reachable")
        print("2. Verify username and password are correct") 
        print("3. Ensure SSH is enabled on the device")
        print("4. Check if device_type matches your device")
        return False

def test_with_different_commands():
    """
    Test connection with multiple simple commands
    """
    
    print("\n" + "="*60)
    print("TESTING MULTIPLE COMMANDS")
    print("="*60)
    
    device = create_device_connection()
    
    # List of safe commands to test
    test_commands = [
        'show clock',
        'show version | include Version',
        'show ip interface brief | include up',
    ]
    
    try:
        print("Connecting to device...")
        connection = ConnectHandler(**device)
        
        for command in test_commands:
            print(f"\nExecuting: {command}")
            print("-" * 50)
            try:
                output = connection.send_command(command)
                print(output)
            except Exception as e:
                print(f"Command failed: {e}")
        
        connection.disconnect()
        print("\nAll commands completed!")
        
    except Exception as e:
        print(f"Connection error: {e}")

def main():
    """
    Main function - entry point of the script
    """
    print("Module 2 - Basic Netmiko Connection")
    print("Make sure to update device connection parameters!")
    
    # Test basic connection
    success = test_basic_connection()
    
    if success:
        # If basic connection works, try more commands
        test_with_different_commands()
        
        print("\n" + "="*60)
        print("SUCCESS! Basic connection is working")
        print("="*60)
        print("Next steps:")
        print("1. Try modifying the device parameters for your lab")
        print("2. Experiment with different show commands")
        print("3. Look at the session log file: connection.log")
    else:
        print("\n" + "="*60)
        print("CONNECTION FAILED - Please check configuration")
        print("="*60)

if __name__ == "__main__":
    main()
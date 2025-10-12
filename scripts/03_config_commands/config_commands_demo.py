#!/usr/bin/env python3
"""
Module 2 - Script 5: Configuration Commands
Purpose: Learn to send configuration commands with Netmiko

This script demonstrates:
- Difference between show and config commands
- Using send_config_set() for configuration changes
- Entering configuration mode automatically
- Saving configuration changes
- Best practices for configuration commands

Learning Objectives:
- Understand configuration vs show commands
- Use send_config_set() method
- Handle configuration mode transitions
- Save configuration to startup-config
- Verify configuration changes

WARNING: This script MODIFIES device configuration!
Only run on lab devices, never on production equipment!
"""

import json
import os
import time
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

def send_single_config_command(connection, command):
    """
    Send a single configuration command
    
    Args:
        connection: Netmiko connection object
        command (str): Configuration command to send
        
    Returns:
        str: Command output
    """
    
    print(f"\nSending configuration command: {command}")
    print("-" * 50)
    
    try:
        # send_config_set expects a list of commands
        output = connection.send_config_set([command])
        print("✓ Command sent successfully")
        print("Output:")
        print(output)
        return output
        
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return None

def send_multiple_config_commands(connection, commands):
    """
    Send multiple configuration commands as a set
    
    Args:
        connection: Netmiko connection object
        commands (list): List of configuration commands
        
    Returns:
        str: Command output
    """
    
    print(f"\nSending {len(commands)} configuration commands:")
    for i, cmd in enumerate(commands, 1):
        print(f"  {i}. {cmd}")
    
    print("-" * 50)
    
    try:
        # Send all commands together
        output = connection.send_config_set(commands)
        print("✓ All commands sent successfully")
        print("Output:")
        print(output)
        return output
        
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return None

def create_test_loopback(connection):
    """
    Create a test loopback interface
    
    Args:
        connection: Netmiko connection object
        
    Returns:
        bool: Success status
    """
    
    print("\n" + "="*60)
    print("CREATING TEST LOOPBACK INTERFACE")
    print("="*60)
    
    # Configuration commands for loopback interface
    config_commands = [
        'interface loopback 99',
        'ip address 99.99.99.99 255.255.255.255',
        'description Test Loopback Created by Python Script',
        'no shutdown'
    ]
    
    # Send configuration
    output = send_multiple_config_commands(connection, config_commands)
    
    if output is not None:
        # Verify the interface was created
        print("\nVerifying interface creation...")
        verify_output = connection.send_command('show ip interface brief | include Loopback99')
        
        if 'Loopback99' in verify_output:
            print("✓ Loopback99 interface created successfully!")
            print("Verification output:")
            print(verify_output)
            return True
        else:
            print("❌ Interface not found in verification")
            return False
    
    return False

def configure_hostname(connection, new_hostname):
    """
    Change device hostname (BE CAREFUL!)
    
    Args:
        connection: Netmiko connection object
        new_hostname (str): New hostname to set
        
    Returns:
        bool: Success status
    """
    
    print("\n" + "="*60)
    print(f"CHANGING HOSTNAME TO: {new_hostname}")
    print("="*60)
    print("WARNING: This will change the device hostname!")
    
    # Get current hostname for reference
    current_prompt = connection.find_prompt()
    print(f"Current prompt: {current_prompt}")
    
    # Send hostname command
    hostname_command = f'hostname {new_hostname}'
    output = send_single_config_command(connection, hostname_command)
    
    if output is not None:
        # Check new prompt (may take a moment to update)
        time.sleep(2)
        new_prompt = connection.find_prompt()
        print(f"New prompt: {new_prompt}")
        
        if new_hostname in new_prompt:
            print("✓ Hostname changed successfully!")
            return True
        else:
            print("❌ Hostname change may not have taken effect")
            return False
    
    return False

def configure_user_account(connection):
    """
    Create a new user account
    
    Args:
        connection: Netmiko connection object
        
    Returns:
        bool: Success status
    """
    
    print("\n" + "="*60)
    print("CREATING NEW USER ACCOUNT")
    print("="*60)
    
    # User configuration commands
    user_commands = [
        'username testuser privilege 1 password testpass123',
        'username testuser secret testpass123'
    ]
    
    output = send_multiple_config_commands(connection, user_commands)
    
    if output is not None:
        # Verify user was created
        print("\nVerifying user creation...")
        verify_output = connection.send_command('show running-config | include username testuser')
        
        if 'testuser' in verify_output:
            print("✓ User account created successfully!")
            print("User configuration:")
            print(verify_output)
            return True
        else:
            print("❌ User not found in running configuration")
            return False
    
    return False

def save_configuration(connection):
    """
    Save running configuration to startup configuration
    
    Args:
        connection: Netmiko connection object
        
    Returns:
        bool: Success status
    """
    
    print("\n" + "="*60)
    print("SAVING CONFIGURATION")
    print("="*60)
    print("Saving running-config to startup-config...")
    
    try:
        # Use send_command for 'write memory' or 'copy run start'
        output = connection.send_command('write memory')
        print("Save output:")
        print(output)
        
        if 'OK' in output or '[OK]' in output:
            print("✓ Configuration saved successfully!")
            return True
        else:
            print("❌ Configuration save may have failed")
            return False
            
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return False

def demo_configuration_commands():
    """
    Demonstrate various configuration commands
    """
    
    print("="*60)
    print("MODULE 2 - CONFIGURATION COMMANDS DEMO")
    print("="*60)
    print("WARNING: This script modifies device configuration!")
    print("Only use on lab devices!")
    
    # Ask for confirmation
    response = input("\nProceed with configuration changes? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Configuration demo cancelled by user")
        return
    
    device = load_device_config()
    print(f"\nConnecting to: {device['host']}")
    
    try:
        connection = ConnectHandler(**device)
        print("✓ Connected successfully!")
        
        # Ensure we're in enable mode
        if not connection.check_enable_mode():
            connection.enable()
            print("✓ Entered enable mode")
        
        # 1. Create test loopback interface
        success1 = create_test_loopback(connection)
        
        # 2. Create user account
        success2 = configure_user_account(connection)
        
        # 3. Optional: Change hostname (commented out for safety)
        print("\n" + "="*60)
        print("HOSTNAME CHANGE (DISABLED FOR SAFETY)")
        print("="*60)
        print("Hostname change is disabled to prevent issues.")
        print("To enable, uncomment the following line in the script:")
        print("# success3 = configure_hostname(connection, 'PythonTest')")
        
        # Uncomment the next line if you want to test hostname change
        # success3 = configure_hostname(connection, 'PythonTest')
        
        # 4. Show running config sections we modified
        print("\n" + "="*60)
        print("VERIFYING CONFIGURATION CHANGES")
        print("="*60)
        
        print("\nLoopback interfaces:")
        loopback_output = connection.send_command('show running-config | section interface Loopback')
        print(loopback_output)
        
        print("\nUser accounts:")
        user_output = connection.send_command('show running-config | include username')
        print(user_output)
        
        # 5. Save configuration
        save_success = save_configuration(connection)
        
        # Summary
        print("\n" + "="*60)
        print("CONFIGURATION SUMMARY")
        print("="*60)
        print(f"Loopback interface created: {'✓' if success1 else '❌'}")
        print(f"User account created: {'✓' if success2 else '❌'}")
        print(f"Configuration saved: {'✓' if save_success else '❌'}")
        
        connection.disconnect()
        print("\n✓ Disconnected successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def cleanup_test_config():
    """
    Remove test configuration (cleanup script)
    """
    
    print("="*60)
    print("CLEANUP TEST CONFIGURATION")
    print("="*60)
    
    response = input("Remove test configuration? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Cleanup cancelled")
        return
    
    device = load_device_config()
    
    try:
        connection = ConnectHandler(**device)
        print("✓ Connected for cleanup")
        
        # Remove test configurations
        cleanup_commands = [
            'no interface loopback 99',
            'no username testuser'
        ]
        
        output = send_multiple_config_commands(connection, cleanup_commands)
        
        if output:
            print("✓ Test configuration removed")
            save_configuration(connection)
        
        connection.disconnect()
        
    except Exception as e:
        print(f"Cleanup error: {e}")

def main():
    """
    Main function - entry point
    """
    
    print("Module 2 - Configuration Commands with Netmiko")
    print("Learn to modify device configuration safely")
    
    try:
        # Main configuration demo
        demo_configuration_commands()
        
        # Offer cleanup option
        print("\n" + "="*60)
        cleanup_response = input("\nRun cleanup to remove test config? (yes/no): ").lower().strip()
        if cleanup_response == 'yes':
            cleanup_test_config()
        
        print("\n" + "="*60)
        print("CONFIGURATION COMMANDS DEMO COMPLETE!")
        print("="*60)
        print("Key learning points:")
        print("1. Configuration commands modify device state")
        print("2. Use send_config_set() for configuration commands")
        print("3. Always verify configuration changes")
        print("4. Save configuration with 'write memory'")
        print("5. Test on lab devices only!")
        print("6. Have a rollback plan for production")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
    except Exception as e:
        print(f"\nScript error: {e}")

if __name__ == "__main__":
    main()
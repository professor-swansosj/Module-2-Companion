#!/usr/bin/env python3
"""
🔐 Secure Connection with getpass
Build your first secure network automation script!

Complete the TODOs to create a secure connection script.
"""

import getpass
from netmiko import ConnectHandler

def get_device_credentials():
    """
    Collect device credentials securely from the user
    """
    print("🔐 Secure Credential Collection")
    print("=" * 40)
    
    # TODO: Get the device IP address
    # Hint: host = input("Device IP Address: ")
    
    # TODO: Get the username  
    # Hint: username = input("Username: ")
    
    # TODO: Use getpass to hide the password input
    # Hint: password = getpass.getpass("Password: ")
    
    # TODO: Optional - get enable secret (can be empty)
    # Hint: Check if enable_secret is empty and set to None
    
    # TODO: Return a device dictionary
    device = {
        'device_type': 'cisco_ios',  # Assume Cisco IOS
        # Add your collected credentials here
    }
    
    return device

def test_connection(device):
    """
    Test the connection and run a simple command
    """
    print(f"\n🔌 Connecting to {device['host']}...")
    
    try:
        # TODO: Create the connection
        # Hint: connection = ConnectHandler(**device)
        
        print("✅ Connection successful!")
        
        # TODO: Send a simple test command
        # Hint: output = connection.send_command('show clock')
        
        # TODO: Print the command output
        
        # TODO: Don't forget to disconnect!
        # Hint: connection.disconnect()
        
        print("✅ Test complete!")
        return True
        
    except Exception as e:
        # TODO: Print a helpful error message
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """
    Main function - put it all together!
    """
    print("🚀 Secure Network Connection Script")
    print("=" * 50)
    
    try:
        # Get credentials securely
        device = get_device_credentials()
        
        # Test the connection
        success = test_connection(device)
        
        if success:
            print("\n🎉 Great job! You made a secure connection!")
        else:
            print("\n💡 Check your credentials and try again.")
            
    except KeyboardInterrupt:
        print("\n👋 Script cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    main()
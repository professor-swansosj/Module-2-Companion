#!/usr/bin/env python3
"""
📺 Basic Show Commands  
Execute show commands and observe the raw output

Complete the TODOs to see how messy raw output can be!
"""

import getpass
from netmiko import ConnectHandler

def get_connection():
    """
    Get a connection to your lab device
    """
    # TODO: Reuse your secure connection code from the previous exercise
    host = input("Device IP: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    
    device = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username, 
        'password': password
    }
    
    return ConnectHandler(**device)

def run_basic_commands(connection):
    """
    Run basic show commands and observe the output
    """
    print("📺 Running basic show commands...")
    
    # List of commands to try
    commands = [
        'show clock',
        'show version', 
        'show ip interface brief'
    ]
    
    for command in commands:
        print(f"\n{'='*50}")
        print(f"Command: {command}")
        print('='*50)
        
        # TODO: Send the command and get output
        # Hint: output = connection.send_command(command)
        
        # TODO: Print the raw output
        # TODO: Notice how messy it looks!
        
        # TODO: Also print the repr() of the output to see \n characters
        # Hint: print("Raw with escapes:", repr(output))

def analyze_output_challenges(connection):
    """
    See why raw output is challenging to work with
    """
    print("\n🔍 Analyzing output formatting challenges...")
    
    # TODO: Get 'show ip interface brief' output
    
    # TODO: Print the output normally
    
    # TODO: Split the output into lines and count them
    # Hint: lines = output.split('\n')
    
    # TODO: Show the first few lines
    
    # TODO: Try to find lines containing 'up' (interface status)
    
    print("\n💡 Notice how hard it is to extract specific information!")

def save_outputs_to_files(connection):
    """
    Save command outputs to files for later analysis
    """
    print("\n💾 Saving outputs to files...")
    
    commands_to_save = {
        'show_version.txt': 'show version',
        'show_interfaces.txt': 'show ip interface brief',
        'show_config.txt': 'show running-config'
    }
    
    for filename, command in commands_to_save.items():
        # TODO: Get command output
        
        # TODO: Save to file
        # Hint: with open(filename, 'w') as f: f.write(output)
        
        print(f"📄 Saved {command} to {filename}")

def main():
    """
    Main function - explore show commands and raw output
    """
    print("📺 Show Commands and Raw Output Explorer")
    print("=" * 50)
    
    try:
        # Connect to device
        connection = get_connection()
        print("✅ Connected successfully!")
        
        # Run the exercises
        run_basic_commands(connection)
        analyze_output_challenges(connection) 
        save_outputs_to_files(connection)
        
        # Clean up
        connection.disconnect()
        print("\n✅ All done! Check your saved files.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
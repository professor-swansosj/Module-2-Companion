"""
Module 02: Secure SSH Connection Foundations
Build your first network automation connection using secure practices

TODO: Import the modules you need and complete the connection
"""

def main():
    """
    Your secure connection script
    """
    
    # TODO 1: Import required modules
    # You'll need getpass for secure password input
    # You'll need ConnectHandler from netmiko for the connection
    
    # TODO 2: Collect connection information from user
    # Use input() for device IP and username
    # Use getpass.getpass() for password (hidden input)
    
    # TODO 3: Build device dictionary
    # Include device_type: 'cisco_ios'
    # Include the host, username, and password you collected
    
    # TODO 4: Establish connection
    # Use ConnectHandler with your device dictionary
    # Wrap in try/except for error handling
    
    # TODO 5: Test the connection
    # Send a simple command like 'show clock'
    # Print the output to verify it worked
    
    # TODO 6: Clean up
    # Always disconnect when finished
    
    print("Connection exercise complete!")

if __name__ == "__main__":
    main()
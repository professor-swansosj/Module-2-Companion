"""
Module 05: Configuration Commands
Safely make changes to network devices using automation

TODO: Complete the configuration exercises with proper safety practices
"""

def main():
    """
    Your configuration automation script
    """
    
    # TODO 1: Import modules and establish connection
    # Build on your previous connection skills
    # Connect to your lab device securely
    
    # TODO 2: Plan your configuration safely
    # ALWAYS verify current config first
    # Use 'show running-config interface' to see current state
    
    # TODO 3: Build configuration command list
    # Create commands to configure a loopback interface
    # Include: interface, ip address, description
    
    # TODO 4: Apply configuration with send_config_set()
    # Use this method for multiple configuration commands
    # Capture and print the output
    
    # TODO 5: Verify the configuration was applied
    # Use 'show running-config interface' again
    # Compare before and after to confirm changes
    
    # TODO 6: SAFETY PRACTICE - Document what you changed
    # Save configuration output to a file with timestamp
    # Always have a record of what automation changed
    
    print("Configuration exercise complete - changes documented!")

if __name__ == "__main__":
    main()
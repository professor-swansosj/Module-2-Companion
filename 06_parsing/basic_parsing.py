"""
Module 06: Parsing with NTC-Templates  
Convert raw text output into structured data for easy processing

TODO: Complete the parsing exercises to see structured data magic
"""

def main():
    """
    Your parsing practice script
    """
    
    # TODO 1: Import required modules
    # You'll need your connection modules from previous exercises
    # You'll also need: from ntc_templates.parse import parse_output
    
    # TODO 2: Connect and get raw output
    # Connect to your device securely
    # Get 'show version' output and save it as raw text
    
    # TODO 3: Compare raw vs parsed
    # Print the first 200 characters of raw output (ugly!)
    # Then use parse_output() to convert it to structured data
    
    # TODO 4: Access parsed data easily
    # Extract hostname, version, and uptime from the parsed data
    # Compare how easy this is vs string manipulation!
    
    # TODO 5: Parse interface data
    # Get 'show ip interface brief' output
    # Parse it and loop through the interfaces
    # Print interface name and status for each
    
    # TODO 6: Experiment with other commands
    # Try parsing 'show ip route' or other commands
    # See what structured data is available
    
    print("Parsing practice complete - structured data is powerful!")

if __name__ == "__main__":
    main()
"""
Module 03: Show Commands and Raw Output
Execute show commands and see why raw text is challenging

TODO: Build on your secure connection skills to explore command output
"""

def main():
    """
    Your show command exploration script
    """
    
    # TODO 1: Import modules and establish connection
    # Reuse your connection code from Module 02
    # Connect to your lab device securely
    
    # TODO 2: Execute basic show commands
    # Try: show clock, show version, show ip interface brief
    # Print the output from each command
    
    # TODO 3: Analyze the raw output structure  
    # Count how many lines each command produces
    # Look at the first and last few lines
    # Use repr() to see the \n and \r characters
    
    # TODO 4: Try to extract specific information
    # From 'show version' - find the hostname
    # From 'show ip interface brief' - find interfaces that are 'up'
    # See how difficult this is with raw text!
    
    # TODO 5: Save raw output to text files
    # Save each command output to a separate file
    # Open the files in a text editor to see the formatting
    
    print("Raw output analysis complete!")

if __name__ == "__main__":
    main()
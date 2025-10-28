"""
Module 01: Object Exploration Foundations
Learn to explore Python libraries using built-in tools

TODO: Complete the functions below to master object exploration
"""

# TODO: Import the modules you need
# Hint: You'll need netmiko's ConnectHandler and the inspect module

def main():
    """
    Your exploration playground
    """
    
    # TODO 1: Basic exploration
    # Use dir(ConnectHandler) to see what methods are available
    # Filter out the private methods (ones starting with '_')
    # Print how many public methods you found
    
    # TODO 2: Get documentation  
    # Use help() to read about the send_command method
    # What parameters does it take? Which are required?
    
    # TODO 3: Find specific methods
    # Look for all methods that have 'send' in their name
    # How many different ways can you send things to a device?
    
    # TODO 4: Method signatures
    # Use inspect.signature() to see the parameters for send_command
    # Do the same for send_config_set - how are they different?
    
    # TODO 5: Exception discovery
    # Import netmiko.exceptions and explore what's available
    # Which exceptions should you be prepared to handle?
    
    print("Exploration complete! You can now investigate any Python library.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
🔍 Exploring Netmiko Objects
Learn to use dir(), help(), and inspect() to understand new libraries

Your mission: Complete the TODOs below to master object exploration!
"""

from netmiko import ConnectHandler
import inspect

def explore_netmiko_methods():
    """
    Use dir() to discover what ConnectHandler can do
    """
    print("🔍 Discovering ConnectHandler methods...")
    
    # TODO: Use dir() to get all methods and attributes
    # Hint: methods = dir(ConnectHandler)
    
    # TODO: Filter to show only methods that don't start with '_'
    # Hint: Use list comprehension to filter methods
    
    # TODO: Print the public methods in a nice format
    
    print(f"Found {len('your_filtered_methods')} public methods!")  # Fix this line!

def get_method_help():
    """
    Use help() to understand what methods do
    """
    print("\n📖 Getting help on send_command...")
    
    # TODO: Use help() to get documentation for send_command
    # Hint: help(ConnectHandler.send_command)
    
    # TODO: Try getting just the docstring instead
    # Hint: print(ConnectHandler.send_command.__doc__)

def find_send_methods():
    """
    Find all methods that contain 'send'
    """
    print("\n🎯 Finding all 'send' methods...")
    
    # TODO: Get all methods using dir()
    
    # TODO: Filter for methods containing 'send'  
    # Hint: Use 'send' in method_name.lower()
    
    # TODO: Print each send method
    
    pass

def inspect_method_signatures():
    """
    Use inspect to see method parameters
    """
    print("\n🔬 Inspecting method signatures...")
    
    # TODO: Use inspect.signature() on send_command
    # Hint: sig = inspect.signature(ConnectHandler.send_command)
    
    # TODO: Do the same for send_config_set
    
    pass

def hunt_for_exceptions():
    """
    CHALLENGE: Find what exceptions Netmiko might raise
    """
    print("\n🏹 Exception hunting challenge...")
    
    # TODO: Import netmiko.exceptions
    # TODO: Use dir() to see what exceptions are available
    # TODO: Print the exception names
    
    print("💡 Hint: Look in netmiko.exceptions module!")

def main():
    """
    Complete each function above, then run this script!
    """
    print("🚀 Welcome to Netmiko Exploration!")
    print("=" * 50)
    
    explore_netmiko_methods()
    get_method_help() 
    find_send_methods()
    inspect_method_signatures()
    hunt_for_exceptions()
    
    print("\n🎉 Exploration complete!")
    print("Now you know how to explore ANY Python library!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
🏹 Exception Hunter Challenge!
Find all the exceptions Netmiko might raise

Complete the code below to become an exception detective!
"""

def find_netmiko_exceptions():
    """
    Your mission: Discover all Netmiko exceptions
    """
    print("🏹 Starting exception hunt...")
    
    # TODO: Import the netmiko.exceptions module
    # Hint: from netmiko import exceptions
    
    # TODO: Use dir() to see what's in the exceptions module
    
    # TODO: Filter for actual exception classes
    # Hint: Look for names that don't start with '_'
    
    # TODO: Print each exception with a brief description
    
    print("💡 Common exceptions you should handle:")
    print("   - NetmikoTimeoutException (connection timeouts)")  
    print("   - NetmikoAuthenticationException (login failures)")
    print("   - Add more as you discover them!")

def test_help_on_exceptions():
    """
    BONUS: Use help() to learn about specific exceptions
    """
    print("\n📚 Learning about exceptions...")
    
    # TODO: Try help() on NetmikoTimeoutException
    # TODO: Try help() on NetmikoAuthenticationException
    
    pass

if __name__ == "__main__":
    print("🎯 Exception Hunter Challenge")
    print("=" * 40)
    
    find_netmiko_exceptions()
    test_help_on_exceptions()
    
    print("\n✅ Challenge complete!")
    print("Now you know what to catch in try/except blocks!")
#!/usr/bin/env python3
"""
🧪 Connection Testing Lab
Test different connection scenarios to build confidence

Practice different ways to handle connections and errors.
"""

import getpass
from netmiko import ConnectHandler

def test_basic_connection():
    """
    Test a basic connection with minimal parameters
    """
    print("🧪 Test 1: Basic Connection")
    print("-" * 30)
    
    # TODO: Create a simple device dictionary
    device = {
        'device_type': 'cisco_ios',
        # Add required fields: host, username, password
    }
    
    # TODO: Try connecting and running 'show version'
    # Remember to handle exceptions!

def test_with_enable_secret():
    """
    Test connection with enable mode
    """
    print("\n🧪 Test 2: Connection with Enable Secret")
    print("-" * 40)
    
    # TODO: Get credentials including enable secret
    # TODO: Test connection and enter enable mode
    # TODO: Run a privileged command like 'show running-config'

def test_connection_timeout():
    """
    Test what happens with wrong IP address (timeout)
    """
    print("\n🧪 Test 3: Connection Timeout Test")
    print("-" * 35)
    
    # TODO: Use an unreachable IP like 192.168.999.999
    # TODO: Set a short timeout (e.g., 5 seconds)  
    # TODO: See what exception you get

def test_authentication_failure():
    """
    Test what happens with wrong credentials
    """
    print("\n🧪 Test 4: Authentication Failure Test")
    print("-" * 40)
    
    # TODO: Use wrong username/password on purpose
    # TODO: See what exception you get
    # TODO: This helps you learn what to catch in try/except

if __name__ == "__main__":
    print("🧪 Connection Testing Laboratory")
    print("=" * 50)
    print("Run each test to understand different scenarios!")
    
    # Uncomment tests one at a time
    # test_basic_connection()
    # test_with_enable_secret() 
    # test_connection_timeout()
    # test_authentication_failure()
    
    print("\n💡 Tip: Run one test at a time to learn from each scenario!")
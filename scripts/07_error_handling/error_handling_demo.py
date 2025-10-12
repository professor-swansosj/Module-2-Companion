#!/usr/bin/env python3
"""
Module 2 - Script 10: Error Handling in Network Automation
Purpose: Learn proper error handling for network automation scripts

This script demonstrates:
- Common network automation errors
- Using try/except blocks effectively
- Specific Netmiko exceptions
- Graceful error recovery
- Logging errors for troubleshooting
- Best practices for production scripts

Learning Objectives:
- Identify common network automation errors
- Use appropriate exception handling
- Implement graceful error recovery
- Log errors for debugging
- Create robust network automation scripts
- Handle connection and command failures
"""

import json
import os
import logging
import time
import socket
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException, 
    SSHException
)

def setup_logging():
    """
    Configure logging for the script
    
    Returns:
        logging.Logger: Configured logger
    """
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/network_automation.log'),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    return logging.getLogger(__name__)

def load_device_config():
    """Load device configuration from JSON file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, '..', '..', 'sample_data', 'devices.json')
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data['devices'][0]
    except FileNotFoundError:
        return {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'cisco123',
            'secret': 'enable123',
            'timeout': 20
        }

def validate_device_parameters(device_params):
    """
    Validate device connection parameters
    
    Args:
        device_params (dict): Device connection parameters
        
    Returns:
        tuple: (is_valid, error_message)
    """
    
    required_fields = ['device_type', 'host', 'username', 'password']
    
    for field in required_fields:
        if field not in device_params:
            return False, f"Missing required field: {field}"
        if not device_params[field]:
            return False, f"Empty value for required field: {field}"
    
    # Basic IP address validation
    try:
        socket.inet_aton(device_params['host'])
    except socket.error:
        return False, f"Invalid IP address format: {device_params['host']}"
    
    return True, "Validation successful"

def safe_connect_to_device(device_params, logger):
    """
    Safely connect to a network device with comprehensive error handling
    
    Args:
        device_params (dict): Device connection parameters
        logger (logging.Logger): Logger instance
        
    Returns:
        tuple: (connection_object, error_message)
    """
    
    logger.info(f"Attempting to connect to {device_params['host']}")
    
    try:
        # Validate parameters first
        is_valid, validation_error = validate_device_parameters(device_params)
        if not is_valid:
            logger.error(f"Parameter validation failed: {validation_error}")
            return None, validation_error
        
        # Attempt connection
        connection = ConnectHandler(**device_params)
        logger.info(f"Successfully connected to {device_params['host']}")
        return connection, None
        
    except NetmikoTimeoutException as e:
        error_msg = f"Connection timeout to {device_params['host']}: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
        
    except NetmikoAuthenticationException as e:
        error_msg = f"Authentication failed for {device_params['host']}: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
        
    except SSHException as e:
        error_msg = f"SSH connection error to {device_params['host']}: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
        
    except socket.gaierror as e:
        error_msg = f"DNS resolution failed for {device_params['host']}: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
        
    except Exception as e:
        error_msg = f"Unexpected connection error to {device_params['host']}: {str(e)}"
        logger.error(error_msg)
        return None, error_msg

def safe_send_command(connection, command, logger, max_retries=3):
    """
    Safely send a command to the device with retries
    
    Args:
        connection: Netmiko connection object
        command (str): Command to send
        logger (logging.Logger): Logger instance
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        tuple: (output, error_message)
    """
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Sending command (attempt {attempt + 1}): {command}")
            
            # Send command with timeout
            output = connection.send_command(command, expect_string='#', delay_factor=2)
            
            logger.debug(f"Command successful: {command}")
            return output, None
            
        except Exception as e:
            error_msg = f"Command '{command}' failed (attempt {attempt + 1}): {str(e)}"
            logger.warning(error_msg)
            
            if attempt < max_retries - 1:
                logger.info("Retrying command in 2 seconds...")
                time.sleep(2)
            else:
                logger.error(f"Command '{command}' failed after {max_retries} attempts")
                return None, error_msg
    
    return None, f"Command '{command}' failed after {max_retries} attempts"

def safe_send_config_commands(connection, config_commands, logger):
    """
    Safely send configuration commands with rollback capability
    
    Args:
        connection: Netmiko connection object
        config_commands (list): List of configuration commands
        logger (logging.Logger): Logger instance
        
    Returns:
        tuple: (success, error_message)
    """
    
    logger.info(f"Applying {len(config_commands)} configuration commands")
    
    try:
        # Check if device supports configuration mode
        if not connection.check_enable_mode():
            connection.enable()
            logger.debug("Entered enable mode")
        
        # Apply configuration
        output = connection.send_config_set(config_commands)
        logger.info("Configuration commands applied successfully")
        logger.debug(f"Configuration output: {output}")
        
        return True, None
        
    except Exception as e:
        error_msg = f"Configuration failed: {str(e)}"
        logger.error(error_msg)
        
        # Attempt to exit config mode if we're stuck
        try:
            connection.send_command('end')
            logger.debug("Exited configuration mode after error")
        except Exception:
            pass
        
        return False, error_msg

def demonstrate_error_scenarios():
    """
    Demonstrate different error scenarios and how to handle them
    """
    
    logger = setup_logging()
    
    print("="*70)
    print("ERROR HANDLING SCENARIOS DEMONSTRATION")
    print("="*70)
    
    # Scenario 1: Invalid IP address
    print("\n1. Invalid IP Address:")
    print("-" * 30)
    
    invalid_device = {
        'device_type': 'cisco_ios',
        'host': '999.999.999.999',  # Invalid IP
        'username': 'admin',
        'password': 'password'
    }
    
    connection, error = safe_connect_to_device(invalid_device, logger)
    if error:
        print(f"❌ Expected error caught: {error}")
    
    # Scenario 2: Connection timeout (unreachable host)
    print("\n2. Connection Timeout:")
    print("-" * 30)
    
    timeout_device = {
        'device_type': 'cisco_ios',
        'host': '192.168.254.254',  # Likely unreachable
        'username': 'admin',
        'password': 'password',
        'timeout': 5  # Short timeout for demo
    }
    
    connection, error = safe_connect_to_device(timeout_device, logger)
    if error:
        print(f"❌ Expected timeout caught: {error}")
    
    # Scenario 3: Missing required parameters
    print("\n3. Missing Parameters:")
    print("-" * 30)
    
    incomplete_device = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',
        # Missing username and password
    }
    
    connection, error = safe_connect_to_device(incomplete_device, logger)
    if error:
        print(f"❌ Expected validation error: {error}")

def resilient_device_monitoring():
    """
    Demonstrate a resilient monitoring script with error handling
    """
    
    logger = setup_logging()
    
    print("\n" + "="*70)
    print("RESILIENT DEVICE MONITORING EXAMPLE")
    print("="*70)
    
    device = load_device_config()
    
    # Monitoring commands to execute
    monitoring_commands = [
        'show clock',
        'show processes cpu | include CPU',
        'show memory statistics | include Total',
        'show ip interface brief | count',
        'show version | include uptime'
    ]
    
    # Connect with error handling
    connection, connect_error = safe_connect_to_device(device, logger)
    
    if connect_error:
        print(f"❌ Cannot monitor device: {connect_error}")
        return False
    
    print(f"✓ Connected to {device['host']} for monitoring")
    
    # Execute monitoring commands with error handling
    results = {}
    failed_commands = []
    
    for command in monitoring_commands:
        output, cmd_error = safe_send_command(connection, command, logger)
        
        if cmd_error:
            print(f"⚠️  Command failed: {command}")
            failed_commands.append(command)
        else:
            print(f"✓ Command successful: {command}")
            results[command] = output
    
    # Generate monitoring report
    print("\nMonitoring Results:")
    print("-" * 30)
    print(f"Total commands: {len(monitoring_commands)}")
    print(f"Successful: {len(results)}")
    print(f"Failed: {len(failed_commands)}")
    
    if results:
        print("\nSample outputs:")
        for command, output in list(results.items())[:2]:
            print(f"{command}: {output.strip()[:100]}...")
    
    # Cleanup
    try:
        if connection:
            connection.disconnect()
            logger.info("Disconnected successfully")
            print("✓ Disconnected successfully")
        else:
            logger.info("No active connection to disconnect")
    except Exception as e:
        logger.warning(f"Disconnect error: {e}")
    
    return len(failed_commands) == 0

def backup_device_config_with_error_handling():
    """
    Backup device configuration with comprehensive error handling
    """
    
    logger = setup_logging()
    
    print("\n" + "="*70)  
    print("CONFIG BACKUP WITH ERROR HANDLING")
    print("="*70)
    
    device = load_device_config()
    
    try:
        # Connect to device
        connection, error = safe_connect_to_device(device, logger)
        if error:
            print(f"❌ Backup failed - cannot connect: {error}")
            return False
        
        # Get running configuration
        print("Retrieving running configuration...")
        config_output, cmd_error = safe_send_command(connection, 'show running-config', logger)
        if cmd_error or config_output is None:
            failure_reason = cmd_error if cmd_error else "No output received"
            print(f"❌ Failed to retrieve config: {failure_reason}")
            try:
                if connection:
                    connection.disconnect()
                    logger.info("Disconnected after failed config retrieval")
                else:
                    logger.info("No active connection to disconnect after failure")
            except Exception as e:
                logger.warning(f"Disconnect error after failure: {e}")
            return False
        
        # Create backup directory
        backup_dir = 'config_backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if connection is None:
            logger.error("Connection object is None before determining hostname")
            print("❌ Lost device connection before determining hostname")
            return False

        try:
            prompt = connection.find_prompt()
            hostname = prompt.replace('#', '').replace('>', '').strip()
        except Exception as e:
            logger.warning(f"Could not get device prompt, falling back to host: {e}")
            hostname = str(device.get('host', 'device')).strip()

        backup_filename = f"{backup_dir}/{hostname}_{timestamp}.cfg"
        
        # Save configuration to file
        try:
            with open(backup_filename, 'w') as f:
                f.write(config_output)
            
            print(f"✓ Configuration backed up to: {backup_filename}")
            logger.info(f"Config backup saved: {backup_filename}")
            
        except IOError as e:
            error_msg = f"Failed to save backup file: {str(e)}"
            print(f"❌ {error_msg}")
            logger.error(error_msg)
            return False
        
        # Verify backup file
        try:
            with open(backup_filename, 'r') as f:
                backup_content = f.read()
            if len(backup_content) > 100:  # Basic sanity check
                print(f"✓ Backup verified - {len(backup_content)} characters")
            else:
                print("⚠️  Backup file seems too small")
        except Exception as e:
            print(f"⚠️  Could not verify backup: {e}")
        
        # Cleanup
        try:
            if connection:
                connection.disconnect()
                logger.info("Disconnected successfully")
            else:
                logger.info("No active connection to disconnect")
        except Exception as e:
            logger.warning(f"Disconnect error: {e}")
        return True
        
    except Exception as e:
        logger.error(f"Unexpected error during backup: {e}")
        print(f"❌ Backup failed with unexpected error: {e}")
        return False

def main():
    """
    Main function demonstrating comprehensive error handling
    """
    
    print("Module 2 - Error Handling in Network Automation")
    print("Learn to create robust network automation scripts")
    
    logger = setup_logging()
    logger.info("Starting error handling demonstration")
    
    try:
        # Demonstrate error scenarios
        demonstrate_error_scenarios()
        
        # Ask user what to demonstrate
        print("\n" + "="*70)
        print("INTERACTIVE DEMONSTRATIONS")
        print("="*70)
        
        while True:
            print("\nAvailable demonstrations:")
            print("1. Resilient device monitoring")
            print("2. Configuration backup with error handling")
            print("3. Exit")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                success = resilient_device_monitoring()
                if success:
                    print("✓ Monitoring completed successfully")
                else:
                    print("⚠️  Monitoring completed with some errors")
                    
            elif choice == '2':
                success = backup_device_config_with_error_handling()
                if success:
                    print("✓ Backup completed successfully")
                else:
                    print("❌ Backup failed")
                    
            elif choice == '3':
                break
            else:
                print("Invalid choice, please try again")
        
        print("\n" + "="*70)
        print("ERROR HANDLING DEMO COMPLETE!")
        print("="*70)
        print("Key learning points:")
        print("1. Always validate input parameters")
        print("2. Use specific exception types when possible")
        print("3. Implement retry logic for transient errors")
        print("4. Log errors for debugging and monitoring")
        print("5. Provide graceful fallbacks and recovery")
        print("6. Clean up resources (connections) in finally blocks")
        print("7. Give users meaningful error messages")
        print("8. Test error scenarios during development")
        
        logger.info("Error handling demonstration completed")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        logger.info("Script interrupted by user")
    except Exception as e:
        print(f"\nUnexpected script error: {e}")
        logger.error(f"Unexpected script error: {e}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Module 2 - Script 6: Mass Loopback Configuration
Purpose: Configure multiple loopback interfaces using loops and dictionaries

This script demonstrates:
- Using Python data structures (lists and dictionaries)
- Looping through configuration data
- Mass configuration deployment
- Data-driven network configuration
- Verification of bulk changes

Learning Objectives:
- Structure configuration data in Python dictionaries
- Use loops to apply repetitive configurations
- Validate configuration data before deployment
- Verify changes after deployment
- Handle configuration errors gracefully

WARNING: This script MODIFIES device configuration!
Only run on lab devices, never on production equipment!
"""

import json
import os
from netmiko import ConnectHandler

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

def load_loopback_data():
    """
    Load loopback interface data from JSON file
    
    Returns:
        list: List of loopback interface dictionaries
    """
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, '..', '..', 'sample_data', 'devices.json')
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data['loopback_interfaces']
    except FileNotFoundError:
        # Fallback data if file not found
        return [
            {'number': 100, 'ip': '100.100.100.100', 'mask': '255.255.255.255', 'description': 'Management Loopback'},
            {'number': 200, 'ip': '200.200.200.200', 'mask': '255.255.255.255', 'description': 'OSPF Router ID'}, 
            {'number': 300, 'ip': '300.300.300.300', 'mask': '255.255.255.255', 'description': 'BGP Router ID'},
            {'number': 400, 'ip': '10.1.1.1', 'mask': '255.255.255.255', 'description': 'Backup Management'},
            {'number': 500, 'ip': '10.2.2.2', 'mask': '255.255.255.255', 'description': 'Service Loopback'}
        ]

def validate_loopback_data(loopback_interfaces):
    """
    Validate loopback interface data before configuration
    
    Args:
        loopback_interfaces (list): List of interface dictionaries
        
    Returns:
        tuple: (is_valid, error_messages)
    """
    
    print("="*60)
    print("VALIDATING LOOPBACK DATA")
    print("="*60)
    
    errors = []
    required_fields = ['number', 'ip', 'mask', 'description']
    
    for i, interface in enumerate(loopback_interfaces):
        print(f"Validating interface {i+1}: Loopback{interface.get('number', 'UNKNOWN')}")
        
        # Check required fields
        for field in required_fields:
            if field not in interface:
                errors.append(f"Interface {i+1}: Missing required field '{field}'")
            elif not interface[field]:
                errors.append(f"Interface {i+1}: Empty value for field '{field}'")
        
        # Validate loopback number
        if 'number' in interface:
            try:
                num = int(interface['number'])
                if num < 0 or num > 2147483647:
                    errors.append(f"Interface {i+1}: Invalid loopback number {num}")
            except ValueError:
                errors.append(f"Interface {i+1}: Loopback number must be integer")
        
        # Basic IP validation (simplified)
        if 'ip' in interface:
            ip_parts = interface['ip'].split('.')
            if len(ip_parts) != 4:
                errors.append(f"Interface {i+1}: Invalid IP address format")
            else:
                try:
                    for part in ip_parts:
                        octet = int(part)
                        if octet < 0 or octet > 255:
                            errors.append(f"Interface {i+1}: Invalid IP octet {octet}")
                except ValueError:
                    errors.append(f"Interface {i+1}: IP address contains non-numeric values")
    
    if errors:
        print("❌ Validation failed with the following errors:")
        for error in errors:
            print(f"  - {error}")
        return False, errors
    else:
        print("✓ All loopback data validated successfully!")
        return True, []

def configure_single_loopback(connection, interface_data):
    """
    Configure a single loopback interface
    
    Args:
        connection: Netmiko connection object
        interface_data (dict): Interface configuration data
        
    Returns:
        tuple: (success, output)
    """
    
    loopback_number = interface_data['number']
    ip_address = interface_data['ip']
    subnet_mask = interface_data['mask']
    description = interface_data['description']
    
    print(f"\nConfiguring Loopback{loopback_number}...")
    print(f"  IP: {ip_address}/{subnet_mask}")
    print(f"  Description: {description}")
    
    # Build configuration commands
    config_commands = [
        f"interface loopback {loopback_number}",
        f"ip address {ip_address} {subnet_mask}",
        f"description {description}",
        "no shutdown"
    ]
    
    try:
        output = connection.send_config_set(config_commands)
        print(f"✓ Loopback{loopback_number} configured successfully")
        return True, output
        
    except Exception as e:
        print(f"❌ Failed to configure Loopback{loopback_number}: {e}")
        return False, str(e)

def configure_all_loopbacks(connection, loopback_interfaces):
    """
    Configure all loopback interfaces
    
    Args:
        connection: Netmiko connection object
        loopback_interfaces (list): List of interface configurations
        
    Returns:
        dict: Results summary
    """
    
    print("="*60)
    print(f"CONFIGURING {len(loopback_interfaces)} LOOPBACK INTERFACES")
    print("="*60)
    
    results = {
        'successful': [],
        'failed': [],
        'outputs': {}
    }
    
    for i, interface in enumerate(loopback_interfaces, 1):
        print(f"\n[{i}/{len(loopback_interfaces)}] ", end="")
        
        success, output = configure_single_loopback(connection, interface)
        
        loopback_id = f"Loopback{interface['number']}"
        results['outputs'][loopback_id] = output
        
        if success:
            results['successful'].append(loopback_id)
        else:
            results['failed'].append(loopback_id)
    
    return results

def verify_loopback_configuration(connection, loopback_interfaces):
    """
    Verify that all loopback interfaces were configured correctly
    
    Args:
        connection: Netmiko connection object
        loopback_interfaces (list): List of expected interfaces
        
    Returns:
        dict: Verification results
    """
    
    print("\n" + "="*60)
    print("VERIFYING LOOPBACK CONFIGURATION")
    print("="*60)
    
    verification_results = {
        'found': [],
        'missing': [],
        'details': {}
    }
    
    # Get current interface status
    output = connection.send_command('show ip interface brief')
    
    for interface in loopback_interfaces:
        loopback_name = f"Loopback{interface['number']}"
        expected_ip = interface['ip']
        
        print(f"\nVerifying {loopback_name}...")
        
        if loopback_name in output and expected_ip in output:
            print(f"✓ {loopback_name} found with IP {expected_ip}")
            verification_results['found'].append(loopback_name)
            
            # Get detailed interface info
            detail_output = connection.send_command(f'show interface {loopback_name}')
            verification_results['details'][loopback_name] = detail_output
            
        else:
            print(f"❌ {loopback_name} not found or incorrect IP")
            verification_results['missing'].append(loopback_name)
    
    return verification_results

def display_configuration_summary(loopback_interfaces, config_results, verify_results):
    """
    Display a comprehensive summary of configuration results
    
    Args:
        loopback_interfaces (list): Original interface data
        config_results (dict): Configuration results
        verify_results (dict): Verification results
    """
    
    print("\n" + "="*60)
    print("CONFIGURATION SUMMARY")
    print("="*60)
    
    total_interfaces = len(loopback_interfaces)
    successful_configs = len(config_results['successful'])
    failed_configs = len(config_results['failed'])
    verified_interfaces = len(verify_results['found'])
    
    print(f"Total interfaces to configure: {total_interfaces}")
    print(f"Successfully configured: {successful_configs}")
    print(f"Failed to configure: {failed_configs}")
    print(f"Verified as working: {verified_interfaces}")
    
    if config_results['successful']:
        print("\n✓ Successfully configured interfaces:")
        for interface in config_results['successful']:
            print(f"  - {interface}")
    
    if config_results['failed']:
        print("\n❌ Failed to configure interfaces:")
        for interface in config_results['failed']:
            print(f"  - {interface}")
    
    if verify_results['missing']:
        print("\n⚠️  Interfaces not found in verification:")
        for interface in verify_results['missing']:
            print(f"  - {interface}")
    
    # Success rate
    success_rate = (successful_configs / total_interfaces) * 100 if total_interfaces > 0 else 0
    print(f"\nOverall success rate: {success_rate:.1f}%")

def save_configuration_backup(connection):
    """
    Save running configuration to startup configuration
    
    Args:
        connection: Netmiko connection object
        
    Returns:
        bool: Success status
    """
    
    print("\n" + "="*60)
    print("SAVING CONFIGURATION")
    print("="*60)
    
    try:
        print("Saving running-config to startup-config...")
        output = connection.send_command('write memory')
        print(output)
        
        if 'OK' in output or '[OK]' in output:
            print("✓ Configuration saved successfully!")
            return True
        else:
            print("❌ Configuration save may have failed")
            return False
            
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return False

def demo_mass_loopback_config():
    """
    Main demonstration of mass loopback configuration
    """
    
    print("="*60)
    print("MODULE 2 - MASS LOOPBACK CONFIGURATION")
    print("="*60)
    print("This script will configure multiple loopback interfaces")
    print("WARNING: This modifies device configuration!")
    
    # Ask for confirmation
    response = input("\nProceed with loopback configuration? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Configuration cancelled by user")
        return
    
    # Load configuration data
    device = load_device_config()
    loopback_interfaces = load_loopback_data()
    
    print(f"\nDevice: {device['host']}")
    print(f"Loopback interfaces to configure: {len(loopback_interfaces)}")
    
    # Display what will be configured
    print("\nInterfaces to be configured:")
    for interface in loopback_interfaces:
        print(f"  - Loopback{interface['number']}: {interface['ip']} - {interface['description']}")
    
    try:
        # Connect to device
        print(f"\nConnecting to {device['host']}...")
        connection = ConnectHandler(**device)
        print("✓ Connected successfully!")
        
        # Ensure we're in enable mode
        if not connection.check_enable_mode():
            connection.enable()
            print("✓ Entered enable mode")
        
        # Validate data
        is_valid, errors = validate_loopback_data(loopback_interfaces)
        if not is_valid:
            print("Cannot proceed due to validation errors")
            return
        
        # Configure all loopbacks
        config_results = configure_all_loopbacks(connection, loopback_interfaces)
        
        # Verify configuration
        verify_results = verify_loopback_configuration(connection, loopback_interfaces)
        
        # Display summary
        display_configuration_summary(loopback_interfaces, config_results, verify_results)
        
        # Save configuration
        save_configuration_backup(connection)
        
        connection.disconnect()
        print("\n✓ Disconnected successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """
    Main function - entry point
    """
    
    print("Module 2 - Mass Loopback Configuration")
    print("Learn to configure multiple interfaces using loops and data structures")
    
    try:
        demo_mass_loopback_config()
        
        print("\n" + "="*60)
        print("MASS CONFIGURATION DEMO COMPLETE!")
        print("="*60)
        print("Key learning points:")
        print("1. Use Python data structures to organize config data")
        print("2. Validate data before applying configurations")
        print("3. Use loops to apply repetitive configurations")
        print("4. Always verify configuration changes")
        print("5. Handle errors gracefully in bulk operations")
        print("6. Save configuration after successful changes")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
    except Exception as e:
        print(f"\nScript error: {e}")

if __name__ == "__main__":
    main()
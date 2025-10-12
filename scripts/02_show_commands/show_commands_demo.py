#!/usr/bin/env python3
"""
Module 2 - Script 3: Show Commands with Netmiko
Purpose: Execute various show commands and handle output

This script demonstrates:
- Sending multiple show commands
- Handling command output
- Using different output formatting
- Working with command lists
- Viewing raw vs formatted output

Learning Objectives:
- Execute common show commands
- Understand command output formatting
- Use loops to execute multiple commands
- Handle different types of output
- Practice with real network data
"""

import json
import os
from netmiko import ConnectHandler

def load_device_config():
    """
    Load device configuration from JSON file
    
    Returns:
        dict: Device connection parameters
    """
    
    # Path to sample device data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, '..', '..', 'sample_data', 'devices.json')
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Return the first device from the list
        return data['devices'][0]
        
    except FileNotFoundError:
        # Fallback to hardcoded values if file not found
        print("Warning: Could not load devices.json, using default values")
        return {
            'device_type': 'cisco_ios',
            'host': '192.168.1.1',
            'username': 'admin',
            'password': 'cisco123',
            'secret': 'enable123',
            'timeout': 20
        }

def execute_single_command(connection, command):
    """
    Execute a single show command and return output
    
    Args:
        connection: Netmiko connection object
        command (str): Command to execute
        
    Returns:
        str: Command output
    """
    
    print(f"\n{'='*60}")
    print(f"Executing: {command}")
    print('='*60)
    
    try:
        output = connection.send_command(command)
        print(output)
        return output
        
    except Exception as e:
        print(f"Command failed: {e}")
        return None

def execute_command_list(connection, commands):
    """
    Execute a list of commands and store results
    
    Args:
        connection: Netmiko connection object  
        commands (list): List of commands to execute
        
    Returns:
        dict: Dictionary with commands as keys and output as values
    """
    
    results = {}
    
    print(f"\n{'='*60}")
    print(f"EXECUTING {len(commands)} COMMANDS")
    print('='*60)
    
    for i, command in enumerate(commands, 1):
        print(f"\n[{i}/{len(commands)}] {command}")
        print("-" * 50)
        
        try:
            output = connection.send_command(command)
            results[command] = output
            
            # Show first few lines of output
            lines = output.split('\n')
            preview_lines = min(5, len(lines))
            
            for line in lines[:preview_lines]:
                print(line)
                
            if len(lines) > preview_lines:
                print(f"... ({len(lines) - preview_lines} more lines)")
                
        except Exception as e:
            print(f"❌ Failed: {e}")
            results[command] = None
    
    return results

def show_raw_output_analysis(connection, command):
    """
    Analyze raw output format of a command
    
    Args:
        connection: Netmiko connection object
        command (str): Command to analyze
    """
    
    print(f"\n{'='*60}")
    print(f"RAW OUTPUT ANALYSIS: {command}")
    print('='*60)
    
    try:
        output = connection.send_command(command)
        
        print("1. Raw string representation:")
        print("-" * 30)
        print(repr(output))  # Shows \n, \r, etc.
        
        print("\n2. Line count and character count:")
        print("-" * 30)
        lines = output.split('\n')
        print(f"Total lines: {len(lines)}")
        print(f"Total characters: {len(output)}")
        print(f"Non-empty lines: {len([line for line in lines if line.strip()])}")
        
        print("\n3. First 5 lines:")
        print("-" * 30)
        for i, line in enumerate(lines[:5]):
            print(f"Line {i+1}: '{line}'")
            
        print("\n4. Last 5 lines:")
        print("-" * 30)
        for i, line in enumerate(lines[-5:], len(lines)-4):
            print(f"Line {i}: '{line}'")
            
    except Exception as e:
        print(f"Analysis failed: {e}")

def demo_show_commands():
    """
    Demonstrate various show commands
    """
    
    print("="*60)
    print("MODULE 2 - SHOW COMMANDS DEMONSTRATION")
    print("="*60)
    
    # Load device configuration
    device = load_device_config()
    print(f"Connecting to: {device['host']} ({device.get('name', 'Device')})")
    
    try:
        # Establish connection
        connection = ConnectHandler(**device)
        print("✓ Connected successfully!")
        
        # 1. Basic device information commands
        basic_commands = [
            'show clock',
            'show version',
            'show users',
        ]
        
        print("\n" + "="*60)
        print("1. BASIC DEVICE INFORMATION")
        print("="*60)
        
        for command in basic_commands:
            execute_single_command(connection, command)
        
        # 2. Interface commands
        interface_commands = [
            'show ip interface brief',
            'show interface status',
            'show interface description',
        ]
        
        print("\n" + "="*60)
        print("2. INTERFACE INFORMATION")
        print("="*60)
        
        interface_results = execute_command_list(connection, interface_commands)
        
        # 3. Routing information
        routing_commands = [
            'show ip route summary',
            'show ip protocols',
        ]
        
        print("\n" + "="*60)
        print("3. ROUTING INFORMATION")
        print("="*60)
        
        routing_results = execute_command_list(connection, routing_commands)
        
        # 4. Raw output analysis
        print("\n" + "="*60)
        print("4. RAW OUTPUT ANALYSIS")
        print("="*60)
        
        show_raw_output_analysis(connection, 'show ip interface brief')
        
        # 5. Save results to file
        print("\n" + "="*60)
        print("5. SAVING RESULTS")
        print("="*60)
        
        save_results_to_file(interface_results, routing_results)
        
        # Cleanup
        connection.disconnect()
        print("\n✓ Disconnected successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure device parameters are correct and device is reachable")

def save_results_to_file(interface_results, routing_results):
    """
    Save command results to files for later analysis
    
    Args:
        interface_results (dict): Interface command results
        routing_results (dict): Routing command results
    """
    
    # Create output directory
    output_dir = "command_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save interface results
    interface_file = os.path.join(output_dir, "interface_commands.txt")
    with open(interface_file, 'w') as f:
        f.write("INTERFACE COMMAND OUTPUTS\n")
        f.write("="*50 + "\n\n")
        
        for command, output in interface_results.items():
            if output:
                f.write(f"Command: {command}\n")
                f.write("-" * 40 + "\n")
                f.write(output)
                f.write("\n\n" + "="*50 + "\n\n")
    
    print(f"✓ Interface results saved to: {interface_file}")
    
    # Save routing results  
    routing_file = os.path.join(output_dir, "routing_commands.txt")
    with open(routing_file, 'w') as f:
        f.write("ROUTING COMMAND OUTPUTS\n")
        f.write("="*50 + "\n\n")
        
        for command, output in routing_results.items():
            if output:
                f.write(f"Command: {command}\n") 
                f.write("-" * 40 + "\n")
                f.write(output)
                f.write("\n\n" + "="*50 + "\n\n")
    
    print(f"✓ Routing results saved to: {routing_file}")

def main():
    """
    Main function - entry point
    """
    
    print("Module 2 - Show Commands with Netmiko")
    print("This script demonstrates executing show commands")
    
    try:
        demo_show_commands()
        
        print("\n" + "="*60)
        print("SHOW COMMANDS DEMO COMPLETE!")
        print("="*60)
        print("Key learning points:")
        print("1. Show commands are read-only and safe to execute")
        print("2. Different commands return different output formats")
        print("3. Output can be stored and analyzed")
        print("4. Raw output contains special characters (\\n, \\r)")
        print("5. Command results can be saved for later processing")
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
    except Exception as e:
        print(f"\nScript error: {e}")

if __name__ == "__main__":
    main()
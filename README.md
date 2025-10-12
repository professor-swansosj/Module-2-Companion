# Software Defined Networking - Module 2 Companion

## Course: Network Automation with Python

## MODULE 2: Executing Commands with Netmiko

Welcome to the Module 2 Companion Repository! This repository provides hands-on practice exercises and examples to accompany the instructional video for Module 2 of the Software Defined Networking course.

### Prerequisites

- Linux+ certification or equivalent knowledge
- Introduction to Python (completed)
- Cisco CCNA 1, 2, and 3 (completed)
- This is your second Python course

### Learning Objectives

By the end of this module, you will be able to:

- Use Python's Netmiko library to connect to Cisco devices
- Execute show and configuration commands remotely
- Parse command output using various techniques
- Implement error handling and best practices
- Create formatted reports using f-strings
- Structure code using functions and main() entry points

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
2. [Introduction to Netmiko](#introduction-to-netmiko)
3. [Using dir(), help(), and inspect](#using-dir-help-and-inspect)
4. [Creating a Basic Connection Script](#creating-a-basic-connection-script)
5. [Executing Show Commands](#executing-show-commands)
6. [Executing Configuration Commands](#executing-configuration-commands)
7. [Viewing Raw Output](#viewing-raw-output)
8. [Pretty Printing Output](#pretty-printing-output)
9. [Configuring Multiple Loopback Interfaces](#configuring-multiple-loopback-interfaces)
10. [Parsing Raw Output](#parsing-raw-output)
11. [Using NTC-Templates](#using-ntc-templates)
12. [Introduction to F-Strings](#introduction-to-f-strings)
13. [Formatting Multiple Device Commands](#formatting-multiple-device-commands)
14. [Implementing Error Handling](#implementing-error-handling)
15. [Creating Functions](#creating-functions)
16. [Main Function Entry Point](#main-function-entry-point)
17. [Complete Examples](#complete-examples)

---

## Setup and Installation

### Required Python Packages

```bash
pip install -r requirements.txt
```

### Directory Structure

```bash
Module-2-Companion/
├── README.md
├── requirements.txt
├── scripts/
│   ├── 01_basic_connection/
│   ├── 02_show_commands/
│   ├── 03_config_commands/
│   ├── 04_loopback_config/
│   ├── 05_parsing/
│   ├── 06_f_strings/
│   ├── 07_error_handling/
│   ├── 08_functions/
│   └── 09_complete_examples/
├── sample_data/
│   ├── devices.json
│   ├── device_configs.yaml
│   ├── interfaces.csv
│   └── commands.txt
└── templates/
    └── cisco_ios_show_version.textfsm
```

---

## Introduction to Netmiko

Netmiko is a multi-vendor Python library that simplifies SSH connections to network devices. It's built on top of Paramiko and provides a more user-friendly interface for network automation tasks.

**Key Features:**

- Support for multiple device types (Cisco, Juniper, Arista, etc.)
- Automatic handling of device prompts
- Built-in support for enable mode
- Configuration mode handling
- File transfer capabilities

### Common Device Types

- `cisco_ios` - Cisco IOS devices
- `cisco_xe` - Cisco IOS-XE devices  
- `cisco_nxos` - Cisco Nexus devices
- `cisco_asa` - Cisco ASA firewalls

---

## Using dir(), help(), and inspect

Before diving into Netmiko, let's explore Python's built-in tools for understanding objects and their methods.

### Example: Exploring Netmiko Objects

```python
from netmiko import ConnectHandler
import inspect

# Use dir() to see available methods
print("Available methods:", dir(ConnectHandler))

# Use help() for detailed documentation  
help(ConnectHandler.send_command)

# Use inspect to get source code and signatures
print("Method signature:", inspect.signature(ConnectHandler.send_command))
```

**Practice Exercise:** Run the script in `scripts/01_basic_connection/explore_netmiko.py`

---

## Creating a Basic Connection Script

Your first script will establish a connection to a Cisco device and verify connectivity.

### Device Connection Dictionary

```python
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'secret': 'enable_password',  # Optional: for enable mode
    'timeout': 20,
    'session_log': 'output.txt'  # Optional: log session
}
```

### Basic Connection Example

```python
from netmiko import ConnectHandler

try:
    # Establish connection
    connection = ConnectHandler(**device)
    
    # Send a simple command to verify connectivity
    output = connection.send_command('show clock')
    print(output)
    
    # Always disconnect
    connection.disconnect()
    
except Exception as e:
    print(f"Connection failed: {e}")
```

**Practice Exercise:** Complete the script in `scripts/01_basic_connection/basic_connect.py`

---

## Executing Show Commands

Show commands are read-only and provide information about the device state.

### Common Show Commands

- `show version` - Device information
- `show ip interface brief` - Interface status  
- `show running-config` - Current configuration
- `show ip route` - Routing table

### Example: Multiple Show Commands

```python
commands = [
    'show version',
    'show ip interface brief', 
    'show ip route'
]

for command in commands:
    print(f"\n{'='*50}")
    print(f"Command: {command}")
    print('='*50)
    output = connection.send_command(command)
    print(output)
```

**Practice Exercise:** Run the scripts in `scripts/02_show_commands/`

---

## Executing Configuration Commands

Configuration commands modify the device configuration and require special handling.

### Single Configuration Command

```python
# Enter configuration mode and send command
output = connection.send_config_set(['interface loopback 1', 'ip address 1.1.1.1 255.255.255.255'])
print(output)
```

### Multiple Configuration Commands

```python
config_commands = [
    'interface loopback 10',
    'ip address 10.10.10.10 255.255.255.255',
    'description Created by Python Script',
    'no shutdown'
]

output = connection.send_config_set(config_commands)
```

**Practice Exercise:** Complete the scripts in `scripts/03_config_commands/`

---

## Viewing Raw Output

Understanding the raw output format is crucial for parsing and processing command results.

### Raw Output Example

```python
output = connection.send_command('show ip interface brief')
print("Raw output:")
print(repr(output))  # Shows \n, \r characters
print("\nFormatted output:")
print(output)
```

**Practice Exercise:** Examine raw output in `scripts/04_raw_output/`

---

## Pretty Printing Output

Use Python's `pprint` module to format complex data structures.

```python
import pprint

# For dictionaries and lists
data = {'interfaces': ['GigE0/0', 'GigE0/1'], 'vlans': [10, 20, 30]}
pprint.pprint(data)

# For command output with custom formatting
def pretty_print_output(command, output):
    print(f"\n{'='*60}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    print(output)
    print(f"{'='*60}\n")
```

**Practice Exercise:** Format output using `scripts/05_pretty_print/`

---

## Configuring Multiple Loopback Interfaces

Use Python data structures and loops to configure multiple interfaces efficiently.

### Interface Data Structure

```python
loopback_interfaces = [
    {'number': 100, 'ip': '100.100.100.100', 'mask': '255.255.255.255', 'description': 'Loopback 100'},
    {'number': 200, 'ip': '200.200.200.200', 'mask': '255.255.255.255', 'description': 'Loopback 200'},
    {'number': 300, 'ip': '300.300.300.300', 'mask': '255.255.255.255', 'description': 'Loopback 300'}
]
```

### Configuration Loop

```python
for interface in loopback_interfaces:
    config_commands = [
        f"interface loopback {interface['number']}",
        f"ip address {interface['ip']} {interface['mask']}",
        f"description {interface['description']}",
        "no shutdown"
    ]
    
    output = connection.send_config_set(config_commands)
    print(f"Configured Loopback {interface['number']}")
```

**Practice Exercise:** Complete `scripts/06_loopback_config/mass_loopback_config.py`

---

## Parsing Raw Output

Learn to extract specific information from command output using string methods and regular expressions.

### String Methods

```python
# Split output into lines
lines = output.split('\n')

# Find lines containing specific text
interface_lines = [line for line in lines if 'GigabitEthernet' in line]

# Extract specific values
for line in interface_lines:
    parts = line.split()
    interface = parts[0]
    ip_address = parts[1]
    print(f"Interface: {interface}, IP: {ip_address}")
```

### Regular Expressions

```python
import re

# Extract IP addresses
ip_pattern = r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b'
ip_addresses = re.findall(ip_pattern, output)
```

**Practice Exercise:** Parse output in `scripts/07_parsing/`

---

## Using NTC-Templates

NTC-Templates provide structured parsing for common network commands.

### Installation and Usage

```python
from netmiko import ConnectHandler
from ntc_templates.parse import parse_output

# Get command output
output = connection.send_command('show version')

# Parse using NTC template
parsed_output = parse_output(
    platform='cisco_ios',
    command='show version', 
    data=output
)

# Access structured data
print(f"Hostname: {parsed_output[0]['hostname']}")
print(f"Version: {parsed_output[0]['version']}")
```

**Practice Exercise:** Use templates in `scripts/08_ntc_templates/`

---

## Introduction to F-Strings

F-strings provide a clean way to format strings with variables.

### Basic F-String Usage

```python
hostname = "Router1"
uptime = "5 days"
version = "15.1(4)M"

# Old way
print("Device %s has been up for %s running version %s" % (hostname, uptime, version))

# F-string way
print(f"Device {hostname} has been up for {uptime} running version {version}")
```

### Advanced F-String Formatting

```python
# Number formatting
cpu_usage = 23.456789
print(f"CPU Usage: {cpu_usage:.2f}%")

# Alignment and width
for i in range(3):
    print(f"Interface GigE0/{i:2d} - Status: {'UP':>10s}")
```

**Practice Exercise:** Learn f-strings in `scripts/09_f_strings/`

---

## Formatting Multiple Device Commands

Combine Netmiko, parsing, and f-strings to create formatted reports.

### Device Report Example

```python
def generate_device_report(connection, hostname):
    # Gather information
    version_output = connection.send_command('show version')
    interface_output = connection.send_command('show ip interface brief')
    
    # Parse data (simplified)
    uptime = extract_uptime(version_output)
    interface_count = len([line for line in interface_output.split('\n') if 'up' in line.lower()])
    
    # Create formatted report
    report = f"""
    {'='*50}
    Device Report: {hostname}
    {'='*50}
    Uptime: {uptime}
    Active Interfaces: {interface_count}
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    {'='*50}
    """
    
    return report
```

**Practice Exercise:** Create reports in `scripts/10_reporting/`

---

## Implementing Error Handling

Robust scripts require proper error handling for network automation.

### Connection Error Handling

```python
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def safe_connect(device_params):
    try:
        connection = ConnectHandler(**device_params)
        return connection, None
    except NetmikoTimeoutException:
        return None, "Connection timed out"
    except NetmikoAuthenticationException:
        return None, "Authentication failed"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
```

### Command Error Handling

```python
def safe_send_command(connection, command):
    try:
        output = connection.send_command(command, expect_string='#')
        return output, None
    except Exception as e:
        return None, f"Command failed: {str(e)}"
```

**Practice Exercise:** Add error handling in `scripts/11_error_handling/`

---

## Creating Functions

Organize code into reusable functions for better maintainability.

### Function Examples

```python
def connect_to_device(device_params):
    """Establish connection to network device"""
    return ConnectHandler(**device_params)

def get_device_info(connection):
    """Gather basic device information"""
    commands = ['show version', 'show ip interface brief']
    results = {}
    
    for command in commands:
        results[command] = connection.send_command(command)
    
    return results

def configure_loopback(connection, interface_data):
    """Configure a loopback interface"""
    config_commands = [
        f"interface loopback {interface_data['number']}",
        f"ip address {interface_data['ip']} {interface_data['mask']}",
        f"description {interface_data['description']}"
    ]
    
    return connection.send_config_set(config_commands)
```

**Practice Exercise:** Refactor code into functions in `scripts/12_functions/`

---

## Main Function Entry Point

Use a main() function as the entry point for your scripts.

### Main Function Pattern

```python
def main():
    """Main function - entry point of the script"""
    # Device parameters
    device = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1', 
        'username': 'admin',
        'password': 'password'
    }
    
    # Connect to device
    print("Connecting to device...")
    connection = connect_to_device(device)
    
    # Perform operations
    try:
        device_info = get_device_info(connection)
        print_device_report(device_info)
    
    finally:
        connection.disconnect()
        print("Disconnected from device")

if __name__ == "__main__":
    main()
```

**Practice Exercise:** Structure scripts with main() in `scripts/13_main_function/`

---

## Complete Examples

The `scripts/14_complete_examples/` directory contains full-featured scripts that demonstrate:

1. **Device Inventory Script** - Connects to multiple devices and generates inventory reports
2. **Configuration Backup Script** - Backs up device configurations with timestamps  
3. **Interface Monitoring Script** - Monitors interface status and generates alerts
4. **Bulk Configuration Script** - Applies configuration changes to multiple devices

---

## Additional Resources

- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [NTC-Templates Repository](https://github.com/networktocode/ntc-templates)  
- [Python Regular Expression Guide](https://docs.python.org/3/library/re.html)
- [F-String Documentation](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)

---

## Troubleshooting

### Common Issues

1. **Connection Timeouts** - Check network connectivity and device IP
2. **Authentication Failures** - Verify username/password and enable secret
3. **Command Failures** - Ensure commands are valid for the device type
4. **Parsing Errors** - Check output format and adjust parsing logic

### Debug Tips

- Use `session_log` parameter to capture all interactions
- Print raw output to understand format
- Test commands manually on device first
- Use try/except blocks for error handling

---

## Repository Status

✅ **Complete Implementation**

This Module 2 companion repository is fully implemented with:

### Completed Scripts (10 Categories)

1. **Basic Connection** - Device connectivity and Netmiko exploration
2. **Show Commands** - Command execution and output formatting  
3. **Configuration Commands** - Safe configuration practices
4. **Loopback Configuration** - Bulk interface configuration
5. **Output Parsing** - Raw parsing and NTC-Templates
6. **F-String Formatting** - Professional output formatting
7. **Error Handling** - Robust error management
8. **Functions** - Modular code organization
9. **Main Patterns** - Professional script structure
10. **Complete Examples** - Full system integration

### Educational Resources

- ✅ 15+ fully functional Python scripts
- ✅ Comprehensive sample data files
- ✅ Detailed inline documentation
- ✅ Progressive learning structure
- ✅ Real-world examples and patterns
- ✅ Best practices integration

### Learning Path

Run `python module_2_summary.py` for a complete overview of all concepts, scripts, and next steps in your network automation journey.

---

**Note:** Remember to follow along with the instructional video and practice each section before moving to the next. The hands-on practice is essential for mastering network automation with Python!

## Module 2 - Network Automation Companion Activities - Complete Implementation

# Software Defined Networking - Module 2 Companion

## Course: Network Automation with Python

## MODULE 2: Executing Commands with Netmiko

Welcome to Module 2! This companion repository provides practice exercises for network automation with Python. You'll learn to connect to network devices and automate basic tasks.

### Prerequisites

- Module 1: Python fundamentals (functions, objects, error handling, file I/O, JSON, YAML, CSV)
- Basic networking knowledge (CCNA level)
- Python development environment

### Learning Objectives

By the end of this module, you will be able to:

- Set up Python virtual environments for network projects
- Connect to network devices using Netmiko
- Execute show and configuration commands
- Handle raw output and format results
- Parse structured data from network commands
- Create basic network automation scripts

## Table of Contents

1. [Virtual Environments and Requirements](#virtual-environments-and-requirements)
2. [Introduction to Netmiko](#introduction-to-netmiko)
3. [Using help(), dir(), and inspect()](#using-help-dir-and-inspect)
4. [Basic Connection with getpass](#basic-connection-with-getpass)
5. [Show Commands and Raw Output](#show-commands-and-raw-output)
6. [Pretty Printing Output](#pretty-printing-output)
7. [Configuration Commands](#configuration-commands)
8. [Working with Multiple Devices](#working-with-multiple-devices)
9. [Parsing with TextFSM and NTC-Templates](#parsing-with-textfsm-and-ntc-templates)
10. [F-Strings and Basic Reports](#f-strings-and-basic-reports)

---

## Virtual Environments and Requirements

Virtual environments keep your project dependencies separate from your system Python.

### Setup Steps

```bash
# Create virtual environment
python -m venv netmiko-env

# Activate it
# Windows:
netmiko-env\Scripts\activate
# Linux/Mac:
```

**Key packages:**
- `netmiko` - SSH to network devices  
- `ntc-templates` - Parse command output
- `PyYAML` - Work with YAML files

**Practice:** Set up your environment and verify netmiko imports successfully.

---

## Introduction to Netmiko

Netmiko is a Python library that simplifies SSH connections to network devices.

### Basic Import and Connection

```python
from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'your_username',
    'password': 'your_password'
}

connection = ConnectHandler(**device)
```

**Practice:** Import netmiko and create a device dictionary for your lab device.

---

## Using help(), dir(), and inspect()

Before diving deeper into netmiko, learn to explore Python objects yourself.

### Essential Exploration Tools

```python
import netmiko
from netmiko import ConnectHandler

# See all available methods
print(dir(ConnectHandler))

# Get detailed help
help(ConnectHandler.send_command)

# Find methods with 'send' in the name
methods = [m for m in dir(ConnectHandler) if 'send' in m]
print(methods)
```

**Practice:** Use `help()` to explore `ConnectHandler.send_command()` and find what exceptions it might raise.

---

## Basic Connection with getpass

Never hardcode passwords! Use `getpass` for secure credential input.

### Secure Connection Example

```python
import getpass
from netmiko import ConnectHandler

# Get credentials securely
host = input("Device IP: ")
username = input("Username: ")
password = getpass.getpass("Password: ")

device = {
    'device_type': 'cisco_ios',
    'host': host,
    'username': username,
    'password': password
}

connection = ConnectHandler(**device)
print("Connected!")
connection.disconnect()
```

**Practice:** Create a connection script using getpass. Test it with your lab device.

---

## Show Commands and Raw Output

Let's see what raw output looks like and why we need to format it.

### Your First Commands

```python
# After connecting...
output = connection.send_command('show version')
print(output)  # This is raw output - messy!

# Try these too
print(connection.send_command('show ip interface brief'))
```

Notice how the raw output is hard to read? That's why we need formatting tools.

**Practice:** Run several show commands and observe the raw output format.

---

## Pretty Printing Output

Now let's make that output readable!

### Using pprint

```python
from pprint import pprint

# For better formatting
output = connection.send_command('show version')
print("="*50)
print("FORMATTED OUTPUT")
print("="*50)
print(output)
```

**Practice:** Format the output of multiple show commands for better readability.

---

## Configuration Commands

Configuration commands modify device settings. Handle with care!

### Basic Config Example

```python
# Single command
config_commands = ['interface loopback 100', 'ip address 100.100.100.100 255.255.255.255']
output = connection.send_config_set(config_commands)
print(output)
```

**Practice:** Configure a loopback interface on your lab device.

---

## Working with Multiple Devices

Scale your automation by working with device lists.

### Multiple Device Example

```python
devices = [
    {'host': '192.168.1.1', 'username': 'admin', 'password': 'pass1'},
    {'host': '192.168.1.2', 'username': 'admin', 'password': 'pass2'}
]

for device in devices:
    device['device_type'] = 'cisco_ios'
    conn = ConnectHandler(**device)
    output = conn.send_command('show version')
    print(f"Device {device['host']}: {output[:50]}...")
    conn.disconnect()
```

**Practice:** Create a device list and gather version info from each.

---

## Parsing with TextFSM and NTC-Templates

Raw text is hard to work with. Let's structure it!

### Why Parse Output?

Look at your raw `show version` output - it's just text. But what if you could get structured data instead?

### Using NTC-Templates

```python
from ntc_templates.parse import parse_output

# Get structured data instead of raw text
output = connection.send_command('show version')
parsed = parse_output(platform='cisco_ios', command='show version', data=output)

# Now you have a list of dictionaries!
print(parsed[0]['hostname'])
print(parsed[0]['version'])
```

**Practice:** Parse `show ip interface brief` and extract just the interface names.

---

## F-Strings and Basic Reports

Create professional output and save results to files.

### Formatting with F-Strings

```python
hostname = parsed[0]['hostname']
version = parsed[0]['version']
uptime = parsed[0]['uptime']

report = f"""
Device Report
=============
Hostname: {hostname}
Version:  {version}
Uptime:   {uptime}
"""

print(report)

# Save to file
with open(f'{hostname}_report.txt', 'w') as f:
    f.write(report)
```

**Practice:** Create a device inventory report and save it to a file.

---

## Next Steps

You've learned the basics! Now practice by:

1. Building a device inventory script
2. Creating configuration backup automation  
3. Monitoring interface status across multiple devices

**Remember:** Start simple, then add complexity. Focus on one concept at a time.

---

## Practice Files

Use the scripts in the `scripts/` directory to practice each concept:

- `01_basic_connection/` - Connection basics
- `02_show_commands/` - Command execution  
- `03_config_commands/` - Configuration tasks
- `04_parsing/` - TextFSM and parsing
- `05_reports/` - F-strings and file output

**Happy automating!** 🚀

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

## Handling Credentials Securely

**NEVER** hardcode passwords in your scripts! Learn to handle credentials securely using environment variables and `getpass`.

### Why Secure Credential Handling Matters

- **Security**: Prevents passwords from being stored in source code
- **Version Control**: Avoids accidentally committing credentials to Git
- **Flexibility**: Different users can use different credentials
- **Compliance**: Meets security best practices and organizational policies

### Method 1: Using `getpass` (Recommended for Course)

The `getpass` module prompts for passwords without displaying them on screen.

```python
import getpass
from netmiko import ConnectHandler

def get_device_credentials():
    """Securely collect device credentials from user"""
    host = input("Device IP Address: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")  # Hidden input
    
    # Optional: Enable password
    enable_secret = getpass.getpass("Enable Secret (press Enter if none): ")
    if not enable_secret:
        enable_secret = None
    
    return {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
        'timeout': 20
    }

# Example usage
device_params = get_device_credentials()
print(f"Connecting to {device_params['host']} as {device_params['username']}...")

try:
    connection = ConnectHandler(**device_params)
    print("✅ Connection successful!")
    
    # Your automation code here
    output = connection.send_command('show clock')
    print(output)
    
    connection.disconnect()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

### Method 2: Environment Variables

Store credentials in environment variables for automated scripts.

#### Setting Environment Variables

**Windows (PowerShell):**
```powershell
# Set for current session
$env:DEVICE_HOST = "192.168.1.1"
$env:DEVICE_USERNAME = "admin"
$env:DEVICE_PASSWORD = "yourpassword"

# Set permanently (requires restart)
[Environment]::SetEnvironmentVariable("DEVICE_HOST", "192.168.1.1", "User")
```

**Linux/macOS:**
```bash
# Set for current session
export DEVICE_HOST="192.168.1.1"
export DEVICE_USERNAME="admin"
export DEVICE_PASSWORD="yourpassword"

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export DEVICE_HOST="192.168.1.1"' >> ~/.bashrc
```

#### Using Environment Variables in Python

```python
import os
from netmiko import ConnectHandler

def get_device_from_env():
    """Get device credentials from environment variables"""
    return {
        'device_type': 'cisco_ios',
        'host': os.getenv('DEVICE_HOST'),
        'username': os.getenv('DEVICE_USERNAME'),
        'password': os.getenv('DEVICE_PASSWORD'),
        'secret': os.getenv('DEVICE_ENABLE_SECRET'),  # Optional
        'timeout': 20
    }

# Validate required environment variables
device = get_device_from_env()
required_vars = ['host', 'username', 'password']

missing_vars = [var for var in required_vars if not device.get(var)]
if missing_vars:
    print(f"❌ Missing environment variables: {missing_vars}")
    exit(1)

print(f"Connecting to {device['host']} as {device['username']}...")
```

### Method 3: Hybrid Approach (Best of Both)

Combine environment variables with getpass for maximum flexibility.

```python
import os
import getpass
from netmiko import ConnectHandler

def get_secure_credentials():
    """Get credentials from environment or prompt user"""
    
    # Try environment variables first
    host = os.getenv('DEVICE_HOST') or input("Device IP Address: ")
    username = os.getenv('DEVICE_USERNAME') or input("Username: ")
    
    # Always prompt for password (most secure)
    password = getpass.getpass("Password: ")
    
    # Optional enable secret
    enable_secret = os.getenv('DEVICE_ENABLE_SECRET')
    if not enable_secret:
        enable_secret = getpass.getpass("Enable Secret (press Enter if none): ")
        if not enable_secret:
            enable_secret = None
    
    return {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
        'timeout': 20
    }

# Usage
device = get_secure_credentials()
print(f"Connecting to {device['host']}...")
```

### Best Practices for Credential Security

1. **Never hardcode passwords** in scripts
2. **Use getpass for interactive scripts** (recommended for course exercises)
3. **Use environment variables for automation** (CI/CD, scheduled scripts)
4. **Always prompt for passwords** when possible
5. **Consider using .env files** with python-dotenv for development
6. **Use secret management tools** for production (HashiCorp Vault, Azure Key Vault)

### Common getpass Patterns

```python
import getpass

# Basic password prompt
password = getpass.getpass()

# Custom prompt
password = getpass.getpass("Enter device password: ")

# Handle KeyboardInterrupt (Ctrl+C)
try:
    password = getpass.getpass("Password: ")
except KeyboardInterrupt:
    print("\n❌ Operation cancelled by user")
    exit(1)

# Confirm password (for setup scripts)
while True:
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password == confirm:
        break
    print("❌ Passwords don't match. Try again.")
```

**Practice Exercise:** Modify your connection scripts to use `getpass` instead of hardcoded passwords.

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

Robust scripts require proper error handling for network automation. Before we implement error handling, let's learn how to explore Python objects and discover what exceptions might occur.

### Exploring Objects with Built-in Tools

Python provides three powerful built-in functions to explore objects and understand their capabilities:

#### Using `help()`

Provides detailed documentation about an object, including methods, parameters, and usage examples.

```python
from netmiko import ConnectHandler

# Get comprehensive help about ConnectHandler
help(ConnectHandler)

# Get help for a specific method
help(ConnectHandler.send_command)
```

#### Using `dir()`

Returns a list of all attributes and methods available on an object.

```python
# See all available methods and attributes
print(dir(ConnectHandler))

# Filter for methods that contain 'send'
methods = [method for method in dir(ConnectHandler) if 'send' in method]
print("Send methods:", methods)
```

#### Using `inspect`

Provides detailed information about objects, including source code and method signatures.

```python
import inspect

# Get the method signature
signature = inspect.signature(ConnectHandler.send_command)
print("Method signature:", signature)

# Get source code (if available)
try:
    source = inspect.getsource(ConnectHandler.send_command)
    print("Source code:", source)
except:
    print("Source code not available")
```

### Discovering Netmiko Exceptions

Let's use these tools to discover what exceptions Netmiko might raise:

```python
from netmiko import exceptions

# Explore available exceptions
print("Available Netmiko exceptions:")
for name in dir(exceptions):
    if not name.startswith('_'):  # Skip private attributes
        exception_class = getattr(exceptions, name)
        if isinstance(exception_class, type) and issubclass(exception_class, Exception):
            print(f"- {name}")

# Get help on a specific exception
help(exceptions.NetmikoTimeoutException)
```

**Key Netmiko Exceptions to Handle:**

- `NetmikoTimeoutException` - Connection or command timeouts
- `NetmikoAuthenticationException` - Login failures
- `SSHException` - SSH connection problems
- `ValueError` - Invalid parameters

### Connection Error Handling

```python
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def safe_connect(device_params):
    """Safely connect to a device with comprehensive error handling"""
    try:
        print(f"Attempting to connect to {device_params.get('host', 'unknown host')}...")
        connection = ConnectHandler(**device_params)
        print("✅ Connection successful!")
        return connection, None
        
    except NetmikoTimeoutException as e:
        error_msg = f"❌ Connection timed out: {str(e)}"
        return None, error_msg

# Example usage
device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'password'
}

connection, error = safe_connect(device)
if connection:
    # Continue with your automation
    pass
else:
    print(f"Failed to connect: {error}")
```

### Command Error Handling

```python
def safe_send_command(connection, command, **kwargs):
    """Safely execute a command with error handling"""
    try:
        print(f"Executing command: {command}")
        output = connection.send_command(command, **kwargs)
        return output, None
        
    except Exception as e:
        error_msg = f"Command '{command}' failed: {str(e)}"
        return None, error_msg

# Example usage
if connection:
    output, error = safe_send_command(connection, 'show version')
    if output:
        print("Command output:", output[:100] + "...")  # Show first 100 chars
    else:
        print(f"Command failed: {error}")
```

### Practice Exercise: Explore and Handle

**Your Task:** Use `help()`, `dir()`, and `inspect` to explore the `send_config_set()` method, then create error handling for it.

```python
# 1. Explore the method
help(ConnectHandler.send_config_set)
print(dir(ConnectHandler))
print(inspect.signature(ConnectHandler.send_config_set))

# 2. Create your own safe_send_config_set() function
# Use the patterns above as a guide!
```

**Practice Exercise:** Complete the error handling exercises in `scripts/07_error_handling/`

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

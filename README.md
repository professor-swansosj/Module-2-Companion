# Module 2 Companion - Network Automation with Netmiko

> **Practice Network Automation!** This companion repository provides hands-on exercises to master SSH connections, command execution, and output processing with network devices.

## Course: Network Automation with Python

### MODULE 2: Executing Commands with Netmiko

This companion supports Module 2 of the FSCJ Network Automation course. You'll build practical skills connecting to network devices, executing commands, and processing output - the foundation of network automation.

## Prerequisites

- **Module 1 Complete**: Python fundamentals (functions, objects, error handling, file I/O, JSON, YAML, CSV)
- **Networking Knowledge**: CCNA-level understanding of routers, switches, and CLI commands
- **Lab Access**: SSH-enabled Cisco device (physical lab or DevNet Sandbox)
- **Python Development Environment**: Python 3.7+ with virtual environment support

## Quick Setup

```bash
# Clone and enter directory
git clone <your-repo-url>
cd Module-2-Companion

# Create virtual environment
python -m venv netmiko-env

# Activate virtual environment
# Windows:
netmiko-env\Scripts\activate
# macOS/Linux:
source netmiko-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test installation
python -c "import netmiko; print('Netmiko ready!')"
```

## Learning Objectives

By the end of this module, you will be able to:

- Set up Python virtual environments for network projects
- Connect to network devices using Netmiko
- Execute show and configuration commands
- Handle raw output and format results
- Parse structured data from network commands
- Create basic network automation scripts

## Table of Contents

1. [Module Structure](#module-structure)
2. [Virtual Environments and Requirements](#virtual-environments-and-requirements)
3. [Introduction to Netmiko](#introduction-to-netmiko)
4. [Using help(), dir(), and inspect()](#using-help-dir-and-inspect)
5. [Basic Connection with getpass](#basic-connection-with-getpass)
6. [Show Commands and Raw Output](#show-commands-and-raw-output)
7. [Pretty Printing Output](#pretty-printing-output)
8. [Configuration Commands](#configuration-commands)
9. [Working with Multiple Devices](#working-with-multiple-devices)
10. [Parsing with TextFSM and NTC-Templates](#parsing-with-textfsm-and-ntc-templates)
11. [F-Strings and Basic Reports](#f-strings-and-basic-reports)

## Estimated Time

**Total: 8-12 hours** across one week

- Initial setup and exploration: 2 hours
- Connection and command practice: 3-4 hours  
- Parsing and formatting: 2-3 hours
- Advanced techniques and projects: 3-4 hours

## Module Structure

Work through these topics sequentially. Each builds on the previous:

### [01_exploration](./01_exploration/) - Object Discovery (1 hour)

**Why this matters:** Before using any library, you need to explore its capabilities.

- Use `dir()`, `help()`, and `inspect()` to understand objects
- Discover Netmiko's methods and capabilities
- Learn self-sufficient exploration techniques

### [02_secure_connection](./02_secure_connection/) - SSH Authentication (1-2 hours)  

**Why this matters:** Security is fundamental - never hardcode passwords.

- Implement secure credential handling with `getpass`
- Establish SSH connections to network devices
- Test connectivity and handle authentication

### [03_show_commands](./03_show_commands/) - Command Execution (2 hours)

**Why this matters:** Most automation starts with gathering device information.

- Execute read-only show commands
- Understand raw output challenges
- Run commands efficiently across devices

### [04_pretty_printing](./04_pretty_printing/) - Output Formatting (1 hour)

**Why this matters:** Raw output is hard to read and process.

- Format command output for readability
- Use Python's pprint for structured data
- Create professional-looking reports

### [05_config_commands](./05_config_commands/) - Configuration Changes (2 hours)

**Why this matters:** Automation's power is in making changes safely and consistently.

- Execute configuration commands securely
- Handle configuration mode properly
- Implement safety checks and rollback

### [06_parsing](./06_parsing/) - Structured Data (2-3 hours)

**Why this matters:** Converting text to data enables programmatic processing.

- Parse raw text output into structured data
- Use regular expressions for pattern matching
- Leverage NTC-Templates for common commands

### [07_reports](./07_reports/) - Professional Output (1-2 hours)

**Why this matters:** Clear reports communicate results effectively.

- Generate formatted reports with f-strings
- Save results to files
- Create dashboards and summaries

## 🎯 Practice Approach

Each module follows this pattern:

1. **Read the README** - Understand concepts and see minimal examples
2. **Complete the starter files** - Fill in TODOs to make scripts functional  
3. **Try the "Try It" challenges** - Extend and modify the examples
4. **Check yourself** - Answer review questions
5. **Experiment freely** - This is your playground!

---

## Lab Equipment

### Recommended: DevNet Sandbox

Free Cisco lab environment - no hardware needed!

1. Visit [DevNet Sandbox](https://devnetsandbox.cisco.com/)
2. Reserve "IOS XE on CSR Recommended Code" sandbox
3. Use provided credentials and IP address
4. SSH access available immediately

### Alternative: Physical Lab

If you have access to physical Cisco equipment:

- Any Cisco router or switch with SSH enabled
- Management IP address configured
- Valid user credentials with appropriate privileges

### Minimum Device Requirements

- SSH server enabled (`ip ssh version 2`)
- Local user account or AAA authentication
- Management interface with IP connectivity
- Basic IOS command set (show commands, configuration)

## Getting Help

### Troubleshooting Common Issues

**Connection Problems:**

- Verify device IP and SSH connectivity: `ping <device-ip>`
- Test SSH manually: `ssh username@device-ip`
- Check credentials and enable password

**Import Errors:**

- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python version compatibility

**Permission Issues:**

- Verify user has appropriate device privileges
- Check if enable mode is required
- Confirm SSH access is allowed

### Resources

- **Course Discussion Forum**: Post questions and help classmates
- **Office Hours**: Schedule time with instructor
- **DevNet Community**: [developer.cisco.com](https://developer.cisco.com)
- **Netmiko Documentation**: [github.com/ktbyers/netmiko](https://github.com/ktbyers/netmiko)

## Success Criteria

By the end of this module, you should be able to:

- [ ] Connect to network devices securely without hardcoded passwords
- [ ] Execute both show and configuration commands successfully  
- [ ] Parse command output to extract specific information
- [ ] Handle common errors gracefully (timeouts, authentication failures)
- [ ] Generate formatted reports and save them to files
- [ ] Build a complete device inventory or configuration script

## Next Steps

After completing this companion:

1. **Module 3**: Advanced automation with APIs and templating
2. **Capstone Project**: Build a comprehensive network management tool
3. **Certification**: Consider Cisco DevNet Associate certification

## Repository Notes

- **No sample data included** - you'll generate real data from your lab devices
- **Starter files only** - complete the TODOs to make scripts functional
- **Progressive difficulty** - each module builds on previous concepts
- **Real-world focus** - all examples mirror actual network operations

---

**Ready to automate your network?** Start with [01_exploration](./01_exploration/) and begin your journey into network programmability!

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
source netmiko-env/bin/activate
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

**Practice:** Format the output of multiple show commands for better readability

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

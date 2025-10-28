# 06: Parsing with NTC-Templates

## Why This Matters

Raw text output is hard to analyze, search, or manipulate programmatically. Parsing converts unstructured text into structured data (lists, dictionaries) that code can easily process. This transforms network automation from simple command execution to intelligent data analysis.

## Key Terms

- **Parsing** - Converting unstructured text into structured data
- **TextFSM** - Template-based text parsing engine for network output
- **NTC-Templates** - Pre-built parsing templates for common network commands
- **Structured data** - Organized data formats (lists, dictionaries) vs raw text
- **Template** - Pattern definition that describes how to extract data

## Minimal Example

```python
from ntc_templates.parse import parse_output
from netmiko import ConnectHandler

# Get raw output
output = connection.send_command('show version')
print(f"Raw output: {len(output)} characters of text")

# Parse into structured data
parsed = parse_output(
    platform='cisco_ios',
    command='show version', 
    data=output
)

# Now work with structured data!
print(f"Hostname: {parsed[0]['hostname']}")
print(f"Version: {parsed[0]['version']}")
print(f"Uptime: {parsed[0]['uptime']}")
```

## Try It

Complete the TODO items in `basic_parsing.py`:

1. Parse `show version` output using NTC-Templates
2. Extract device information (hostname, version, uptime) from parsed data
3. Parse `show ip interface brief` into a list of interface dictionaries
4. Compare the ease of working with parsed vs raw data
5. **Challenge**: Parse `show ip route` and find all connected routes

## Check Yourself

1. What's the main advantage of parsed data over raw text?
2. How does NTC-Templates know which template to use?
3. What data type does `parse_output()` return?
4. How would you find all 'up' interfaces from parsed data?
5. What happens if no template exists for a command?

## Links

- [NTC-Templates repository](https://github.com/networktocode/ntc-templates)
- [TextFSM documentation](https://github.com/google/textfsm)
- [Available template list](https://github.com/networktocode/ntc-templates/tree/master/ntc_templates/templates)

# 03: Show Commands and Raw Output

## Why This Matters

Show commands are the foundation of network automation - they're read-only and safe to experiment with. However, raw command output is unstructured text that's difficult to process programmatically. Understanding this challenge is essential before learning parsing and formatting techniques.

## Key Terms

- **Show command** - Read-only CLI command that displays device information
- **Raw output** - Unprocessed text returned by network devices
- **Newline characters (`\n`)** - Special characters that create line breaks
- **String processing** - Manipulating text data for analysis
- **Command execution** - Running CLI commands programmatically via SSH

## Minimal Example

```python
from netmiko import ConnectHandler

# After establishing connection...
commands = ['show version', 'show ip interface brief', 'show clock']

for command in commands:
    print(f"\n{'='*50}")
    print(f"Executing: {command}")
    print('='*50)
    
    output = connection.send_command(command)
    print(f"Raw length: {len(output)} characters")
    print(f"Line count: {len(output.split('\\n'))} lines")
    print(output[:200] + "...")  # Show first 200 chars
```

## Try It

Complete the TODO items in `basic_show_commands.py`:

1. Connect to your lab device securely
2. Execute multiple show commands in a loop
3. Analyze the raw output structure (length, line count, special characters)
4. Save raw output to text files for later analysis
5. **Challenge**: Find patterns that could help with parsing

## Check Yourself

1. What makes raw command output difficult to process?
2. How many lines does `show version` typically produce?
3. Which show command produces the most structured output?
4. What special characters appear in network device output?
5. How would you extract just the hostname from `show version`?

## Links

- [Cisco IOS show commands reference](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/command/ios-fundamentals-cr-book.html)
- [Python string methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
- [Text processing techniques](https://docs.python.org/3/library/string.html)

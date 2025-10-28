# 05: Configuration Commands

## Why This Matters

Configuration commands are where automation becomes powerful - they make actual changes to network infrastructure. However, with great power comes great responsibility. Learning safe configuration practices prevents outages and builds confidence in automation tools.

## Key Terms

- **Configuration mode** - CLI mode where device settings can be modified
- **`send_config_set()`** - Netmiko method for sending multiple config commands
- **Configuration verification** - Checking that changes were applied correctly
- **Rollback plan** - Strategy to undo changes if something goes wrong
- **Lab environment** - Safe space to practice without affecting production

## Minimal Example

```python
from netmiko import ConnectHandler

# After establishing connection...
# Configure a loopback interface
config_commands = [
    'interface loopback 100',
    'ip address 100.100.100.100 255.255.255.255',
    'description Created by Python automation',
    'no shutdown'
]

# Send configuration
print("Applying configuration...")
output = connection.send_config_set(config_commands)
print(output)

# Verify the configuration
verification = connection.send_command('show running-config interface loopback 100')
print(f"Verification:\n{verification}")
```

## Try It

Complete the TODO items in `basic_config.py`:

1. Create configuration command lists for loopback interfaces
2. Use `send_config_set()` to apply multiple commands at once  
3. Verify configurations with appropriate show commands
4. Implement error handling for configuration failures
5. **Challenge**: Create a rollback function to remove configurations

## Check Yourself

1. What's the difference between `send_command()` and `send_config_set()`?
2. Why should you verify configurations after applying them?
3. How do you check if a configuration command succeeded?
4. What happens if a configuration command fails mid-sequence?
5. Why is it important to test in lab environments first?

## Links

- [Cisco configuration mode guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fundamentals/configuration/15mt/fundamentals-15-mt-book/cf-cli-basics.html)
- [Netmiko configuration methods](https://github.com/ktbyers/netmiko#configuration-changes)
- [Network automation best practices](https://www.ansible.com/blog/network-automation-best-practices)
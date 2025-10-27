# 🔐 Module 2.2: Secure Connections with getpass

## What You'll Learn

- Use `getpass` to hide password input
- Create secure device connection dictionaries  
- Make your first connection to a network device
- Handle connection success and failure

## Why This Matters

NEVER hardcode passwords in your scripts! Learn the secure way from day one.

## Your Mission 🎯

Complete the starter code to:

1. Collect credentials securely using getpass
2. Create a proper device connection dictionary
3. Establish your first Netmiko connection
4. Test the connection with a simple command

## Lab Requirements 📋

- A Cisco device (router/switch) you can SSH to
- Valid credentials (username/password)
- Device IP address or hostname
- SSH enabled on the device

## Starter Files

- `secure_connect.py` - Build your secure connection script
- `test_connection.py` - Test different connection scenarios

## Success Criteria ✅

- [ ] Password input is hidden when typing
- [ ] Successfully connects to your lab device  
- [ ] Can execute 'show clock' command
- [ ] Properly disconnects when done

## Security Reminders 🔒

- Never put passwords in code
- Never commit credentials to version control
- Always disconnect when finished
- Use strong passwords in production

## Next Steps

Once you can connect securely, you'll explore show commands and raw output!

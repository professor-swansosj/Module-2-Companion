# 02: Secure SSH Connections

## Why This Matters

Network devices contain sensitive configurations and control critical infrastructure. Scripts with hardcoded passwords create security vulnerabilities that can lead to breaches, outages, and compliance violations. Professional network automation requires secure credential handling from day one.

## Key Terms

- **`getpass`** - Python module that hides password input from screen and logs
- **SSH** - Secure Shell protocol providing encrypted connections to network devices
- **Device dictionary** - Python data structure containing connection parameters
- **Credential exposure** - Security vulnerability where passwords are visible in code or logs
- **Authentication** - Process of verifying identity before allowing device access

## Security Fundamentals

**Never hardcode credentials** because:

- Passwords become visible to anyone reading your code
- Version control systems store password history permanently  
- Log files may capture credential information
- Shared scripts expose passwords to unauthorized users

**Always collect interactively** using:

- `input()` for usernames and hostnames (visible information)
- `getpass.getpass()` for passwords (hidden input)
- Error handling for authentication failures

## Your Mission

Open `secure_connect.py` and build a secure connection script. You'll:

- Collect device credentials without exposing them
- Build connection parameters properly
- Handle authentication failures gracefully
- Test connectivity with a simple command

**Figure out the syntax yourself** - use your exploration skills from Module 01!

## Check Yourself

After completing your connection script:

1. Can you see the password while typing it? (You shouldn't!)
2. What happens if you enter wrong credentials?
3. How do you know if the connection succeeded?
4. What information do you need to connect to any network device?
5. Why is it important to disconnect when finished?

## Real-World Context

In enterprise environments:

- **Credential management systems** store passwords securely
- **Multi-factor authentication** adds extra security layers
- **Connection logging** tracks who accessed which devices
- **Automated systems** use certificates instead of passwords

Start with secure habits now - they'll serve you throughout your career.

## Links

- [Python getpass Documentation](https://docs.python.org/3/library/getpass.html) - Secure password input
- [SSH Security Best Practices](https://www.ssh.com/academy/ssh/security) - Professional SSH usage

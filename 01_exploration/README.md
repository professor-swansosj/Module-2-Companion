# 01: Object Exploration with Python Built-ins

## Why This Matters

The most valuable skill in programming isn't memorizing syntax - it's knowing how to explore and understand new code. Python gives you powerful built-in tools to investigate any library. Master these exploration techniques and you'll never be stuck wondering "what can this object do?"

## Key Terms

- **`dir()`** - Shows you what's available on any object
- **`help()`** - Reads the documentation for you  
- **`inspect`** - Gets detailed information about functions and classes
- **Method signature** - Shows what parameters a function expects
- **Public vs private methods** - Public methods (your tools) vs internal methods (implementation details)

## The Discovery Process

When you encounter a new Python library:

1. **Start broad**: Use `dir()` to see what's available
2. **Focus in**: Use `help()` to understand specific methods  
3. **Go deep**: Use `inspect` for detailed signatures and parameters
4. **Find patterns**: Look for naming conventions and method families

## Your Mission

Open `explore_netmiko.py` and complete the TODOs. You'll discover:

- How many methods ConnectHandler actually has
- Which methods are for sending commands vs receiving data
- What parameters each method expects
- What exceptions you need to handle

## Check Yourself

After completing the exploration:

1. How would you find all methods related to configuration?
2. What's the difference between `send_command` and `send_config_set`?
3. Which method signatures include timeout parameters?
4. What exceptions should you always be prepared to catch?
5. How can you tell which parameters are optional vs required?

## Discovery Tips

- **Filter wisely**: Ignore methods starting with `_` (internal use)
- **Read carefully**: Help text tells you parameter types and purposes
- **Look for patterns**: Method names often follow naming conventions
- **Try things**: Python won't break - experiment in the interpreter

## Links

- [Python Built-in Functions](https://docs.python.org/3/library/functions.html) - Your exploration toolkit
- [inspect Module Guide](https://docs.python.org/3/library/inspect.html) - Deep object investigation

# 04: Pretty Printing and Output Formatting

## Why This Matters

Raw network device output is functional but ugly. Professional automation requires clean, readable output for troubleshooting, reports, and user interfaces. Good formatting transforms messy text into clear, actionable information that humans can quickly understand.

## Key Terms

- **`pprint`** - Python module for "pretty printing" structured data
- **String formatting** - Techniques for organizing and presenting text
- **Headers and separators** - Visual elements that organize output sections  
- **Whitespace management** - Controlling spaces, tabs, and line breaks
- **Professional output** - Clean, consistent formatting suitable for reports

## The Formatting Challenge

Compare these two outputs - which would you rather read in a report?

**Raw output:** `GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up      \nGigabitEthernet0/1     unassigned      YES NVRAM  administratively down down    `

**Formatted output:**

```bash
Interface Status Report
=======================
GigE0/0: 192.168.1.1 (UP)
GigE0/1: unassigned  (DOWN)
```

## Try It

Complete the TODO items in `pretty_formatting.py`:

1. Import `pprint` and create formatting functions
2. Add professional headers and separators to command output
3. Create a table-style formatter for interface data
4. Compare raw vs formatted output side-by-side
5. **Challenge**: Build a custom formatter that highlights errors

## Check Yourself

1. When should you use `pprint` vs custom formatting?
2. How do headers and separators improve readability?
3. What's the difference between `.strip()` and `.split()`?
4. How can formatting help identify problems in output?
5. Why is consistent formatting important in automation?

## Links

- [pprint module documentation](https://docs.python.org/3/library/pprint.html)
- [Python string formatting guide](https://docs.python.org/3/tutorial/inputoutput.html)
- [Text alignment and padding](https://docs.python.org/3/library/stdtypes.html#str.ljust)

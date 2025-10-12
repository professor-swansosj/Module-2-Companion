#!/usr/bin/env python3
"""
Module 2 - Script 12: Main Function Patterns for Network Automation
Purpose: Learn proper script structure and main() function patterns

This script demonstrates:
- Using if __name__ == "__main__" pattern
- Command line argument handling
- Script configuration and setup
- Proper program flow and structure
- Exit codes and error handling
- Creating production-ready scripts

Learning Objectives:
- Structure scripts with proper main() functions
- Handle command line arguments effectively
- Use configuration files and environment variables
- Implement proper script initialization
- Create scripts that are importable as modules
- Follow Python best practices for executable scripts
"""

import argparse
import json
import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Setup logging configuration for the script
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (str, optional): Log file path. If None, logs to console only.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logs directory if using file logging
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Setup handlers
    handlers: List[logging.Handler] = [logging.StreamHandler()]  # Console handler
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers,
        force=True  # Override any existing configuration
    )
    
    return logging.getLogger(__name__)

def load_config_file(config_path: str) -> Dict:
    """
    Load configuration from JSON file
    
    Args:
        config_path (str): Path to configuration file
        
    Returns:
        Dict: Configuration data
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        json.JSONDecodeError: If config file is invalid JSON
    """
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in config file: {e.msg}", e.doc, e.pos)

def get_default_config() -> Dict:
    """
    Return default configuration values
    
    Returns:
        Dict: Default configuration
    """
    
    return {
        "devices_file": "sample_data/devices.json",
        "backup_directory": "backups",
        "timeout": 30,
        "concurrent_connections": 5,
        "retry_attempts": 3,
        "commands": [
            "show version",
            "show ip interface brief",
            "show running-config"
        ]
    }

def validate_config(config: Dict) -> bool:
    """
    Validate configuration parameters
    
    Args:
        config (Dict): Configuration to validate
        
    Returns:
        bool: True if configuration is valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    
    required_keys = ['devices_file', 'backup_directory', 'timeout']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")
    
    # Validate timeout
    if not isinstance(config['timeout'], int) or config['timeout'] <= 0:
        raise ValueError("Timeout must be a positive integer")
    
    # Validate backup directory
    backup_dir = Path(config['backup_directory'])
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise ValueError(f"Cannot create backup directory: {config['backup_directory']}")
    
    return True

def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure command line argument parser
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    
    parser = argparse.ArgumentParser(
        description="Network Automation Script with Main Function Pattern",
        epilog="Example: python main_function_demo.py --devices devices.json --backup-all"
    )
    
    # Configuration file
    parser.add_argument(
        '-c', '--config',
        type=str,
        help='Configuration file path (JSON format)'
    )
    
    # Device file
    parser.add_argument(
        '-d', '--devices',
        type=str,
        help='Devices file path (JSON format)'
    )
    
    # Operations
    parser.add_argument(
        '--backup-all',
        action='store_true',
        help='Backup configuration from all devices'
    )
    
    parser.add_argument(
        '--check-status',
        action='store_true',
        help='Check status of all devices'
    )
    
    parser.add_argument(
        '--run-command',
        type=str,
        help='Run specific command on all devices'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output directory for results'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    
    # Logging options
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        help='Log file path'
    )
    
    # Connection options
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Connection timeout in seconds (default: 30)'
    )
    
    parser.add_argument(
        '--concurrent',
        type=int,
        default=5,
        help='Number of concurrent connections (default: 5)'
    )
    
    # Dry run mode
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without executing'
    )
    
    # Verbose output
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    return parser

def load_devices(devices_file: str, logger: logging.Logger) -> List[Dict]:
    """
    Load device configurations from file
    
    Args:
        devices_file (str): Path to devices file
        logger (logging.Logger): Logger instance
        
    Returns:
        List[Dict]: List of device configurations
    """
    
    logger.info(f"Loading devices from: {devices_file}")
    
    try:
        with open(devices_file, 'r') as f:
            data = json.load(f)
        
        if 'devices' in data:
            devices = data['devices']
        else:
            devices = [data] if isinstance(data, dict) else data
        
        logger.info(f"Loaded {len(devices)} device(s)")
        return devices
        
    except FileNotFoundError:
        logger.error(f"Devices file not found: {devices_file}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in devices file: {e}")
        return []

def backup_device_configs(devices: List[Dict], config: Dict, 
                         logger: logging.Logger, dry_run: bool = False) -> int:
    """
    Backup configurations from all devices
    
    Args:
        devices (List[Dict]): List of device configurations
        config (Dict): Script configuration
        logger (logging.Logger): Logger instance
        dry_run (bool): If True, show what would be done without executing
        
    Returns:
        int: Number of successful backups
    """
    
    logger.info(f"Starting backup process for {len(devices)} devices")
    
    if dry_run:
        logger.info("DRY RUN MODE - No actual backups will be performed")
    
    success_count = 0
    backup_dir = Path(config['backup_directory'])
    
    for i, device in enumerate(devices, 1):
        device_name = device.get('name', device.get('host', f'device_{i}'))
        logger.info(f"Processing device {i}/{len(devices)}: {device_name}")
        
        if dry_run:
            logger.info(f"Would backup device: {device_name}")
            success_count += 1
            continue
        
        try:
            # Simulate backup process (in real script, use Netmiko here)
            backup_file = backup_dir / f"{device_name}_backup.cfg"
            
            # Simulate creating backup
            logger.debug(f"Creating backup file: {backup_file}")
            
            # In a real script, you would:
            # 1. Connect to device using Netmiko
            # 2. Execute 'show running-config'
            # 3. Save output to backup file
            
            success_count += 1
            logger.info(f"Backup successful: {device_name}")
            
        except Exception as e:
            logger.error(f"Backup failed for {device_name}: {e}")
    
    logger.info(f"Backup process complete. {success_count}/{len(devices)} successful")
    return success_count

def check_device_status(devices: List[Dict], config: Dict, 
                       logger: logging.Logger, dry_run: bool = False) -> Dict:
    """
    Check status of all devices
    
    Args:
        devices (List[Dict]): List of device configurations
        config (Dict): Script configuration
        logger (logging.Logger): Logger instance
        dry_run (bool): If True, show what would be done without executing
        
    Returns:
        Dict: Status results
    """
    
    logger.info(f"Checking status of {len(devices)} devices")
    
    if dry_run:
        logger.info("DRY RUN MODE - No actual connections will be made")
    
    results = {
        'total': len(devices),
        'reachable': 0,
        'unreachable': 0,
        'details': []
    }
    
    for i, device in enumerate(devices, 1):
        device_name = device.get('name', device.get('host', f'device_{i}'))
        device_ip = device.get('host', 'unknown')
        
        logger.info(f"Checking device {i}/{len(devices)}: {device_name}")
        
        if dry_run:
            logger.info(f"Would check connectivity to: {device_ip}")
            results['reachable'] += 1
            results['details'].append({
                'device': device_name,
                'ip': device_ip,
                'status': 'simulated_reachable'
            })
            continue
        
        try:
            # Simulate connectivity check (in real script, use ping or Netmiko)
            import random
            is_reachable = random.choice([True, True, False])  # Simulate mostly successful
            
            if is_reachable:
                results['reachable'] += 1
                status = 'reachable'
                logger.info(f"Device reachable: {device_name}")
            else:
                results['unreachable'] += 1
                status = 'unreachable'
                logger.warning(f"Device unreachable: {device_name}")
            
            results['details'].append({
                'device': device_name,
                'ip': device_ip,
                'status': status
            })
            
        except Exception as e:
            results['unreachable'] += 1
            logger.error(f"Status check failed for {device_name}: {e}")
            results['details'].append({
                'device': device_name,
                'ip': device_ip,
                'status': 'error',
                'error': str(e)
            })
    
    logger.info(f"Status check complete. {results['reachable']} reachable, {results['unreachable']} unreachable")
    return results

def run_command_on_devices(devices: List[Dict], command: str, config: Dict,
                          logger: logging.Logger, dry_run: bool = False) -> Dict:
    """
    Run a command on all devices
    
    Args:
        devices (List[Dict]): List of device configurations
        command (str): Command to execute
        config (Dict): Script configuration
        logger (logging.Logger): Logger instance
        dry_run (bool): If True, show what would be done without executing
        
    Returns:
        Dict: Command execution results
    """
    
    logger.info(f"Running command '{command}' on {len(devices)} devices")
    
    if dry_run:
        logger.info("DRY RUN MODE - No actual commands will be executed")
    
    results = {
        'command': command,
        'total': len(devices),
        'successful': 0,
        'failed': 0,
        'outputs': []
    }
    
    for i, device in enumerate(devices, 1):
        device_name = device.get('name', device.get('host', f'device_{i}'))
        
        logger.info(f"Executing on device {i}/{len(devices)}: {device_name}")
        
        if dry_run:
            logger.info(f"Would execute '{command}' on {device_name}")
            results['successful'] += 1
            continue
        
        try:
            # Simulate command execution (in real script, use Netmiko)
            import random
            
            if random.choice([True, True, True, False]):  # Simulate mostly successful
                output = f"Simulated output from {device_name} for command '{command}'"
                results['successful'] += 1
                logger.debug(f"Command successful on {device_name}")
                
                results['outputs'].append({
                    'device': device_name,
                    'status': 'success',
                    'output': output[:100] + '...' if len(output) > 100 else output
                })
            else:
                raise Exception("Simulated command failure")
                
        except Exception as e:
            results['failed'] += 1
            logger.error(f"Command failed on {device_name}: {e}")
            
            results['outputs'].append({
                'device': device_name,
                'status': 'failed',
                'error': str(e)
            })
    
    logger.info(f"Command execution complete. {results['successful']} successful, {results['failed']} failed")
    return results

def save_results(results: Dict, output_path: str, output_format: str, 
                logger: logging.Logger) -> bool:
    """
    Save results to file in specified format
    
    Args:
        results (Dict): Results data to save
        output_path (str): Output file path
        output_format (str): Output format (json, text, csv)
        logger (logging.Logger): Logger instance
        
    Returns:
        bool: True if save successful
    """
    
    logger.info(f"Saving results to: {output_path} (format: {output_format})")
    
    try:
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if output_format == 'json':
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
                
        elif output_format == 'text':
            with open(output_path, 'w') as f:
                f.write("Results Summary\n")
                f.write("===============\n")
                f.write(f"Total items: {results.get('total', 'N/A')}\n")
                
                if 'reachable' in results:
                    f.write(f"Reachable: {results['reachable']}\n")
                    f.write(f"Unreachable: {results['unreachable']}\n")
                
                if 'successful' in results:
                    f.write(f"Successful: {results['successful']}\n")
                    f.write(f"Failed: {results['failed']}\n")
        
        elif output_format == 'csv':
            import csv
            with open(output_path, 'w', newline='') as f:
                if 'details' in results and results['details']:
                    fieldnames = results['details'][0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results['details'])
        
        logger.info(f"Results saved successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        return False

def main():
    """
    Main function - entry point for the script
    
    This function demonstrates proper script structure:
    1. Parse command line arguments
    2. Setup logging
    3. Load and validate configuration
    4. Execute requested operations
    5. Save results if requested
    6. Exit with appropriate code
    """
    
    # Parse command line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_level, args.log_file)
    logger.info("Starting network automation script")
    
    try:
        # Load configuration
        if args.config:
            logger.info(f"Loading configuration from: {args.config}")
            config = load_config_file(args.config)
        else:
            logger.info("Using default configuration")
            config = get_default_config()
        
        # Override config with command line arguments
        if args.devices:
            config['devices_file'] = args.devices
        if args.output:
            config['backup_directory'] = args.output
        if args.timeout:
            config['timeout'] = args.timeout
        
        # Validate configuration
        validate_config(config)
        logger.info("Configuration validated successfully")
        
        # Load devices
        devices = load_devices(config['devices_file'], logger)
        if not devices:
            logger.error("No devices loaded. Exiting.")
            return 1
        
        # Determine operation to perform
        if not any([args.backup_all, args.check_status, args.run_command]):
            logger.error("No operation specified. Use --help for options.")
            return 1
        
        results = None
        
        # Execute backup operation
        if args.backup_all:
            logger.info("Starting backup operation")
            success_count = backup_device_configs(devices, config, logger, args.dry_run)
            results = {'operation': 'backup', 'successful': success_count, 'total': len(devices)}
        
        # Execute status check
        elif args.check_status:
            logger.info("Starting status check operation")
            results = check_device_status(devices, config, logger, args.dry_run)
        
        # Execute command
        elif args.run_command:
            logger.info(f"Starting command execution: {args.run_command}")
            results = run_command_on_devices(devices, args.run_command, config, logger, args.dry_run)
        
        # Save results if output path specified
        if results and args.output:
            output_file = f"{args.output}/results.{args.format}"
            save_results(results, output_file, args.format, logger)
        
        # Print summary
        if results:
            print("\n" + "="*60)
            print("OPERATION SUMMARY")
            print("="*60)
            
            if args.backup_all:
                print(f"Backup operation: {results['successful']}/{results['total']} successful")
            elif args.check_status:
                print(f"Status check: {results['reachable']}/{results['total']} reachable")
            elif args.run_command:
                print(f"Command execution: {results['successful']}/{results['total']} successful")
            
            if args.verbose and 'details' in results:
                print("\nDetailed results:")
                for detail in results['details'][:5]:  # Show first 5
                    print(f"  {detail}")
                if len(results.get('details', [])) > 5:
                    print(f"  ... and {len(results['details']) - 5} more")
        
        logger.info("Script completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Script failed with error: {e}")
        if args.verbose:
            import traceback
            logger.error(traceback.format_exc())
        return 1

# Demonstration functions that can be called when script is imported
def demo_argument_parsing():
    """
    Demonstrate argument parsing functionality
    """
    
    print("="*60)
    print("ARGUMENT PARSING DEMO")
    print("="*60)
    
    parser = create_argument_parser()
    
    print("Available command line arguments:")
    parser.print_help()
    
    print("\nExample command lines:")
    examples = [
        "python main_function_demo.py --backup-all",
        "python main_function_demo.py --check-status --verbose",
        "python main_function_demo.py --run-command 'show version' --output results",
        "python main_function_demo.py -c config.json -d devices.json --backup-all --dry-run"
    ]
    
    for example in examples:
        print(f"  {example}")

def demo_config_management():
    """
    Demonstrate configuration loading and validation
    """
    
    print("\n" + "="*60)
    print("CONFIGURATION MANAGEMENT DEMO") 
    print("="*60)
    
    # Show default config
    default_config = get_default_config()
    print("Default configuration:")
    for key, value in default_config.items():
        print(f"  {key}: {value}")
    
    # Demonstrate validation
    print("\nValidating configuration...")
    try:
        is_valid = validate_config(default_config)
        print(f"✓ Configuration is valid: {is_valid}")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")

# Script execution entry point
if __name__ == "__main__":
    # This block only runs when script is executed directly, not when imported
    
    # Check for demo mode
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        print("Module 2 - Main Function Patterns Demo")
        print("Learn proper Python script structure and patterns")
        
        demo_argument_parsing()
        demo_config_management()
        
        print("\n" + "="*70)
        print("MAIN FUNCTION PATTERN DEMO COMPLETE!")
        print("="*70)
        print("Key learning points:")
        print("1. Use if __name__ == '__main__' to make scripts importable")
        print("2. Create a main() function as the script entry point") 
        print("3. Use argparse for professional command line interfaces")
        print("4. Setup logging early in the script execution")
        print("5. Load and validate configuration before main operations")
        print("6. Use try/except blocks to handle errors gracefully")
        print("7. Return appropriate exit codes (0 = success, non-zero = error)")
        print("8. Make scripts both executable and importable as modules")
        print("9. Provide comprehensive help and documentation")
        print("10. Use type hints and docstrings for better code clarity")
    else:
        # Run the actual script
        exit_code = main()
        sys.exit(exit_code)
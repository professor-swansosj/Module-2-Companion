#!/usr/bin/env python3
"""
Module 2 - Complete Example: Network Device Inventory and Monitoring System
Purpose: Comprehensive network automation script combining all learned concepts

This script demonstrates:
- Complete production-ready network automation script
- Integration of all Module 2 concepts
- Error handling, functions, and main() patterns
- Configuration management and logging
- Device inventory and status monitoring
- Configuration backup and restoration
- Report generation and data export

Learning Objectives:
- Build complete network automation solutions
- Integrate multiple network automation concepts
- Create production-ready scripts with proper structure
- Handle complex error scenarios gracefully
- Generate professional reports and documentation
- Manage device configurations at scale
"""

import json
import os
import sys
import argparse
import logging
import time
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import concurrent.futures
from dataclasses import dataclass

@dataclass
class DeviceStatus:
    """Data class for device status information"""
    name: str
    ip_address: str
    device_type: str
    status: str
    uptime: Optional[str] = None
    version: Optional[str] = None
    interfaces_up: Optional[int] = None
    interfaces_total: Optional[int] = None
    last_backup: Optional[str] = None
    error_message: Optional[str] = None

class NetworkInventorySystem:
    """
    Complete network inventory and monitoring system
    
    This class encapsulates all functionality for managing network device
    inventory, status monitoring, and configuration management.
    """
    
    def __init__(self, config: Dict, logger: logging.Logger):
        """
        Initialize the network inventory system
        
        Args:
            config (Dict): System configuration
            logger (logging.Logger): Logger instance
        """
        self.config = config
        self.logger = logger
        self.devices = []
        self.device_status = {}
        self.backup_directory = Path(config.get('backup_directory', 'backups'))
        self.reports_directory = Path(config.get('reports_directory', 'reports'))
        
        # Create necessary directories
        self.backup_directory.mkdir(parents=True, exist_ok=True)
        self.reports_directory.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Initialized NetworkInventorySystem")
        self.logger.info(f"Backup directory: {self.backup_directory}")
        self.logger.info(f"Reports directory: {self.reports_directory}")
    
    def load_devices(self, devices_file: str) -> bool:
        """
        Load device configurations from file
        
        Args:
            devices_file (str): Path to devices configuration file
            
        Returns:
            bool: True if devices loaded successfully
        """
        
        try:
            self.logger.info(f"Loading devices from: {devices_file}")
            
            with open(devices_file, 'r') as f:
                data = json.load(f)
            
            if 'devices' in data:
                self.devices = data['devices']
            else:
                self.devices = [data] if isinstance(data, dict) else data
            
            self.logger.info(f"Loaded {len(self.devices)} device(s)")
            
            # Validate device configurations
            valid_devices = []
            for i, device in enumerate(self.devices):
                if self._validate_device_config(device, i):
                    valid_devices.append(device)
            
            self.devices = valid_devices
            self.logger.info(f"Validated {len(self.devices)} device(s)")
            
            return len(self.devices) > 0
            
        except FileNotFoundError:
            self.logger.error(f"Devices file not found: {devices_file}")
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in devices file: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error loading devices: {e}")
            return False
    
    def _validate_device_config(self, device: Dict, index: int) -> bool:
        """
        Validate device configuration
        
        Args:
            device (Dict): Device configuration
            index (int): Device index for error reporting
            
        Returns:
            bool: True if device configuration is valid
        """
        
        required_fields = ['device_type', 'host', 'username', 'password']
        
        for field in required_fields:
            if field not in device or not device[field]:
                self.logger.warning(f"Device {index}: Missing or empty field '{field}' - skipping")
                return False
        
        # Validate IP address format
        try:
            import socket
            socket.inet_aton(device['host'])
        except socket.error:
            self.logger.warning(f"Device {index}: Invalid IP address '{device['host']}' - skipping")
            return False
        
        return True
    
    def simulate_device_connection(self, device: Dict) -> DeviceStatus:
        """
        Simulate device connection and gather status information
        
        In a real implementation, this would use Netmiko to connect to devices
        
        Args:
            device (Dict): Device configuration
            
        Returns:
            DeviceStatus: Device status information
        """
        
        device_name = device.get('name', device.get('host'))
        
        try:
            # Simulate connection delay
            time.sleep(0.5)
            
            # Simulate different outcomes
            import random
            
            success_rate = 0.85  # 85% success rate
            if random.random() > success_rate:
                raise Exception("Simulated connection failure")
            
            # Generate simulated status data
            status = DeviceStatus(
                name=device_name,
                ip_address=device['host'],
                device_type=device['device_type'],
                status='connected',
                uptime=f"{random.randint(1, 365)} days, {random.randint(0, 23)} hours",
                version=f"Cisco IOS Software, Version {random.randint(12, 17)}.{random.randint(1, 9)}",
                interfaces_up=random.randint(8, 24),
                interfaces_total=24,
                last_backup=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            self.logger.debug(f"Successfully connected to {device_name}")
            return status
            
        except Exception as e:
            self.logger.warning(f"Failed to connect to {device_name}: {e}")
            return DeviceStatus(
                name=device_name,
                ip_address=device['host'],
                device_type=device['device_type'],
                status='failed',
                error_message=str(e)
            )
    
    def inventory_devices(self, concurrent_connections: int = 5) -> Dict:
        """
        Perform inventory scan of all devices
        
        Args:
            concurrent_connections (int): Number of concurrent connections
            
        Returns:
            Dict: Inventory results summary
        """
        
        self.logger.info(f"Starting device inventory scan for {len(self.devices)} devices")
        self.logger.info(f"Using {concurrent_connections} concurrent connections")
        
        results = {
            'start_time': datetime.now(),
            'total_devices': len(self.devices),
            'successful': 0,
            'failed': 0,
            'devices': []
        }
        
        # Use ThreadPoolExecutor for concurrent connections
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_connections) as executor:
            # Submit all connection tasks
            future_to_device = {
                executor.submit(self.simulate_device_connection, device): device 
                for device in self.devices
            }
            
            # Process completed tasks
            for future in concurrent.futures.as_completed(future_to_device):
                device = future_to_device[future]
                
                try:
                    device_status = future.result()
                    
                    if device_status.status == 'connected':
                        results['successful'] += 1
                        self.logger.info(f"✓ {device_status.name}")
                    else:
                        results['failed'] += 1
                        self.logger.warning(f"✗ {device_status.name}: {device_status.error_message}")
                    
                    results['devices'].append(device_status)
                    
                    # Store in instance variable for reporting
                    self.device_status[device_status.name] = device_status
                    
                except Exception as e:
                    results['failed'] += 1
                    device_name = device.get('name', device.get('host'))
                    self.logger.error(f"✗ {device_name}: Unexpected error: {e}")
        
        results['end_time'] = datetime.now()
        results['duration'] = results['end_time'] - results['start_time']
        
        self.logger.info(f"Inventory scan complete in {results['duration']}")
        self.logger.info(f"Results: {results['successful']} successful, {results['failed']} failed")
        
        return results
    
    def backup_configurations(self, target_devices: Optional[List[str]] = None) -> Dict:
        """
        Backup device configurations
        
        Args:
            target_devices (Optional[List[str]]): Specific devices to backup. If None, backup all.
            
        Returns:
            Dict: Backup results summary
        """
        
        devices_to_backup = []
        
        if target_devices:
            devices_to_backup = [d for d in self.devices if d.get('name') in target_devices or d.get('host') in target_devices]
        else:
            devices_to_backup = self.devices
        
        self.logger.info(f"Starting configuration backup for {len(devices_to_backup)} devices")
        
        results = {
            'start_time': datetime.now(),
            'total_devices': len(devices_to_backup),
            'successful': 0,
            'failed': 0,
            'backup_files': []
        }
        
        for device in devices_to_backup:
            device_name = device.get('name', device.get('host'))
            
            try:
                # Generate backup filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = f"{device_name}_running_config_{timestamp}.cfg"
                backup_path = self.backup_directory / backup_filename
                
                # Simulate configuration backup
                config_content = self._simulate_device_config(device)
                
                with open(backup_path, 'w') as f:
                    f.write(config_content)
                
                results['successful'] += 1
                results['backup_files'].append(str(backup_path))
                
                # Update device status
                if device_name in self.device_status:
                    self.device_status[device_name].last_backup = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                self.logger.info(f"✓ Backed up {device_name} to {backup_filename}")
                
            except Exception as e:
                results['failed'] += 1
                self.logger.error(f"✗ Backup failed for {device_name}: {e}")
        
        results['end_time'] = datetime.now()
        results['duration'] = results['end_time'] - results['start_time']
        
        self.logger.info(f"Backup complete in {results['duration']}")
        self.logger.info(f"Results: {results['successful']} successful, {results['failed']} failed")
        
        return results
    
    def _simulate_device_config(self, device: Dict) -> str:
        """
        Simulate device configuration content
        
        Args:
            device (Dict): Device configuration
            
        Returns:
            str: Simulated configuration content
        """
        
        device_name = device.get('name', device.get('host'))
        
        config = f"""!
! Configuration backup for {device_name}
! Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname {device_name}
!
boot-start-marker
boot-end-marker
!
!
enable secret 5 $1$mERr$hx5rVt7rPNoS4wqbXKX7m0
!
no aaa new-model
ethernet lmi ce
!
!
!
mmi polling-interval 60
no mmi auto-configure
no mmi pvc
mmi snmp-timeout 180
!
!
!
!
!
no ip domain lookup
ip cef
no ipv6 cef
!
multilink bundle-name authenticated
!
!
!
!
!
redundancy
!
!
! 
!
!
!
!
!
!
!
!
!
!
!
!
interface GigabitEthernet0/0
 ip address {device['host']} 255.255.255.0
 duplex auto
 speed auto
 media-type rj45
!
interface GigabitEthernet0/1
 no ip address
 shutdown
 duplex auto
 speed auto
 media-type rj45
!
interface Loopback0
 ip address 10.1.1.1 255.255.255.255
!
ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!
!
!
!
control-plane
!
banner exec ^C
**************************************************************************
* IOSv is strictly limited to use for evaluation, demonstration and IOS  *
* education. IOSv is provided as-is and is not supported by Cisco's      *
* Technical Advisory Center. Any use or disclosure, in whole or in part, *
* of the IOSv Software or Documentation to any third party for any       *
* purposes is expressly prohibited except as otherwise authorized by      *
* Cisco in writing.                                                      *
**************************************************************************^C
banner incoming ^C
**************************************************************************
* IOSv is strictly limited to use for evaluation, demonstration and IOS  *
* education. IOSv is provided as-is and is not supported by Cisco's      *
* Technical Advisory Center. Any use or disclosure, in whole or in part, *
* of the IOSv Software or Documentation to any third party for any       *
* purposes is expressly prohibited except as otherwise authorized by      *
* Cisco in writing.                                                      *
**************************************************************************^C
banner login ^C
**************************************************************************
* IOSv is strictly limited to use for evaluation, demonstration and IOS  *
* education. IOSv is provided as-is and is not supported by Cisco's      *
* Technical Advisory Center. Any use or disclosure, in whole or in part, *
* of the IOSv Software or Documentation to any third party for any       *
* purposes is expressly prohibited except as otherwise authorized by      *
* Cisco in writing.                                                      *
**************************************************************************^C
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
line vty 0 4
 login
!
no scheduler allocate
!
end
"""
        return config
    
    def generate_inventory_report(self, output_format: str = 'text') -> str:
        """
        Generate comprehensive inventory report
        
        Args:
            output_format (str): Report format ('text', 'html', 'json', 'csv')
            
        Returns:
            str: Path to generated report file
        """
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format == 'text':
            report_path = self.reports_directory / f"inventory_report_{timestamp}.txt"
            self._generate_text_report(report_path)
        elif output_format == 'html':
            report_path = self.reports_directory / f"inventory_report_{timestamp}.html"
            self._generate_html_report(report_path)
        elif output_format == 'json':
            report_path = self.reports_directory / f"inventory_report_{timestamp}.json"
            self._generate_json_report(report_path)
        elif output_format == 'csv':
            report_path = self.reports_directory / f"inventory_report_{timestamp}.csv"
            self._generate_csv_report(report_path)
        else:
            raise ValueError(f"Unsupported report format: {output_format}")
        
        self.logger.info(f"Generated {output_format.upper()} report: {report_path}")
        return str(report_path)
    
    def _generate_text_report(self, report_path: Path):
        """Generate text format report"""
        
        with open(report_path, 'w') as f:
            f.write("NETWORK DEVICE INVENTORY REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Devices: {len(self.device_status)}\n\n")
            
            # Summary statistics
            connected = sum(1 for d in self.device_status.values() if d.status == 'connected')
            failed = len(self.device_status) - connected
            
            f.write("SUMMARY\n")
            f.write("-" * 20 + "\n")
            f.write(f"Connected Devices: {connected}\n")
            f.write(f"Failed Devices: {failed}\n")
            f.write(f"Success Rate: {(connected / len(self.device_status) * 100):.1f}%\n\n")
            
            # Device details
            f.write("DEVICE DETAILS\n")
            f.write("-" * 20 + "\n")
            
            for device_status in self.device_status.values():
                f.write(f"\nDevice: {device_status.name}\n")
                f.write(f"  IP Address: {device_status.ip_address}\n")
                f.write(f"  Type: {device_status.device_type}\n")
                f.write(f"  Status: {device_status.status}\n")
                
                if device_status.status == 'connected':
                    f.write(f"  Uptime: {device_status.uptime}\n")
                    f.write(f"  Version: {device_status.version}\n")
                    f.write(f"  Interfaces: {device_status.interfaces_up}/{device_status.interfaces_total} up\n")
                    if device_status.last_backup:
                        f.write(f"  Last Backup: {device_status.last_backup}\n")
                else:
                    f.write(f"  Error: {device_status.error_message}\n")
    
    def _generate_html_report(self, report_path: Path):
        """Generate HTML format report"""
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Network Device Inventory Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; }}
        .summary {{ margin: 20px 0; }}
        .device {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .connected {{ border-left: 4px solid #4CAF50; }}
        .failed {{ border-left: 4px solid #f44336; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Network Device Inventory Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total Devices: {len(self.device_status)}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Devices</td><td>{len(self.device_status)}</td></tr>
            <tr><td>Connected</td><td>{sum(1 for d in self.device_status.values() if d.status == 'connected')}</td></tr>
            <tr><td>Failed</td><td>{sum(1 for d in self.device_status.values() if d.status == 'failed')}</td></tr>
        </table>
    </div>
    
    <div class="devices">
        <h2>Device Details</h2>
"""
        
        for device_status in self.device_status.values():
            status_class = 'connected' if device_status.status == 'connected' else 'failed'
            
            html_content += f"""
        <div class="device {status_class}">
            <h3>{device_status.name}</h3>
            <p><strong>IP:</strong> {device_status.ip_address}</p>
            <p><strong>Type:</strong> {device_status.device_type}</p>
            <p><strong>Status:</strong> {device_status.status}</p>
"""
            
            if device_status.status == 'connected':
                html_content += f"""
            <p><strong>Uptime:</strong> {device_status.uptime}</p>
            <p><strong>Version:</strong> {device_status.version}</p>
            <p><strong>Interfaces:</strong> {device_status.interfaces_up}/{device_status.interfaces_total} up</p>
"""
            else:
                html_content += f"""
            <p><strong>Error:</strong> {device_status.error_message}</p>
"""
            
            html_content += "        </div>\n"
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(report_path, 'w') as f:
            f.write(html_content)
    
    def _generate_json_report(self, report_path: Path):
        """Generate JSON format report"""
        
        report_data = {
            'generated': datetime.now().isoformat(),
            'total_devices': len(self.device_status),
            'summary': {
                'connected': sum(1 for d in self.device_status.values() if d.status == 'connected'),
                'failed': sum(1 for d in self.device_status.values() if d.status == 'failed')
            },
            'devices': []
        }
        
        for device_status in self.device_status.values():
            device_data = {
                'name': device_status.name,
                'ip_address': device_status.ip_address,
                'device_type': device_status.device_type,
                'status': device_status.status
            }
            
            if device_status.status == 'connected':
                device_data.update({
                    'uptime': device_status.uptime,
                    'version': device_status.version,
                    'interfaces_up': device_status.interfaces_up,
                    'interfaces_total': device_status.interfaces_total,
                    'last_backup': device_status.last_backup
                })
            else:
                device_data['error_message'] = device_status.error_message
            
            report_data['devices'].append(device_data)
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
    
    def _generate_csv_report(self, report_path: Path):
        """Generate CSV format report"""
        
        fieldnames = [
            'name', 'ip_address', 'device_type', 'status', 'uptime', 
            'version', 'interfaces_up', 'interfaces_total', 'last_backup', 'error_message'
        ]
        
        with open(report_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for device_status in self.device_status.values():
                row = {
                    'name': device_status.name,
                    'ip_address': device_status.ip_address,
                    'device_type': device_status.device_type,
                    'status': device_status.status,
                    'uptime': device_status.uptime or '',
                    'version': device_status.version or '',
                    'interfaces_up': device_status.interfaces_up or '',
                    'interfaces_total': device_status.interfaces_total or '',
                    'last_backup': device_status.last_backup or '',
                    'error_message': device_status.error_message or ''
                }
                writer.writerow(row)

def setup_logging(log_level: str, log_file: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration"""
    
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers,
        force=True
    )
    
    return logging.getLogger(__name__)

def load_config(config_file: Optional[str] = None) -> Dict:
    """Load configuration from file or return defaults"""
    
    default_config = {
        'devices_file': 'sample_data/devices.json',
        'backup_directory': 'backups',
        'reports_directory': 'reports',
        'concurrent_connections': 5,
        'timeout': 30
    }
    
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
            default_config.update(file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    return default_config

def create_argument_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    
    parser = argparse.ArgumentParser(
        description="Complete Network Device Inventory and Monitoring System",
        epilog="Example: python complete_example.py --inventory --backup --report html"
    )
    
    parser.add_argument('-c', '--config', help='Configuration file path')
    parser.add_argument('-d', '--devices', help='Devices file path')
    
    # Operations
    parser.add_argument('--inventory', action='store_true', help='Run device inventory scan')
    parser.add_argument('--backup', action='store_true', help='Backup device configurations')
    parser.add_argument('--report', choices=['text', 'html', 'json', 'csv'], help='Generate report in specified format')
    
    # Options
    parser.add_argument('--concurrent', type=int, default=5, help='Concurrent connections (default: 5)')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO')
    parser.add_argument('--log-file', help='Log file path')
    
    return parser

def main():
    """Main function - demonstrates complete network automation system"""
    
    # Parse arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_level, args.log_file)
    logger.info("Starting Network Inventory System")
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        if args.devices:
            config['devices_file'] = args.devices
        if args.concurrent:
            config['concurrent_connections'] = args.concurrent
        
        # Initialize system
        inventory_system = NetworkInventorySystem(config, logger)
        
        # Load devices
        devices_file = config['devices_file']
        if not inventory_system.load_devices(devices_file):
            logger.error("Failed to load devices. Exiting.")
            return 1
        
        # Run operations
        if args.inventory:
            logger.info("Running device inventory scan...")
            inventory_results = inventory_system.inventory_devices(config['concurrent_connections'])
            
            print(f"\n{'='*60}")
            print("INVENTORY SCAN RESULTS")
            print(f"{'='*60}")
            print(f"Total devices: {inventory_results['total_devices']}")
            print(f"Successful: {inventory_results['successful']}")
            print(f"Failed: {inventory_results['failed']}")
            print(f"Duration: {inventory_results['duration']}")
        
        if args.backup:
            logger.info("Starting configuration backup...")
            backup_results = inventory_system.backup_configurations()
            
            print(f"\n{'='*60}")
            print("BACKUP RESULTS")
            print(f"{'='*60}")
            print(f"Total devices: {backup_results['total_devices']}")
            print(f"Successful: {backup_results['successful']}")
            print(f"Failed: {backup_results['failed']}")
            print(f"Duration: {backup_results['duration']}")
            print(f"Backup files created: {len(backup_results['backup_files'])}")
        
        if args.report:
            logger.info(f"Generating {args.report.upper()} report...")
            report_path = inventory_system.generate_inventory_report(args.report)
            
            print(f"\n{'='*60}")
            print("REPORT GENERATION")
            print(f"{'='*60}")
            print(f"Format: {args.report.upper()}")
            print(f"Report saved to: {report_path}")
        
        # If no specific operations requested, run all
        if not any([args.inventory, args.backup, args.report]):
            logger.info("No specific operations requested. Running full system demo...")
            
            # Run inventory
            inventory_results = inventory_system.inventory_devices(config['concurrent_connections'])
            
            # Run backup
            backup_results = inventory_system.backup_configurations()
            
            # Generate reports in all formats
            for report_format in ['text', 'html', 'json', 'csv']:
                report_path = inventory_system.generate_inventory_report(report_format)
            
            print(f"\n{'='*70}")
            print("COMPLETE NETWORK AUTOMATION SYSTEM DEMO")
            print(f"{'='*70}")
            print(f"Inventory: {inventory_results['successful']}/{inventory_results['total_devices']} devices")
            print(f"Backups: {backup_results['successful']}/{backup_results['total_devices']} configs")
            print(f"Reports: Generated in all formats (text, html, json, csv)")
            print(f"Duration: {inventory_results['duration'] + backup_results['duration']}")
        
        logger.info("Network Inventory System completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"System error: {e}")
        return 1

if __name__ == "__main__":
    # This demonstrates the complete network automation system
    # integrating all concepts from Module 2
    
    exit_code = main()
    sys.exit(exit_code)
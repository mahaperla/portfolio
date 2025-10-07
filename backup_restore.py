#!/usr/bin/env python3
"""
Portfolio Backup and Restore Utility
Handles backup and restoration of all portfolio data
"""

import os
import json
import shutil
import zipfile
import argparse
from datetime import datetime
import logging

class PortfolioBackup:
    def __init__(self):
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.backup_dir = os.path.join(self.app_dir, 'backups')
        self.setup_logging()
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('backup.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_backup(self, include_logs=False):
        """Create a full backup of the portfolio"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'portfolio_backup_{timestamp}'
        backup_path = os.path.join(self.backup_dir, f'{backup_name}.zip')
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
                # Backup data files
                self._backup_directory(backup_zip, 'data', 'data/')
                
                # Backup static files (excluding large files)
                self._backup_directory(backup_zip, 'static', 'static/', 
                                     exclude_patterns=['*.mp4', '*.avi', '*.mov'])
                
                # Backup templates
                self._backup_directory(backup_zip, 'templates', 'templates/')
                
                # Backup configuration files
                config_files = ['settings.json', 'requirements.txt', 'app.py']
                for file in config_files:
                    if os.path.exists(file):
                        backup_zip.write(file, file)
                
                # Backup utility scripts
                self._backup_directory(backup_zip, 'utils', 'utils/')
                
                # Optionally backup logs
                if include_logs:
                    self._backup_directory(backup_zip, 'logs', 'logs/')
                
                # Create backup manifest
                manifest = self._create_manifest()
                backup_zip.writestr('backup_manifest.json', json.dumps(manifest, indent=2))
            
            self.logger.info(f"Backup created successfully: {backup_path}")
            self._cleanup_old_backups()
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Backup failed: {str(e)}")
            if os.path.exists(backup_path):
                os.remove(backup_path)
            raise
    
    def restore_backup(self, backup_file, target_dir=None):
        """Restore from a backup file"""
        if target_dir is None:
            target_dir = self.app_dir
        
        if not os.path.exists(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
        try:
            # Create restore directory
            restore_dir = os.path.join(target_dir, 'restored_portfolio')
            os.makedirs(restore_dir, exist_ok=True)
            
            with zipfile.ZipFile(backup_file, 'r') as backup_zip:
                # Verify backup integrity
                backup_zip.testzip()
                
                # Extract all files
                backup_zip.extractall(restore_dir)
                
                # Read manifest if available
                manifest_path = os.path.join(restore_dir, 'backup_manifest.json')
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                    self.logger.info(f"Restored backup from: {manifest['created_at']}")
                    self.logger.info(f"Backup version: {manifest['version']}")
                
                self.logger.info(f"Backup restored to: {restore_dir}")
                return restore_dir
                
        except Exception as e:
            self.logger.error(f"Restore failed: {str(e)}")
            raise
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith('.zip') and file.startswith('portfolio_backup_'):
                file_path = os.path.join(self.backup_dir, file)
                file_size = os.path.getsize(file_path)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                backups.append({
                    'filename': file,
                    'path': file_path,
                    'size': self._format_size(file_size),
                    'created': file_time.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    def _backup_directory(self, zip_file, source_dir, archive_dir, exclude_patterns=None):
        """Backup a directory to the zip file"""
        if not os.path.exists(source_dir):
            return
        
        exclude_patterns = exclude_patterns or []
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                # Check if file should be excluded
                if any(self._matches_pattern(file, pattern) for pattern in exclude_patterns):
                    continue
                
                file_path = os.path.join(root, file)
                archive_path = os.path.join(archive_dir, os.path.relpath(file_path, source_dir))
                zip_file.write(file_path, archive_path)
    
    def _matches_pattern(self, filename, pattern):
        """Check if filename matches a pattern (supports * wildcard)"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def _create_manifest(self):
        """Create backup manifest with metadata"""
        return {
            'created_at': datetime.now().isoformat(),
            'version': '1.0',
            'app_version': self._get_app_version(),
            'python_version': self._get_python_version(),
            'files_count': self._count_files(),
            'backup_type': 'full'
        }
    
    def _get_app_version(self):
        """Get application version"""
        try:
            # You can implement version tracking here
            return "1.0.0"
        except:
            return "unknown"
    
    def _get_python_version(self):
        """Get Python version"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def _count_files(self):
        """Count total files in the application"""
        count = 0
        for root, dirs, files in os.walk(self.app_dir):
            # Skip backup directory and other unnecessary directories
            dirs[:] = [d for d in dirs if d not in ['backups', '__pycache__', '.git']]
            count += len(files)
        return count
    
    def _format_size(self, size_bytes):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def _cleanup_old_backups(self, max_backups=30):
        """Remove old backups to keep only the most recent ones"""
        backups = self.list_backups()
        
        if len(backups) > max_backups:
            old_backups = backups[max_backups:]
            for backup in old_backups:
                try:
                    os.remove(backup['path'])
                    self.logger.info(f"Removed old backup: {backup['filename']}")
                except Exception as e:
                    self.logger.warning(f"Failed to remove old backup {backup['filename']}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Portfolio Backup and Restore Utility')
    parser.add_argument('action', choices=['backup', 'restore', 'list'], 
                       help='Action to perform')
    parser.add_argument('--file', '-f', help='Backup file path (for restore)')
    parser.add_argument('--target', '-t', help='Target directory (for restore)')
    parser.add_argument('--include-logs', action='store_true', 
                       help='Include log files in backup')
    
    args = parser.parse_args()
    
    backup_manager = PortfolioBackup()
    
    try:
        if args.action == 'backup':
            backup_path = backup_manager.create_backup(include_logs=args.include_logs)
            print(f"✅ Backup created: {backup_path}")
            
        elif args.action == 'restore':
            if not args.file:
                print("❌ Error: --file argument required for restore")
                return 1
            
            restore_path = backup_manager.restore_backup(args.file, args.target)
            print(f"✅ Backup restored to: {restore_path}")
            
        elif args.action == 'list':
            backups = backup_manager.list_backups()
            if not backups:
                print("No backups found.")
                return 0
            
            print("Available backups:")
            print("-" * 80)
            for backup in backups:
                print(f"📦 {backup['filename']}")
                print(f"   Created: {backup['created']}")
                print(f"   Size: {backup['size']}")
                print()
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
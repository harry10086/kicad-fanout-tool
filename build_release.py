import os
import json
import shutil
import zipfile
import hashlib
from pathlib import Path

def get_version():
    with open('version.py', 'r') as f:
        for line in f:
            if line.startswith('version ='):
                return line.split('=')[1].strip().strip("'").strip('"')
    return '1.0.0'

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def build_release():
    version = get_version()
    print(f"Building release {version}")

    # Setup directories
    plugins_dir = Path('plugins')
    resources_dir = Path('resources')
    pcm_dir = Path('pcm')
    
    if plugins_dir.exists(): shutil.rmtree(plugins_dir)
    if resources_dir.exists(): shutil.rmtree(resources_dir)
    pcm_dir.mkdir(exist_ok=True)

    plugins_dir.mkdir()
    resources_dir.mkdir()

    # Copy files
    shutil.copy('icons/icon_64x64.png', resources_dir / 'icon.png')
    
    files_to_copy = ['icon.png', 'plugin.json', 'requirements.txt', 'package.json']
    for f in files_to_copy:
        shutil.copy(f, plugins_dir / f)
    
    # Copy all .py files
    for f in Path('.').glob('*.py'):
        shutil.copy(f, plugins_dir / f.name)
    
    # Copy preview folder
    shutil.copytree('preview', plugins_dir / 'preview', dirs_exist_ok=True)

    # First pass of metadata.json (without SHA/size)
    with open('metadata_template.json', 'r') as f:
        metadata_content = f.read()
    
    # We'll handle the final metadata after zipping
    
    # Zip package
    zip_name = f"fanout-tool-{version}.zip"
    zip_path = Path(zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in plugins_dir.rglob('*'):
            zipf.write(file, file.relative_to('.').relative_to(plugins_dir.parent)) # this is wrong
            # Wait, the build.sh does zip -r $name plugins resources metadata.json
            # So it should be:
            # plugins/...
            # resources/...
            # metadata.json
    
    # Let's rethink the zip structure to match build.sh:
    # zip -r $name plugins resources metadata.json
    
    # I'll use a temporary directory for zipping
    temp_build = Path('temp_build')
    if temp_build.exists(): shutil.rmtree(temp_build)
    temp_build.mkdir()
    
    shutil.copytree('plugins', temp_build / 'plugins')
    shutil.copytree('resources', temp_build / 'resources')
    
    # Create a temporary metadata.json for the zip
    with open('metadata_template.json', 'r') as f:
        content = f.read()
    
    # Use a dummy valid SHA256 for the initial internal metadata to pass schema validation
    # (64 zeros)
    internal_content = content.replace('VERSION', version)
    internal_content = internal_content.replace('SHA256', "0" * 64)
    internal_content = internal_content.replace('DOWNLOAD_SIZE', "0")
    internal_content = internal_content.replace('INSTALL_SIZE', "0")
    
    with open(temp_build / 'metadata.json', 'w') as f:
        f.write(internal_content)
        
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in temp_build.rglob('*'):
            zipf.write(file, file.relative_to(temp_build))
            
    # Calculate final values
    sha = calculate_sha256(zip_path)
    size = zip_path.stat().st_size
    
    # Install size is the unzipped size
    install_size = 0
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for info in zipf.infolist():
            install_size += info.file_size
            
    # Final metadata.json
    with open('metadata_template.json', 'r') as f:
        content = f.read()
    
    content = content.replace('VERSION', version)
    content = content.replace('SHA256', sha)
    content = content.replace('DOWNLOAD_SIZE', str(size))
    content = content.replace('INSTALL_SIZE', str(install_size))
    
    with open('metadata.json', 'w') as f:
        f.write(content)
        
    # Move zip to pcm/
    shutil.move(zip_path, pcm_dir / zip_name)
    
    # Cleanup
    shutil.rmtree(plugins_dir)
    shutil.rmtree(resources_dir)
    shutil.rmtree(temp_build)
    
    print(f"Successfully created {pcm_dir / zip_name} and metadata.json")

if __name__ == '__main__':
    build_release()

import os
import subprocess
import shutil
import tempfile

def detect_package_manager():
    """Detect the system's package manager."""
    if shutil.which('apt'):
        return 'apt'
    elif shutil.which('dnf'):
        return 'dnf'
    elif shutil.which('yum'):
        return 'yum'
    else:
        raise EnvironmentError("Unsupported package manager or not running on a supported Linux distribution.")

def list_installed_packages(package_manager):
    """List installed packages based on the package manager."""
    if package_manager == 'apt':
        cmd = ['dpkg-query', '-W', '-f=${Package} ${Version}\n']
    elif package_manager == 'dnf':
        cmd = ['dnf', 'list', 'installed']
    elif package_manager == 'yum':
        cmd = ['yum', 'list', 'installed']
    else:
        raise ValueError("Unsupported package manager.")

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Error listing packages: {result.stderr}")
    return result.stdout

def generate_sbom(package_list, output_file='sbom.json'):
    """Generate an SBOM using distro2sbom."""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(package_list.encode())
        temp_file_path = temp_file.name

    try:
        cmd = [
            'distro2sbom',
            '--input-file', temp_file_path,
            '--sbom', 'cyclonedx',
            '--output-file', output_file
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Error generating SBOM: {result.stderr}")
        print(f"SBOM generated successfully and saved to {output_file}")
    finally:
        os.remove(temp_file_path)

def main():
    try:
        package_manager = detect_package_manager()
        print(f"Detected package manager: {package_manager}")
        package_list = list_installed_packages(package_manager)
        generate_sbom(package_list)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

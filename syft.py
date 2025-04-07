import shutil
import subprocess
import sys


def detect_package_manager():
    """Detect the system's package manager (for logging purposes)."""
    if shutil.which('apt'):
        return 'apt'
    elif shutil.which('dnf'):
        return 'dnf'
    elif shutil.which('yum'):
        return 'yum'
    else:
        return 'unknown'


def check_syft_installed():
    """Ensure syft is installed and on the PATH."""
    if not shutil.which('syft'):
        print("Error: 'syft' not found in PATH. Please install syft from https://github.com/anchore/syft")
        sys.exit(1)


def generate_rich_sbom(output_file='sbom.json', output_format='cyclonedx-json', target_path='/'):
    """Use syft to scan the filesystem and generate a rich SBOM."""
    cmd = [
        'syft',
        f'dir:{target_path}',
        '--output',
        output_format
    ]

    try:
        with open(output_file, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Syft error: {result.stderr}")
        print(f"✅ Rich SBOM generated: {output_file}")
    except Exception as e:
        print(f"SBOM generation failed: {e}")
        sys.exit(1)


def main():
    check_syft_installed()
    pkg_manager = detect_package_manager()
    print(f"🔍 Detected package manager: {pkg_manager}")
    generate_rich_sbom()


if __name__ == '__main__':
    main()

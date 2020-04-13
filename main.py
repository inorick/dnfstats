import subprocess
import sys


def get_installed_packages():
    packages = subprocess.run(['rpm', '-qa'], text=True, stdout=subprocess.PIPE)
    packages = packages.stdout.split('\n')
    packages = [p.strip() for p in packages]
    return packages


def get_installed_groups():
    groups = subprocess.run(['dnf', 'group', 'list', '--hidden'], text=True, stdout=subprocess.PIPE)
    groups = groups.stdout.split('\n')
    groups = [g.strip() for g in groups]
    try:
        start = groups.index("Installed Groups:") + 1
        end = groups.index("Available Groups:")
    except ValueError:
        sys.exit("Error extracting installed groups")
    return groups[start: end]


def get_mandatory_and_default_packages(group):
    packages = subprocess.run(['dnf', 'group', 'info', '-v', group], text=True, stdout=subprocess.PIPE)
    packages = packages.stdout.split('\n')
    mandatory = []
    default = []
    try:
        start = packages.index(" Mandatory Packages:") + 1
        for p in packages[start:]:
            if not p.startswith('   '):
                break
            mandatory.append(p.strip().split(' ')[0])
    except ValueError:
        pass
    try:
        start = packages.index(" Default Packages:") + 1
        for p in packages[start:]:
            if not p.startswith('   '):
                break
            default.append(p.strip().split(' ')[0])
    except ValueError:
        pass
    return mandatory + default


if __name__ == '__main__':
    print("Getting list of installed groups")
    installed_groups = get_installed_groups()
    print("Getting package lists of installed groups")
    group_packages = []
    for group in installed_groups:
        for package in get_mandatory_and_default_packages(group):
            group_packages.append(package)
    print("Getting list of installed packages")
    installed_packages = get_installed_packages()

    print("Missing packages (part of group but not installed):")
    missing_packages = list(set(group_packages) - set(installed_packages))
    missing_packages.sort()
    for p in missing_packages:
        print(p)
    print()

    # print("Additional packages (part of group but not installed):")
    # additional_packages = list(set(installed_packages) - set(group_packages))
    # additional_packages.sort()
    # for p in additional_packages:
    #     print(p)

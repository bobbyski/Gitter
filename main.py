import argparse

def show_version(version):
    """Display the version information and exit."""
    print(f"Version {version}")
    exit(0)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# cli.add_command(show_version)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    show_version('0.0.1')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

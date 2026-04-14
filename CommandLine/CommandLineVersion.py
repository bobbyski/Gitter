from BusinessLogic.toml_helper import TomlHelper

def show_version(version):
    """Display the version information and exit."""
    version = TomlHelper().get_version()
    print(f"Version {version}")
    exit(0)
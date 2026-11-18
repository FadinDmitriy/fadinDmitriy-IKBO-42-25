import xml.etree.ElementTree as ET
from pathlib import Path


CONFIG_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "config.xml"
)


def main():
    """Прочитать XML-конфигурацию и вывести параметры."""
    tree = ET.parse(CONFIG_FILE)
    root = tree.getroot()

    fields = ("package", "repository", "test_mode", "filter")

    for field in fields:
        value = root.findtext(field, default="")
        print(f"{field}: {value}")


if __name__ == "__main__":
    main()

from urllib.parse import urlparse
import xml.etree.ElementTree as ET
from pathlib import Path
CONFIG_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "config.xml"
)

def get_required_text(root, field):
    """Получить обязательный параметр XML."""
    value = root.findtext(field)

    if value is None or not value.strip():
        raise ValueError(
            f"Обязательный параметр '{field}' не задан"
        )

    return value.strip()

def get_test_mode(root):
    """Проверить и вернуть режим тестирования."""
    value = get_required_text(root, "test_mode").lower()

    if value not in ("true", "false"):
        raise ValueError(
            "Параметр 'test_mode' должен быть true или false"
        )

    return value == "true"

def get_repository(root):
    """Проверить адрес репозитория или путь к файлу."""
    value = get_required_text(root, "repository")

    if get_test_mode(root):
        path = Path(value)

        if not path.is_absolute():
            path = CONFIG_FILE.parent.parent / path

        if not path.is_file():
            raise ValueError(
                "Файл тестового репозитория не найден"
            )
    else:
        parsed = urlparse(value)

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError(
                "Параметр 'repository' должен содержать URL http(s)"
            )

    return value

def get_filter(root):
    """Получить подстроку для фильтрации пакетов."""
    element = root.find("filter")

    if element is None:
        raise ValueError(
            "Параметр 'filter' отсутствует"
        )

    if len(element) > 0:
        raise ValueError(
            "Параметр 'filter' должен содержать только текст"
        )

    return (element.text or "").strip()

def main():
    """Прочитать XML-конфигурацию и вывести параметры."""
    tree = ET.parse(CONFIG_FILE)
    root = tree.getroot()

    if root.tag != "configuration":
        raise ValueError(
            "Корневой элемент XML должен называться 'configuration'"
        )

    fields = ("package", "repository", "test_mode", "filter")

    for field in fields:
        if field == "package":
            value = get_required_text(root, field)
        elif field == "repository":
            value = get_repository(root)
        elif field == "test_mode":
            value = str(get_test_mode(root)).lower()
        elif field == "filter":
            value = get_filter(root)
        else:
            value = root.findtext(field, default="")

        print(f"{field}: {value}")



if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Ошибка конфигурации: {error}")
        raise SystemExit(1) from None
    except ET.ParseError as error:
        print(f"Ошибка синтаксиса XML: {error}")
        raise SystemExit(1) from None
    except OSError as error:
        print(f"Ошибка чтения файла: {error}")
        raise SystemExit(1) from None

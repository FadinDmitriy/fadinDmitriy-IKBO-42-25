import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from src.main import (
    get_required_text,
    get_test_mode,
    get_filter,
    get_repository,
)


class TestConfiguration(unittest.TestCase):
    """Тесты параметров XML-конфигурации."""

    def test_valid_package(self):
        """Проверить правильное имя пакета."""
        root = ET.fromstring(
            "<configuration>"
            "<package>python3</package>"
            "</configuration>"
        )

        result = get_required_text(root, "package")

        self.assertEqual(result, "python3")

    def test_empty_package(self):
        """Проверить обработку пустого имени пакета."""
        root = ET.fromstring(
            "<configuration>"
            "<package></package>"
            "</configuration>"
        )

        with self.assertRaises(ValueError):
            get_required_text(root, "package")

    def test_valid_test_mode(self):
        """Проверить правильный режим тестирования."""
        root = ET.fromstring(
            "<configuration>"
            "<test_mode>true</test_mode>"
            "</configuration>"
        )

        result = get_test_mode(root)

        self.assertTrue(result)

    def test_invalid_test_mode(self):
        """Проверить неправильный режим тестирования."""
        root = ET.fromstring(
            "<configuration>"
            "<test_mode>hello</test_mode>"
            "</configuration>"
        )

        with self.assertRaises(ValueError):
            get_test_mode(root)

    def test_empty_filter(self):
        """Проверить допустимый пустой фильтр."""
        root = ET.fromstring(
            "<configuration>"
            "<filter></filter>"
            "</configuration>"
        )

        result = get_filter(root)

        self.assertEqual(result, "")

    def test_missing_filter(self):
        """Проверить отсутствие параметра filter."""
        root = ET.fromstring(
            "<configuration>"
            "</configuration>"
        )

        with self.assertRaises(ValueError):
            get_filter(root)

    def test_valid_repository(self):
        """Проверить правильный URL репозитория."""
        root = ET.fromstring(
            "<configuration>"
            "<repository>https://archive.ubuntu.com/ubuntu/</repository>"
            "<test_mode>false</test_mode>"
            "</configuration>"
        )

        result = get_repository(root)

        self.assertEqual(
            result,
            "https://archive.ubuntu.com/ubuntu/"
        )

    def test_invalid_repository(self):
        """Проверить неправильный URL репозитория."""
        root = ET.fromstring(
            "<configuration>"
            "<repository>not-a-link</repository>"
            "<test_mode>false</test_mode>"
            "</configuration>"
        )

        with self.assertRaises(ValueError):
            get_repository(root)

    def test_valid_test_repository(self):
        """Проверить путь к существующему тестовому файлу."""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "repository.txt"
            path.write_text(
                "A: B\nB:\n",
                encoding="utf-8"
            )

            root = ET.fromstring(
                "<configuration>"
                f"<repository>{path.as_posix()}</repository>"
                "<test_mode>true</test_mode>"
                "</configuration>"
            )

            result = get_repository(root)

            self.assertEqual(result, path.as_posix())

    def test_missing_test_repository(self):
        """Проверить отсутствие тестового файла."""
        root = ET.fromstring(
            "<configuration>"
            "<repository>config/not_existing_file.txt</repository>"
            "<test_mode>true</test_mode>"
            "</configuration>"
        )

        with self.assertRaises(ValueError):
            get_repository(root)


if __name__ == "__main__":
    unittest.main()

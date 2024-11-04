import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from the models folder."""
    package_dir = Path(__file__).resolve().parent / "models"  # Укажите путь к вашей папке с моделями

    if package_dir.exists() and package_dir.is_dir():
        # Получаем все модули в указанной папке
        modules = pkgutil.walk_packages(
            path=[str(package_dir)],
            prefix="app.db.models.",  # Убедитесь, что это соответствует вашей структуре пакетов
        )
        for module in modules:
            __import__(module.name)  # Импортируем модуль
import logging
import requests

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Офіційне API Нацбанку України (повертає JSON)
URL_API = (
    "https://bank.gov.ua"
)


def get_usd_rate() -> float:
    """Функція для отримання актуального курсу USD від НБУ."""
    try:
        logging.info("Надсилаємо запит до API НБУ...")
        response = requests.get(URL_API, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Шукаємо долар (USD) у списку валют
        usd_data = next(item for item in data if item["cc"] == "USD")

        logging.info(
            f"Успішно отримано курс: {usd_data['rate']} UAH за 1 USD"
        )
        return float(usd_data["rate"])

    except (requests.exceptions.RequestException, StopIteration) as e:
        logging.error(f"Помилка при отриманні даних: {e}")
        # Дефолтний курс на випадок, якщо пропав інтернет
        return 41.50


class CurrencyConverter:
    # Використовуємо slots для оптимізації пам'яті, як ти і хотів
    __slots__ = ("usd_rate",)

    def __init__(self, usd_rate: float) -> None:
        self.usd_rate = usd_rate

    def convert_to_uah(self, usd_amount: float) -> dict:
        """Конвертує долари в гривні та повертає словник із результатом."""
        uah_amount = round(usd_amount * self.usd_rate, 2)
        return {
            "usd": usd_amount,
            "rate": self.usd_rate,
            "result_uah": uah_amount,
        }

    def print_result(self, data: dict) -> None:
        """Виводить гарний результат у консоль."""
        print("\n--- Результат конвертації ---")
        print(f"Сума в USD: ${data['usd']}")
        print(f"Курс конвертації: {data['rate']} UAH")
        print(f"Ви отримаєте: {data['result_uah']} UAH")


# --- Головний блок програми ---
if __name__ == "__main__":
    # 1. Отримуємо курс із мережі
    current_rate = get_usd_rate()

    # 2. Ініціалізуємо наш конвертер
    converter = CurrencyConverter(usd_rate=current_rate)

    # 3. Запитуємо у користувача суму для обміну
    try:
        user_input = input(
            "\nВведіть суму в USD для конвертації в UAH: "
        )
        usd_to_exchange = float(user_input)

        # 4. Проводимо розрахунок та виводимо результат
        conversion_data = converter.convert_to_uah(usd_to_exchange)
        converter.print_result(conversion_data)

    except ValueError:
        print("Помилка: Будь ласка, введіть коректне число.")
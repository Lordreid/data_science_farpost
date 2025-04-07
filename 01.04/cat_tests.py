import pytest
from unittest.mock import Mock, patch
from cat_connect_example import CatFactProcessor, APIError

class TestCatFactProcessor:
    # Тест для успешного получения факта
    @patch("requests.get")
    def test_get_fact_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"fact": "Cats are cool"}
        mock_get.return_value = mock_response

        processor = CatFactProcessor()
        result = processor.get_fact()

        assert result == "Cats are cool"
        assert processor.facts == ["Cats are cool"]

    # Тест для ошибки API
    @patch("requests.get")
    def test_get_fact_api_error(self, mock_get):
        mock_get.side_effect = Exception("API broken")

        processor = CatFactProcessor()
        with pytest.raises(APIError) as exc:
            processor.get_fact()
        
        assert "API broken" in str(exc.value)

    # Тест длины факта при пустом списке
    def test_fact_length_empty(self):
        processor = CatFactProcessor()
        assert processor.get_fact_length() == 0

    # Тест длины последнего факта
    def test_fact_length_non_empty(self):
        processor = CatFactProcessor()
        processor.facts = ["Test", "Longer fact"]
        assert processor.get_fact_length() == 11

    # Тест статистики для пустого списка
    def test_stats_empty(self):
        processor = CatFactProcessor()
        assert processor.get_stats() == {"average": 0, "min": 0, "max": 0}

    # Тест статистики для данных
    def test_stats_with_values(self):
        processor = CatFactProcessor(num_facts=2)
        processor.facts = [
            "One",          # длина 3 (не войдет в выборку)
            "Two cats",     # длина 8
            "Three cats"    # длина 10
        ]
        
        stats = processor.get_stats()
        assert stats["average"] == 9.0
        assert stats["min"] == 8
        assert stats["max"] == 10
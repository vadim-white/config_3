import unittest
from io import StringIO
from main import *
class TestCustomLanguageParser(unittest.TestCase):
    def test_simple_constants(self):
        input_data = {"key1": 123, "key2": "value", "key3": [1, 2, 3]}
        expected_output = """set key1 = 123
set key2 = "value"
key3 = '( 1 2 3 )"""
        result = parse_toml_to_custom_lang(input_data)
        self.assertEqual(result, expected_output)

    def test_postfix_expression(self):
        input_data = {"key1": 10, "key2": ".[key1 20 +]."}
        expected_output = """set key1 = 10
set key2 = 30"""
        result = parse_toml_to_custom_lang(input_data)
        self.assertEqual(result, expected_output)

    def test_nested_arrays(self):
        input_data = {"array1": [1, 2, 3], "array2": [4, 5, 6]}
        expected_output = """array1 = '( 1 2 3 )
array2 = '( 4 5 6 )"""
        result = parse_toml_to_custom_lang(input_data)
        self.assertEqual(result, expected_output)

    def test_invalid_postfix_expression(self):
        input_data = {"key1": ".[10 20 &]."}
        with self.assertRaises(SystemExit):
            parse_toml_to_custom_lang(input_data)

if __name__ == "__main__":
    unittest.main()
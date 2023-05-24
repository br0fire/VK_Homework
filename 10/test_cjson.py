import unittest
import cjson


class JsonTestCase(unittest.TestCase):
    def test_json_load(self):
        # Test loading JSON with string keys and string values
        json_str = '{"key1": "value1", "key2": "value2"}'
        expected_result = {'key1': 'value1', 'key2': 'value2'}
        self.assertEqual(cjson.loads(json_str), expected_result)

        # Test loading JSON with string keys and integer values
        json_str = '{"key1": 1, "key2": 2}'
        expected_result = {'key1': 1, 'key2': 2}
        self.assertEqual(cjson.loads(json_str), expected_result)

        # Test loading JSON with multiple spaces
        json_str = '{"key1":    "value1",    "key2":   2   }'
        expected_result = {'key1': 'value1', 'key2': 2}
        self.assertEqual(cjson.loads(json_str), expected_result)

        # Test loading invalid JSON
        json_str = '{"key1" "value1", "key2": 2}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": "value1, "key2": 2}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": "value1" "key2": 2}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": "value1", "key2": }'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": ", "key2": 2}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": , "key2": 2}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '"key1": , "key2": 2}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": , "key2": 2'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": , "key2": 2}}}}}'

        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{{{{"key1": , "key2": 2}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = 'abab}'
        self.assertRaises(TypeError, cjson.loads, json_str)

        json_str = '{"key1": , "key2": [1, 3, 8]}'
        self.assertRaises(TypeError, cjson.loads, json_str)

    def test_json_dumps(self):
        # Test dumping dictionary with string keys and string values to JSON
        data = {'key1': 'value1', 'key2': 'value2'}
        expected_result = '{"key1": "value1", "key2": "value2"}'
        self.assertEqual(cjson.dumps(data), expected_result)

        # Test dumping dictionary with string keys and integer values to JSON
        data = {'key1': 1, 'key2': 2}
        expected_result = '{"key1": 1, "key2": 2}'
        self.assertEqual(cjson.dumps(data), expected_result)

        # Test loading invalid dictionary
        data = {'key1': 'a', 2: 2}
        self.assertRaises(TypeError, cjson.dumps, data)

        data = {'key1': (5, 6), 'key2': 2}
        self.assertRaises(TypeError, cjson.dumps, data)

        data = {'key1': 1, 'key2': {'key2': 'value'}}
        self.assertRaises(TypeError, cjson.dumps, data)


if __name__ == '__main__':
    unittest.main()

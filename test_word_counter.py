import unittest
import tempfile
import os
from main import WordFrequencyCounter, top_words_from_file


class TestWordFrequencyCounter(unittest.TestCase):
    def setUp(self):
        self.counter = WordFrequencyCounter(case_sensitive=False)
        
    def test_specific_example(self):
        test_text = "Go do that thing that you do so well"
        expected_counts = {
            "go": 1,
            "do": 2,
            "that": 2,
            "thing": 1,
            "you": 1,
            "so": 1,
            "well": 1
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_text)
            temp_file_path = temp_file.name
        
        try:
            result = self.counter.count_from_file(temp_file_path)
            
            for word, expected_count in expected_counts.items():
                self.assertEqual(result[word], expected_count, 
                               f"Word '{word}' should have count {expected_count}, but got {result.get(word, 0)}")
            
            self.assertEqual(len(result), len(expected_counts), 
                           f"Expected {len(expected_counts)} unique words, but got {len(result)}")
            
        finally:
            os.unlink(temp_file_path)
    
    def test_top_words_from_file_function(self):
        test_text = "Go do that thing that you do so well"
        expected_result = [
            ("do", 2),
            ("that", 2),
            ("go", 1),
            ("thing", 1),
            ("you", 1),
            ("so", 1),
            ("well", 1)
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_text)
            temp_file_path = temp_file.name
        
        try:
            result = top_words_from_file(temp_file_path)
            
            for expected_word, expected_count in expected_result:
                self.assertIn((expected_word, expected_count), result,
                             f"Expected pair ('{expected_word}', {expected_count}) not found in result")
            
            self.assertEqual(len(result), len(expected_result),
                           f"Expected {len(expected_result)} word-count pairs, but got {len(result)}")
            
        finally:
            os.unlink(temp_file_path)
    
    def test_case_insensitive(self):
        test_text = "Go GO go Go"
        expected_count = 4
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_text)
            temp_file_path = temp_file.name
        
        try:
            result = self.counter.count_from_file(temp_file_path)
            self.assertEqual(result["go"], expected_count,
                           f"Word 'go' should have count {expected_count} (case insensitive), but got {result.get('go', 0)}")
        finally:
            os.unlink(temp_file_path)
    
    def test_case_sensitive(self):
        test_text = "Go GO go Go"
        counter_sensitive = WordFrequencyCounter(case_sensitive=True)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(test_text)
            temp_file_path = temp_file.name
        
        try:
            result = counter_sensitive.count_from_file(temp_file_path)
            self.assertEqual(result["Go"], 2, "Case sensitive 'Go' should have count 2")
            self.assertEqual(result["GO"], 1, "Case sensitive 'GO' should have count 1")
            self.assertEqual(result["go"], 1, "Case sensitive 'go' should have count 1")
        finally:
            os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()

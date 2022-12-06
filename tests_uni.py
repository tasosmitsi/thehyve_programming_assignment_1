import unittest
import hyve_test


class Tests(unittest.TestCase):
    def test_is_correct(self):
      
        data = [0, 61, 0]
        result = hyve_test.sequence.is_correct(self, *data)
        self.assertEqual(result, True)



if __name__ == '__main__':
    
    unittest.main()
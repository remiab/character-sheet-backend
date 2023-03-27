from unittest import TestCase, main
from spell_caster import check_int

class TestCheckInt(TestCase):

    def test_strings(self):
        expected = False
        result = check_int(input_val="no")
        self.assertEqual(expected, result)
    
    def test_OO_range(self):
        expected = False
        result = check_int(input_val= "50")
        self.assertEqual(expected, result)

if __name__=="__main__":
    main()

TestCheckInt()
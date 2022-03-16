import sunnyhills 

class TestAutotesting:

    def test_addition(self):
        assert 4 == 4
    
    def test_basic(self): 
        assert 2 == sunnyhills.basic.get_two()

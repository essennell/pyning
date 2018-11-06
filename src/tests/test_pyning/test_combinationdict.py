from pyning.combinationdict import CombinationDict


def test_key_at_root_is_located():
    items = CombinationDict( '/', { 'a': 10 } )
    assert items[ 'a' ] == 10


if __name__ == '__main__':
    pass

from pyning.combinationdict import CombinationDict

import pytest


def test_key_at_root_is_located():
    items = CombinationDict( '/', { 'a': 10 } )
    assert items[ 'a' ] == 10


def test_key_nested_1_level_is_located():
    items = CombinationDict( '/', { 'a': { 'b': 10 } } )
    assert items[ 'a/b' ] == 10


def test_escaped_separator_is_used_as_direct_key():
    items = CombinationDict( '.', { 'a': { 'b\\.c': { 'd': 10 } } } )
    assert items[ 'a.b\\.c.d' ] == 10


def test_nested_value_can_be_updated():
    items = CombinationDict( '.', { 'a': { 'b': { 'c': 10 } } } )
    items[ 'a.b.c' ] = 100
    assert items[ 'a' ][ 'b' ][ 'c' ] == 100


def test_item_value_can_be_a_list():
    items = CombinationDict( '.', { 'a': [ 1, 2 ] } )
    assert items[ 'a' ][ 0 ] == 1


def test_nested_item_can_be_a_list():
    items = CombinationDict( '.', { 'a': { 'b': [ 1, 2 ] } } )
    assert items[ 'a.b' ][ 0 ] == 1


def test_nested_dict_can_be_updated():
    items = CombinationDict( '.', { 'a': { 'b': 10, 'c': 20 } } )
    items.update( { 'a': { 'b': 100 } } )
    assert items[ 'a.b' ] == 100
    assert items[ 'a.c' ] == 20


def test_nested_dict_can_be_updated_from_tuple():
    items = CombinationDict( '.', { 'a': { 'b': 10 } } )
    items[ 'a' ].update( [ ( 'c', 100 ), ( 'e', 1 ) ] )
    assert items[ 'a.c' ] == 100
    assert items[ 'a.e' ] == 1


def test_update_respects_nesting_notation():
    items = CombinationDict( '.', { 'a': { 'b': 10 } } )
    items.update( { 'a.b': 100 } )
    assert items[ 'a' ][ 'b' ] == items[ 'a.b' ]
    assert 'a.b' not in set( items.keys() )


def test_separator_for_nesting_can_be_escaped():
    items = CombinationDict( '.', { 'a': { 'b': 10 } } )
    items[ r'a\.b' ] = 100
    assert items[ 'a.b' ] == 10


if __name__ == '__main__':
    pytest.main()

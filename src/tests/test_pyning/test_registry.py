from pyning.config import Registry

import pytest


def test_no_variables_gives_literal_results():
    args = { 'a': '10', 'b': '20' }
    a = Registry().add( args ).resolve()
    assert a[ 'a' ] == '10'


def test_simple_element_substitution_replaces_whole_expression():
    args = { 'foo': 'hello', 'bar': '${foo}' }
    cfg = Registry().add( args ).resolve()
    assert cfg[ 'bar' ] == args[ 'foo' ]


def test_expression_can_be_further_expression():
    args = { 'foo': '${bar}', 'bar': '${bing}', 'bing': 'hello' }
    cfg = Registry().add( args ).resolve()
    assert cfg[ 'foo' ] == args[ 'bing' ]


def test_expression_cannot_be_recursive():
    args = { 'foo': '${foo}' }
    cfg = Registry().add( args )
    with pytest.raises( Exception ):
        cfg.resolve()


def test_expression_cannot_be_reflective():
    args = { 'foo': '${bar}', 'bar': '${foo}' }
    cfg = Registry().add( args )
    with pytest.raises( Exception ):
        cfg.resolve()


def test_expression_cannot_be_indirectly_recursive():
    args = { 'foo': '${bar}', 'bar': '${bing}', 'bing': '${baz}', 'baz': '${foo}' }
    cfg = Registry().add( args )
    with pytest.raises( Exception ):
        cfg.resolve()


def test_handlers_are_processed_in_order_of_addition():
    first = { 'a': 100 }
    second = { 'a': 200 }
    assert Registry().add( first ).add( second ).resolve()[ 'a' ] == 200


def test_keys_in_later_handlers_are_added():
    first = { 'a': 100 }
    second = { 'b': 200 }
    assert Registry().add( first ).add( second ).resolve()[ 'b' ] == 200


def test_variables_can_refer_to_keys_in_later_handlers():
    first = { 'a': '${b}' }
    second = { 'b': 'hello' }
    assert Registry().add( first ).add( second ).resolve()[ 'a' ] == second[ 'b' ]


def test_variables_are_substituted_from_earlier_handlers():
    first = { 'a': 'hello' }
    second = { 'b': '${a}' }
    assert Registry().add( first ).add( second ).resolve()[ 'b' ] == first[ 'a' ]


def test_value_can_contain_multiple_substitutions():
    args = { 'foo': 'The ${bar} is ${bing}ed', 'bar': 'test', 'bing': 'pass' }
    assert Registry().add( args ).resolve()[ 'foo' ] == 'The test is passed'


def test_variable_with_unknown_key_remains_unchanged():
    args = { 'foo': '${bar}' }
    assert Registry().add( args ).resolve()[ 'foo' ] == '${bar}'


def test_nonstring_values_remain_unchanged():
    args = { 'foo': 100 }
    assert Registry().add( args ).resolve()[ 'foo' ] == 100


def test_value_can_be_unset():
    args = { 'foo': None }
    assert Registry().add( args ).resolve()[ 'foo' ] == None


def test_all_items_in_a_list_are_resolved():
    args = { 'foo': 'hello', 'bar': '10', 'bing': [ 'Yes', '${bar}', '${foo}' ] }
    cfg = Registry().add( args ).resolve()
    assert cfg[ 'bing' ][ 1 ] == args[ 'bar' ]
    assert cfg[ 'bing' ][ 2 ] == args[ 'foo' ]


def test_substituted_value_can_be_nonstring_and_is_converted_to_string():
    args = { 'foo': 10, 'bar': '${foo}' }
    assert Registry().add( args ).resolve()[ 'bar' ] == str( args[ 'foo' ] )


def test_nested_substitutions_are_resolved():
    args = { 'foo': { 'bar': '${bing}' }, 'bing': 'hello' }
    assert Registry().add( args ).resolve()[ 'foo.bar' ] == args[ 'bing' ]


def test_substitutions_are_resolved_from_nested_keys():
    args = { 'foo': { 'bar': 'hello' }, 'bing': '${foo.bar}' }
    assert Registry().add( args ).resolve()[ 'bing' ] == args[ 'foo' ][ 'bar' ]


def test_substitutions_with_escaped_separator_resolves_to_correct_key():
    args = { 'foo': { 'bar\\.bing': 'hello' }, 'baz': { 'fart': '${foo.bar\\.bing}' } }
    assert Registry().add( args ).resolve()[ 'baz.fart' ] == 'hello'


def test_nest_dict_can_be_a_list():
    args = { 'foo': { 'baz': [ 5, 50 ] }, 'bar': '${foo}' }
    assert Registry().add( args ).resolve()[ 'foo.baz' ][ 1 ] == 50


def test_nest_dict_is_updated_by_added_handler():
    first = { 'a': { 'b': 10, 'c': 20 } }
    second = { 'a': { 'c': 200, 'd': 1000 } }
    assert Registry().add( first ).add( second ).resolve()[ 'a.b' ] == 10
    assert Registry().add( first ).add( second ).resolve()[ 'a.c' ] == 200
    assert Registry().add( first ).add( second ).resolve()[ 'a.d' ] == 1000


def test_resolved_registry_is_a_dictionary():
    first = { 'a': { 'b': '${a.d}', 'c': '1' } }
    second = { 'a': { 'c': '${a.b}_here', 'd': 'hello' } }
    cfg = Registry().add( first ).add( second ).resolve()
    assert cfg[ 'a.b' ] == 'hello'
    assert cfg[ 'a.c' ] == 'hello_here'


if __name__ == '__main__':
    pytest.main()

    import json

    args = { 'url': '${remotes.endpoint}' }
    overrides = json.loads( '''
        { "remotes": {
            "endpoint": "http://nowhere"
        } } '''
                            )

    cfg = Registry().add( args ).add( overrides ).resolve()
    print( cfg[ 'url' ] )


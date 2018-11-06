from .combinationdict import CombinationDict as cdict

from collections import Mapping
import re


def _substitute_params( marker, all_keys, v ):
    match = marker.search( v )
    seen = set()
    while match:
        sub, key = match.groups()[ 0 ], match.groups()[ 1 ]
        if key in seen:
            raise Exception( key )
        seen.add( key )
        if key in all_keys:
            v = re.sub( re.escape( sub ), str( all_keys[ key ] ), v )
            match = marker.search( v )
        else:
            match = None
    return v


def _identify_item( marker, all_keys, v ):
    if isinstance( v, str ):
        return _substitute_params( marker, all_keys, v )
    elif isinstance( v, list ):
        return [ _identify_item( marker, all_keys, i ) for i in v ]
    else:
        return v


def _resolve( marker, all_keys, src ):
    result = src.copy()
    for k, v in src.items():
        if isinstance( v, Mapping ):
            result[ k ] = _resolve( marker, all_keys, v )
        else:
            result[ k ] = _identify_item( marker, all_keys, v )
    return result


class Registry:
    def __init__( self, separator='.', marker=r'(\$\{(.*?)\})' ):
        self.handlers = []
        self.data = cdict( separator )
        self.marker_pattern = re.compile( marker )

    def add( self, handler ):
        self.handlers.append( handler )
        self.data.update( handler )
        return self

    def resolve( self ):
        return _resolve( self.marker_pattern, self.data, self.data )

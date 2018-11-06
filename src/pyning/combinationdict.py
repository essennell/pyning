from collections import UserDict, Mapping
import re


class CombinationDict( UserDict ):
    def __init__( self, separator, content=None, **kwargs ):
        self.separator = separator
        self.key_pattern = re.compile( rf'(?<!\\){re.escape(self.separator)}' )
        UserDict.__init__( self, content, **kwargs )

    def _locate( self, key ):
        res = self.data
        for k in key:
            if k not in res:
                return None
            res = res[ k ]
        return res

    def update( *args, **kwargs ):
        self, other, *args = args
        for k, v in other.items():
            if k in self.data and isinstance( v, Mapping ):
                self[ k ].update( v )
            else:
                self[ k ] = v
        return self

    def copy( self ):
        return CombinationDict( self.separator, self.data )

    def __getitem__( self, key ):
        return self._locate( self.key_pattern.split( key ) )

    def __setitem__( self, key, value ):
        key = self.key_pattern.split( key )
        res = self._locate( key[ :-1 ] )
        res[ key[ -1 ] ] = value

    def __contains__( self, key ):
        return self._locate( self.key_pattern.split( key ) )
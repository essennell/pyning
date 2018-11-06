# Pyning
## A quick and extensible configuration management library

Pyning lets you take configuration entries in key/value pairs, 
and query by key. For example, you might just use a dict (or any 
Mapping type):

```python
args = { 'stop-on-error': True }
registry = pyning.config.Registry()
config = registry.add( args ).resolve()

print( config[ 'stop-on-error' ] )
# True
```

Multiple levels of handler are possible, with later handlers 
override same-key settings in earlier handlers. 

```python
args = { 'stop-on-error': True }
overrides = { 'stop-on-error': False }
registry = pyning.config.Registry()
config = registry.add( args ).add( overrides ).resolve()

print( config[ 'stop-on-error' ] )
# False
```

You might use this to have some configuration in a file, and
override with the argparse.ArgumentParser values.

```python
args = { 'stop-on-error': True }
parser = ArgumentParser().add_argument( '--stop-on-error' )
cmdline = parser.parse_args()
registry = pyning.config.Registry()
config = registry.add( args ).add( vars( cmdline ).resolve()

print( config[ 'stop-on-error' ] )
# False
```

Values can use a limited variable substitution to swap in 
values from different keys. This is especially useful when
using the overrides feature. At present, it only works for strings.

```python
public_args = { 'password': '${private_password}' }
overrides = { 'private_password': 'a good strong password' }
registry = pyning.config.Registry()
config = registry.add( args ).add( overrides ).resolve()

print( config[ 'password' ] )
# a good strong password
```

Values don't have to be single items: they can be sequences or
even nested Mapping objects. A convenient short-hand can be used
to refer to nested keys, and works with variable substitution,
too.

```python
    import json

    args = { 'url': '${remotes.endpoint}' }
    overrides = json.loads( '''
        { "remotes": {
            "endpoint": "http://nowhere"
        } } '''
                            )

    cfg = Registry().add( args ).add( overrides ).resolve()
    print( cfg[ 'url' ] )

```


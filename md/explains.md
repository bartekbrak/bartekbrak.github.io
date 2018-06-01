# Bartek explains

I get asked about technical problems. Often it is possible to answer using sample code. Rather
than sending the samples to those who ask, I will publish them here so I can reference them when 
asked again for the same stuff.

### An example of monkey-patching

```
class StupidClass:
    def stupid_method(self, some_arg):
        print("this method is stupid, we want to replace it")

def good_function(some_arg):
    print("this method is clever, it replaces the other one")

sc = StupidClass()
sc.stupid_method('whatever')
# monkey patch now
sc.__some_name = sc.stupid_method
sc.stupid_method = good_function
sc.stupid_method('whatever')
# and back, not always needed
sc.stupid_method = sc.__some_name
```

out
```
this method is stupid, we want to replace it
this method is clever, it replaces the other one
``` 

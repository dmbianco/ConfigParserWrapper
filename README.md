# ConfigParserWrapper
### A wrapper for Python class ConfigParser


The intent of this class is to provide additional functionalities to the ConfigParser
class. In particular, it can infer the type of the pickled variables.
Only a bunch of types are supported (str, int, float, dict, bool), but they can easily
extended (give a look at the dictionary *types* into the class definition).

## Usage

An instance of ConfigParserWrapper can be initialized with the constructor of the class. It only requires a dict that should have a structure similar to the following:
```
dict = { "section1":{"var1":"val1", "var2":"val2"},
         "section2":{"varA":"valA", "varB":"valB"}
        }
```
Alternatively, a *section* (using the jargon of ConfigParser) can be added thanks to the method 
```
add_section_dict(dic_of_variables, section_name, check_section=True)
```

The easiest way to use this class is through the method *add_section_dict*. Then one calls the method *save_config* to save all the variables. Finally, one can restore the variables and the associated values (hopefully with the correct types) with *load_config*.










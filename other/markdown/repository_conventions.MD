# The Repository Conventions Compact

## Code
### Python
* **Styling**: please follow the Google Python Style Guide as default for general syntactic decisions. This can be accessed [here](https://google.github.io/styleguide/pyguide.html#316-naming). Here's a summary: 
    * Use tabs instead of spaces for indentation, with four space equivalency 
    * ```module_name```, ```package_name```, ```ClassName```, ```method_name```, ```ExceptionName```, ```function_name```, ```GLOBAL_CONSTANT_NAME```, ```global_var_name```, ```instance_var_name```, ```function_parameter_name```, ```local_var_name```, etc. 
    * Please keep names short but informative. If you need to describe things beyond the variable name, leave a comment next to it (we don't want gargantuan variable names)

### General Repository Things
* Plese initialize new directories with ```.gitkeep``` files 
* Keep plot sets under ```./plots``` rather than ```./data```

## Workflow
* Please confirm with everybody in the group before making major changes that affect everyone else (e.g. changing commonly used functions drastically, changing file/path names along highly trafficked paths, changing data file headers, etc. 
* Dealing with meta data: if single row value per object, keep in the current single metadata file (in which each row contains data for a different object with however many columns of information)...otherwise, e.g. TLS (depth, period, etc.), store in separate files within a sub-directory of results. 


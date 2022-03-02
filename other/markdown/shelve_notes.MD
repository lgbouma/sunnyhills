# Notes on shelve

## Shelve Opening Flag Meanings

| Value      | Meaning |
| ----------- | ------------------- |
| `'r'` | Open existing database for reading only (default)|
| `'w'` | Open existing database for reading and writing |
| `'c'` | Open database for reading and writing, creating it if it doesn’t exist |
| `'n'`| Always create a new, empty database, open for reading and writing |

## Operation Notes
* Open new shelve file: 
```python 
with shelve.open(file_name, "c") as shelf:
        shelf['shelf_name'] = example_dictionary
```

* Open with read write capabilities shelve file that already exists, and delete a dictionary within it: 
```python
with shelve.open(file_name, 'w') as shelf:
    if 'example_key' in shelf: 
        del shelf['example_key']
```

* Open shelve file, print key, and read dictionaries within it: 
```python
with shelve.open(file_name, 'r') as shelf:
    print(list(shelf.keys()))

    example_dictionary = shelf['example_name']
```



## Other Notes
* A “shelf” is a persistent, dictionary-like object
* The difference with “dbm” databases is that the values (not the keys!) in a shelf can be essentially arbitrary Python objects — anything that the pickle module can handle.
* The shelve allows you to store pickled objects ... in a perseistent manner. It is useful to store large amount of data because Python performs *shelf lookups as needed* instead of loading the entire shelf in memory.

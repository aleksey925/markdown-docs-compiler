# Оглавление

1. Программирование
    - [Чистый код](clean-code/clean-code-index.md)
    - [Computer Science](computer-science/computer-science-index.md)

# Таблица

Column1 |   Column2
--------|-------------
val1    | val3, val4
val2    | val5


- [Реализация dict в CPython](#Реализация-dict-в-CPython)

<a name='Реализация-dict-в-CPython'></a>
#### dict в CPython

```с
typedef struct {
    Py_hash_t me_hash;
    PyObject *me_key;
    PyObject *me_value;
} PyDictKeyEntry;
```

```python
entries = [['--', '--', '--'],
           [-8522787127447073495, 'barry', 'green'],
           ['--', '--', '--'],
           ['--', '--', '--'],
           ['--', '--', '--'],
           [-9092791511155847987, 'timmy', 'red'],
           ['--', '--', '--'],
           [-6480567542315338377, 'guido', 'blue']]
```

<details markdown="span">
    <summary>Show slides</summary>

![](python-notes-index/dict/impl-dict-in-cpython/add-new-element-1.jpg)
![](python-notes-index/dict/impl-dict-in-cpython/add-new-element-2.jpg)

</details>

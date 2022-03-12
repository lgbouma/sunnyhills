# notes

## pipenv 
* tried doing it from scratch in pipenv...everything went smoothly until importing transitleastsquares. It said ```from . import _nonlinear_ld ImportError: numpy.core.multiarray failed to import```
    * possible solution: [https://github.com/tensorflow/tensorflow/issues/559](https://github.com/tensorflow/tensorflow/issues/559)
    * perhaps we just work in an old dir to download everything and then move to new one to use numba? 
    * my big question is, why does it work in google collab but not locally? perhaps I should pip list everything in google collab, set those as requirements, and setup a virtualenv accordingly? 
* after upgrading numpy, which seemed like the internet recommended solution, numba wouldn't work anymore because numba needs numpy <= 1.22 >1.8 (off of memory)

### virtualenv <3.9 python attempt
* going to use virtualenv to make < 3.9 version python attempt (starting with python 3.8)

* first made new virtual environment with python3.8 via virtualenv: ```py -m virtualenv -p="C:\Users\Research\AppData\Local\Programs\Python\Python38\python.exe" "C:\Users\Research\.virtualenvs\trying_again\.virtenv"```
* Then ran this script in terminal:  ```C:\Users\Research\.virtualenvs\trying_again\.virtenv\Scripts\activate.bat```
* Then ran this: ```C:\Users\Research\.virtualenvs\trying_again\.virtenv\Scripts\python.exe -m pip install numpy==1.21.5```
* this website was helpful: ```https://www.roelpeters.be/virtualenv-venv-choose-python-version/```
* also helpful: ```https://docs.python-guide.org/dev/virtualenvs/``` 
* batman has so many dependencies SMH 

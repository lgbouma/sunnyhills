# notes

## pipenv 
* tried doing it from scratch in pipenv...everything went smoothly until importing transitleastsquares. It said ```from . import _nonlinear_ld ImportError: numpy.core.multiarray failed to import```
    * possible solution: [https://github.com/tensorflow/tensorflow/issues/559](https://github.com/tensorflow/tensorflow/issues/559)
    * perhaps we just work in an old dir to download everything and then move to new one to use numba? 
    * my big question is, why does it work in google collab but not locally? perhaps I should pip list everything in google collab, set those as requirements, and setup a virtualenv accordingly? 
* after upgrading numpy, which seemed like the internet recommended solution, numba wouldn't work anymore because numba needs numpy <= 1.22 >1.8 (off of memory)
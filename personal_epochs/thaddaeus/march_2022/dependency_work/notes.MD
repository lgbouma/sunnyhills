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
* then i did the same thing but installed astropy, lightkurve, wotan, transitleastsquares, matplotlib, seaborn, and pandas 
* Then I went to view-->command pallet--> select python interpreter --> enter interpreter path --> into which I pasted the path to the python.exe file from the venv I made 
* this website was helpful: ```https://www.roelpeters.be/virtualenv-venv-choose-python-version/```
* also helpful: ```https://docs.python-guide.org/dev/virtualenvs/``` 
* batman has so many dependencies SMH 
* Okay so unfortunately, TLS is *still* not working, despite the python3.8 download. Here's my new solution: I will make two shhs_hrl environments: one for wotan work, and one for tls_work. SMH THIS IS ANNOYING

* I am going to use the requirements.txt approach. 
    * once you've installed all the packages, do ```pip freeze > requirements.txt```
    * to install python packages according to requirements.txt file, do ```pip install -r requirements.txt```
        * note that all of these pip's should probably have the prefix of the venv path like you see in the code above
        * I'll make a dir with requirements for each new venv 
* this [article](https://stackoverflow.com/questions/43256369/how-to-rename-a-virtualenv-in-python) was helpful 
* this other [article](https://www.akamai.com/blog/developers/how-building-virtual-python-environment) also seemed helpful 

* recall that python version is 3.8

* okay tls kinda making me want to die ... I split wotan and tls into two different libraries but tls still won't work AHAHAHAHHAAHHAHAHAHAHAHA

** big picture ** 

    * it's kinda depressing how much time I spent trying to get all this dependency stuff working out...what are some lessons I can take from this experience to avoid it in the future? I think the chief lesson I'm taking away is that the first thing you should do in this experience is determine which modules are in conflict, and make separate virtual envs for them. Also have other stuff to do when you do this kind of stuff...it's mad annoying. Finally, when you have something that works use it (e.g. just use tls for colab for now on, stop trying to fix it for windows )
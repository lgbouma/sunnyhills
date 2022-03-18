# working install guide

1. Download [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) (and despite the warning the installed gives, make sure to select the "Add Anaconda to my PATH enviroment variable``` option) 
2. From Anaconda Prompt (miniconda3)<sup>1</sup>, execute ```conda create --name py37 python=3.7```
3. Execute ```conda activate py37```
4. Execute ```conda install astropy h5py beautifulsoup4 html5lib bleach pyyaml pandas sortedcontainers pytz setuptools mpmath bottleneck ipython pip```
5. Execute ```pip install -U transitleastsquares```
6. Execute ```pip install -U wotan```
7. ```cd``` into the top level ```sunnyhills``` directory on your machine within the conda prompt (for me this is ```cd Documents``` then ```cd GitHub``` then ```cd sunnyhills```)
8. Execute the command ```conda install conda-build```
9. Execute ```conda develop .```
10. Execute ```pip install -e .```
    * Note that if you ever want to *uninstall* the sunnyhills repo, you can use ```pip uninstall .``` or ```conda develop -u .```
11. To start using this environment in VSCode, go to ```view``` then ```command palette``` then ```Python: Select Interpreter``` then click ```Enter interpreter path...``` then enter the path to the ```python.exe``` file within the environment folder oft this enviroment you just made. For me, this is something like ```C:\Users\Research\miniconda3\envs\py37\python.exe``` (note that you can find the environment under ```envs``` under ```miniconda3```)

Finally, you should now be able to use everything in this perfectly working environment! 

[1] I recommend pinning the Anaconda Prompt to your taskbar once you find it (for me it's located around ```C:\Users\Research\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)\Anaconda Prompt (miniconda3).lnk```). I wouldn't use the Anaconda Powershell Prompt because I didn't test this approach on it. 
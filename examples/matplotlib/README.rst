Matplotlib + PyPy Example
=========================

* wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.3.1-linux_x86_64-portable.tar.bz2
* tar -xf pypy-2.3.1-linux_x86_64-portable.tar.bz2 
* ./pypy-2.3.1-linux_x86_64-portable/bin/virtualenv-pypy venv
* source venv/bin/activate
* pip install git+https://bitbucket.org/pypy/numpy.git
* pip install git+https://github.com/mattip/matplotlib.git
* pip install pgi
* pip install cairocffi
* python --version
* python matplotlib_example.py

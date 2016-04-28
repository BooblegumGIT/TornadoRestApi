# REST-API server
Делаем собственный мини-фрэймворк с использованием:

* Tornado
* MongoDB (motor)
* Models (schematics)

### Run
<pre class="code">
    # apt-get install python3-pip
    # pip3 install > requirements.txt
    $ python3 app.py
</pre>

### Build docs
*Не реализовано*

<pre class="code">
    $ hg clone https://bitbucket.org/birkenfeld/sphinx-contrib
    $ cd sphinx-contrib/httpdomain
    $ python setup.py build
    # python setup.py install
    $ cd docs
    $ make html
</pre>

[MD GitHub syntax] (https://help.github.com/articles/basic-writing-and-formatting-syntax/)
linkchecker
===========

#### Buliding from Source

OS X

```
$ brew update
$ brew doctor

$ brew install pyqt
$ brew info pyqt

$ brew install gettext
$ brew link --force gettext
$ pip install --upgrade pytest
$ pip install --upgrade requests

$ make localbuild

$ ./linkchecker-gui
```

Ubuntu

```
apt-get install -y flex git python-pip
pip install --upgrade requests
apt-get build-dep -y linkchecker

git clone https://github.com/wummel/linkchecker.git
cd linkchecker

make localbuild
```

#### Example usage

> nohup ./linkchecker -q -F html/utf8/checked.html -r -1 --check-extern http://example.com/ >/dev/null 2>&1 &

#### Subdomains

[internlinks](http://wummel.github.io/linkchecker/man5/linkcheckerrc.5.html) is available only via config file. The command line doesn't support it.

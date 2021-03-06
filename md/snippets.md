# Notes

This is a collection of snippets and little things I discovered that might
come handy one day. All conveniently put together on one page to make searching
easy.

## ipython style bash history

```
bind '"\e[A": history-search-backward';bind '"\e[B": history-search-forward'
```

## Hot to scan using Mustek 1200 Ub PLus

```
# root
/usr/share/sane/gt68xx
wget http://www.meier-geinitz.de/sane/gt68xx-backend/firmware/sbfw.usb

sed -i.backup -e 's/^#override "mustek-scanexpress-1200-ub-plus"/override "mustek-scanexpress-1200-ub-plus"/' /etc/sane.d/gt68xx.conf

# user
# Re-plug USB cable connecting the scanner
simple-scan
```

## add user to group

```
usermod -a -G users bartek
```

_I have looked up this particular snippet way too many times_

## Remove hrefs, useful for trans_now

```
var anchors = document.getElementsByTagName("a");
for (var i = 0; i < anchors.length; i++) {
    var elem = anchors[i];
    elem.onclick = function() {return(false);};
    console.log(elem.href, 'removed');
    elem.removeAttribute("href");
}
```

bookmarklet <a href="javascript:var anchors = document.getElementsByTagName('a'); for (var i = 0; i < anchors.length; i++) {var elem = anchors[i]; elem.onclick = function() {return(false);}; console.log(elem.href, 'removed'); elem.removeAttribute('href'); }">rm hrefs</a>
## Follow logs of a systemd service

```
journalctl -fu NetworkManager.service
```

## Fix torrent files

```
sudo sed -i "s, %U, '%U'," /usr/share/applications/transmission-qt.desktop
xdg-mime default transmission-qt.desktop x-scheme-handler/magnet
```

## Tag flac/mp3 files

`sudo apt-get install easytag`


## useradd or adduser

adduser

## Install newest Mercurial on Ubuntu 14.04, system wide, with thg.

```
$ hg version
Mercurial Distributed SCM (version 2.8.2)
$ sudo apt-add-repository ppa:mercurial-ppa/releases
$ apt update
$ apt upgrade # will remove thg as it is not compatible
$ hg version
Mercurial Distributed SCM (version 3.8.4)
# There is no PPA for thg
$ hg clone https://bitbucket.org/tortoisehg/thg ~/opt/tortoisehg
$ ln -s ~/opt/tortoisehg/thg ~/bin
# it sometimes just works, maybe Qt4 is required.
```


## In django, context is shared between included templates.

When `{% include "child_template.html "%}` is used the parent template context
is available inside the child template. This sucks. When you have many templates included you will 
have to be carefyul with clenaing the context.

```
# context
c = {
    'a': 'a value',
    'b': 'b value'
}

# parent.html
Parent: {{ a }}
<br>
{% include "child.html" %}

# child.html
Child: {{ b }}

# Rendered:
Parent: a value
<br>
Child: b value
```

### Now is, context created inside a template shared as well? 

The first sentence od [Built-in template tags and filters/include](https://docs.djangoproject.com/en/1.9/ref/templates/builtins/#include)
says it does but let's see for ourselves:

> Loads a template and renders it *with* the current context.

```
from django.template import Template, Context
outer = '''
{{a}} 
{% with "the_b" as b%}
    {% include included %}
{% endwith %}
'''
inner = '''
inside {{ b }}
'''
print Template(outer).render(Context({
    'a': 'in outer', 
    'included': Template(inner)
}))
```

## unbreak not-starting pycharm

`/usr/local/bin/charm` is a runner, wrapper script that checks whether PyCharm
isn't already started. If you quit PyCharm abruptly, it will silently fail.
Remove these files to reset its "running" status:


```
/home/bartek/.PyCharm2016.1/config/port
/home/bartek/.PyCharm2016.1/system/token
```
 
## go down git tags

```
for x in $(git tag|tac); do read -p $x; git co $x; done
```
## Use dnsmasq

Let all `.lol` domains pont localy. 
```
apt install dnsmasq
sudo vim /etc/dnsmasq.d/me_is_local
# address=/lol/127.0.0.1
service dnsmasq restart
```

## bash slugify

```
slugify() {
  if [ $# -eq 0 ]
  then
      read data
  else
      data=$@
  fi
  echo $data | sed -e 's/[^[:alnum:]]/_/g' | tr -s '_' | tr A-Z a-z
}
```

## Make google always verbatim.

[chrome extension](https://chrome.google.com/webstore/detail/occcfdnjdbgjglcbpolkmjnjillkgbcm)

also [this](https://productforums.google.com/forum/#!msg/websearch/q7NK4RduwM0/LndTBrveLdMJ)

## Dirty way to enable nginx to access user folders

```bash
usermod -a -G bartek www-data
chmod g+rx /home/bartek
$ grep -A 3 site_media /etc/nginx/sites-available/this_site 
    location /site_media {
    	alias /home/bartek/workspace/this_site/site_media;
    }
```

## Do something in all subdirs

```
for x in ls *; do pushd $x; hg revert setup.py; popd; done
```

## defaultdict of defaultdict

```
group_ids = defaultdict(lambda: defaultdict(list))
# pprint
pprint({k: dict(v) for k, v in dict(group_ids).items()})
# or, ugly
pprint({
    k:{k2:v2 for k2, v2 in v.items()} 
    for k, v 
    in group_ids.items()
})
```

## Get ibus 1.5.11 on Ubuntu

```bash
wget https://github.com/ibus/ibus/releases/download/1.5.11/ibus-1.5.11.tar.gz

checking for XML::Parser... configure: error: XML::Parser perl module is required for intltool
sudo perl -MCPAN -e shell
# autoconf yes, enter, enter
# at prompt cpan[1]>
install XML::Parser

wget http://ftp.gnome.org/pub/gnome/sources/intltool/0.35/intltool-0.35.5.tar.gz

> No package 'gtk+-2.0' found
apt-get install libgtk2.0-dev

> No package 'gtk+-3.0' found
apt-get install libgtk-3-dev  # see what they did with dashes? :) nice people

> No package 'dconf' found
$ ./configure --disable-dconf

> No package 'libnotify' found
$ apt-get install libnotify-dev
```

## Why does unicode_literals differ form prefixing u in py.test

Consider:

```python
from __future__ import unicode_literals
def test_unicode():
    s = 'ł'
    print type(s), s, repr(s)
```

and

```python
def test_unicode():
    s = u'ł'
    print type(s), s, repr(s)
```

I assumed these should produce same results, they don't. Why? Py.test fails?

## jQuery .data('something') isn’t the same as .attr('data-something')

https://forum.jquery.com/topic/jquery-data-caching-of-data-attributes

So setting via `data-*` and retrieving via `.data()` will get you in trouble. 
Just be consistent. I don't understand the reasoning behind this. :/
 
## Sticky virtualenvs for virtualenvwrapper

```shell
$ cat ~/.virtualenvs/postactivate 
#!/bin/bash
echo -n "$(basename $VIRTUAL_ENV)" > ~/.virtualenvs/.last

$ cat ~/.virtualenvs/.last
wi-tex

$ tail -n 1 ~/.bashrc 
workon $(cat ~/.virtualenvs/.last)
```

## Lat PyCharm discover virtualenvs when started from sxhkd.

PyCharm needs env var `WORKON_HOME` to be set to discover virtualenv paths. 
A prepopulated list of them appears in settings and is convenient to use when creating new projects. 
So if you start pycharm by, let's say a keyboard shortcut, be sure to pass it:

```shell
$ grep Exec ~/.config/autostart/sxhkd.desktop
Exec=env WORKON_HOME=/home/bartek/.virtualenvs sxhkd
```

## List directories only

```shell
ls -d */
```

## Getting Corona SDK to run under Linux again (compiling wine)

Trying to run Corona SDK under linux via Wine (virtualbox won't run die to
opengl). I managed that on last machine but time went on, ubuntu 15.04 got
released, new version of wine was published... and official apt package does
not work anymore. Neither does PPA wine1.7. So I got to compiling. Compiling
wine from source without reading their compiling guide that I didn't find first
is a nightmare. I finally read it and they offered a single most amazing piece
of edvice. If there is a PPA there is a good chance that they put all the deps
in their source PPA. Just uncomment the line with src in wine apt list and

```shell
add-apt-repository --yes ppa:ubuntu-wine/ppa
vim /etc/apt/sources.list.d/ubuntu-wine-ubuntu-ppa-vivid.list
# uncomment deb-src line
apt-get build-dep wine1.7
```

and no more missing deps during package configure.  The whole mess was due to
other mess with SSL recently. I assume some libraries were security patched and
wine with corona stopped working with SSl connections which is needed. This was
signalled via missing gnutls during runtime. I just assume that they didn't
compile gnutls support in their PPA deb. I'll see soon if self-compiled binary
does not have this error.  The above helps building the 64bit version which is
buggy and didn't work in the end. Building 32 bit version on 64bit machine was
a nightmare but worked as a last resort. It involved lxc containers and lots of
time. 

http://wiki.winehq.org/WineOn64bit#head-ec78c77745c37a264ed79173d9704efc286514fc

## More useful gsettings

For those of you using gnome shell [classic]

```shell
gsettings set org.gnome.nautilus.preferences enable-delete true
gsettings set com.canonical.desktop.interface scrollbar-mode normal
```

If you completely hate trash and have an hour to spare and you are an OCD:
[go here](http://www.theitcommunity.com/wiki/Globally_disable_GNOME%27s_Trash_in_Debian-based_distributions)
as your only option.

## Installing mysql on default Vagrantfile will fail

Due to insufficient memory as demsg shows, in your `Vagrantfile`:

```
  config.vm.provider "virtualbox" do |v|
    # mysql requires at least that much
    v.memory = 1024
  end
```


## What packages have you ever installed on your system?

```
zgrep ' install ' /var/log/dpkg.log* | awk '{print $4}' | sed 's/:.*//' | sort
```

## Flatten tree directory content:

`find . -type f -exec mv "{}" -t . \;`

## Get audio of mp4 files

Useful to get audio from coursera content:

```bash
for f in *.mp4
do 
    ffmpeg -i "$f" -vn -acodec copy "${f/%mp4/m4a}"
done
```

## Does mongoengine's `values_list('sth')` imply `only('sth')` ?

It does:

```python
In [26]: Resource.objects(slug='X').only('slug').values_list('slug').explain() == \
   ....:     Resource.objects(slug='X').only('slug').explain() == \
   ....:     Resource.objects(slug='X').values_list('slug').explain()
Out[26]: True
```

Comparing outputs of explain is sometimes silly and dangerous but it did the trick this time.

## Get e-mails of all your coworkers from the list of git projects you have on your drive

```bash
for repo in project1 project2 project3
do 
    pushd $repo > /dev/null
    git log --format='%ae'
    popd > /dev/null
done | sort -u | uniq
```

## monitor dd

```sudo kill -USR1 $(pgrep ^dd)```

## In Ipython Download a list of youtube podcasts, convert to mp3, rename to order.

```python
#/usr/bin/env ipython3
# Download a list of youtube podcasts, convert to mp3, rename to order
import os, regex

# get the playlist of Tomasz Kopyra Blog Q&A series, takes very long
#!youtube-dl 'https://www.youtube.com/playlist?list=PLJVfE77NnRt7bWvJhqCGqB9XQ-MAhxape'

ls -1 | head
[100 pytań do kopyra] 43. odcinek-1tGxCXP4ezY.mp3
[100 pytań do kopyra] 45. odcinek-1T40CaUoG58.mp3
[100 pytań do kopyra] 47. odcinek-c0EvfQ7wNSM.mp3
[100 pytań do kopyra] 59. odcinek-wCI6Ds8NMmM.mp3
100 pytań do kopyra - odc. 10.-cLDDtEm2kEo.mp3
100 pytań do kopyra - odc. 11-mvGLBS1I8QU.mp3
100 pytań do kopyra - odc. 12-ZIN-GDjvTH0.mp3
100 pytań do kopyra odc. 13.-H2cQ1j5hvEI.mp3
100 pytań do kopyra odc. 14.-Uo76D513eJ8.mp3
100 pytań do kopyra odc. 15.-52QMYRK6lVk.mp3

files = !ls

# use regex rather than re to redefine named group "no"
VOL_NO = regex.compile(
    '(?:'
    'odcinek\s*(?P<no>\d+)'
    '|(?P<no>\d+)\.\s*odcinek'
    '|odc.\s*(?P<no>\d+)'
    ')'
)

for fname in files:
    vol_no = VOL_NO.search(fname).group('no')
    os.rename(fname, 'kopyr_qa_%s.mp3' % vol_no.zfill(2))

ls -1 | head    
kopyr_qa_01.mp3
kopyr_qa_02.mp3
kopyr_qa_03.mp3
kopyr_qa_04.mp3
kopyr_qa_05.mp3
kopyr_qa_06.mp3
kopyr_qa_07.mp3
kopyr_qa_08.mp3
kopyr_qa_09.mp3
kopyr_qa_10.mp3
```

## Reset terminal from Python

When you're debugging using [i]pdb and the process get restarted, you will 
end up with no carret, bash `reset` solves this but what if you don't want
to leave the debugger?

```python
import os; os.system('reset')
```

Obviously, with caret gone, you have to type it "blind". 

## Dumb check which package version broke the API.

```shell

tags=$(
    git ls-remote --tags https://github.com/bokeh/bokeh.git\
    | awk '{print $2;}' \
    | egrep '/([0-9.]+)$' \
    | cut -d"/" -f3 \
    | sort -r
)
set -e
for tag in ${tags[@]}
do
    echo $tag
    pip --isolated install --quiet bokeh==$tag
    python -c 'from bokeh.models.actions import Callback'
done
```


## Write a simple bash completion simulating virtualenvwrapper for pyenv.

I'd like to be able to `workon project_name` which would take me to that
project directory which would activate a previously configured pyenv for that
project directory. I'll use the template discussed
[here](https://www.debian-administration.org/article/317/An_introduction_to_bash_completion_part_2).

```shell
PROJ_DIR=~/workspace

function workon() {
    cd ~/workspace/${1}
}

function find_projects() {
    find ${PROJ_DIR} -name .python-version \
    | awk '{split($0,fragments,"/"); print fragments[5]}'
}

_workon() 
{
    local cur prev opts 
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    projects=$(find_projects)

    COMPREPLY=( $(compgen -W "${projects}" -- ${cur}) )
    return 0
}
complete -F _workon workon
```

## Update many mongo documents with a function

Isn't there a simpler way to do this?

```javascript 
var all = db.resource.find({
    slug: {$exists: false}}, 
    {private_meta:1}
).limit(50000).toArray();
print(all.length);
all.forEach(function(element, index, array){
    fragments = element.private_meta.orig_url.split('/');
    slug = fragments[fragments.length - 1];
    print(element._id + ' ' + slug);
    db.resource.findAndModify({
        query: {_id:element._id},
        update: {$set: {slug:slug, at: null}}
    });
});
```

## Automount USB storage on insertion

`apt-get install usbmount`

## PyCharm keyboard hangs

`killall -9 ibus-x11` and carry on, without restarting IDE

I seem to remeber that this caused some stability problem in the OS. 

1. [stack link](http://stackoverflow.com/a/26694754/1472229)

## VIM foo

- `D` - delete to the end of line
- `OD` - delete line but leave it empty, go to first char and `D`
- in `INSERT` mode `Ctrl-N`, `Ctrl-P` complete words

## Enabling Radeon HD 8730M on Linux for better gaming.

I installed a 3D game on Linux for the first time and the FPS sucked. 
[This](https://wiki.ubuntu.com/X/Config/HybridGraphics) tells me to get fglrx 
and reboot... 

```
$ lspci | grep VGA
00:02.0 VGA compatible controller: Intel Corporation 3rd Gen Core processor Graphics Controller (rev 09)
01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Mars [Radeon HD 8730M] (rev ff)
$ apt-get install fglrx fglrx-updates
```

Wow, it worked the first time. 


## Compile `Pyenv` Pythons with `UCS4`
The python that comes with `pyenv` is `UCS2` type [1], `lxml` needs `UCS4`, 
you need to recompile any python you'll use:

`PYTHON_CONFIGURE_OPTS="--enable-unicode=ucs4" pyenv install 2.7.4`

It's probably a good idea to recompile all wrong pythons straight away. First 
check the "UCS Status" of installed Pytohns using this magic commandfu:

```shell
find ~/.pyenv/versions/ \
    -maxdepth 3 \
    -name python \
    -print0 \
    | xargs -0 \
    -i bash -c "echo {}; eval {} -c \'import sys\; print\(sys.maxunicode\)\'" 
```

`1114111` is the desired range. 64K is not. 

There is a good chance that the wheel cache contains packages compiled for the 
previous, wrong, UCS2 Python so delete the cache:

```
rm -rf ~/.cache/pip/
```

### pyenv-virtualenv

[pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv) is great. Note that you need to 
explicitely turn it on for a given directory, so:

```
pyenv virtualenv 3.4.3 venv_name
pyenv local venv_name
```

Now if there was a virtualenvwrapper `workon`-like command that'd switch to that 
directory

The second line was not so obvious to me and docs don't mention it. Or maybe I'm
doing something wrong?

1. [Python UCS](https://docs.python.org/2/c-api/unicode.html#c.Py_UNICODE)
2. [How to pass Python build options to pyenv](https://github.com/yyuu/pyenv/issues/86)

## How to disable `mate` workspace key shortcuts

```shell
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left "[]"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right "[]"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-up "[]"
gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-down "[]"
gsettings set org.mate.Marco.global-keybindings switch-to-workspace-down ""
gsettings set org.mate.Marco.global-keybindings switch-to-workspace-up ""
```

### Reset gnome shell classic keybindings to minimum

```shell
# set all keybindings to none
for x in $(gsettings list-keys org.gnome.desktop.wm.keybindings); do gsettings set org.gnome.desktop.wm.keybindings $x []; done
# set only the useful ones
gsettings set org.gnome.desktop.wm.keybindings panel-run-dialog "['<Alt>F2']"
gsettings set org.gnome.desktop.wm.keybindings activate-window-menu "['<Alt>space']"
gsettings set org.gnome.desktop.wm.keybindings switch-applications "['<Alt>Tab']"
gsettings set org.gnome.desktop.wm.keybindings close "['<Alt>F4']"
# on titlebar, only close button
gsettings set org.gnome.desktop.wm.preferences button-layout ":close"
```

You can also access all such bindings using `dconf-editor`. The path above
can be found in the tree. Use find for similar values.

## How to extend PyCharm's multicursor to lines below.

- Double click ctrol + up/down arrows.
- [ctrl+shift]+alt+j - select [all] similar   

## Bokeh observations

- Bokeh gives you jQuery under `Bokeh.$`.


#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2017 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pox/LICENSE
"""
test pox's shell utilities
"""
import os

def test_shutils():
    '''script to test all shutils functions'''
    from pox import shelltype, homedir, rootdir, sep, mkdir, walk, where, \
                    username, minpath, env, which, find, shellsub, expandvars

   #print('testing shelltype...')
    shell = shelltype()
    try:
        assert shell in ['bash','sh','csh','zsh','tcsh','ksh','rc','es','cmd']
    except AssertionError:
        if shell:
            print("Warning: non-standard shell type")
            assert isinstance(shell, str)
        else:
            print("Warning: could not determine shell type")
            assert shell is None

   #print('testing username...')
   #print(username())

   #print('testing homedir...')
   #print(homedir())
    assert homedir().rstrip(sep()).endswith(username())

   #print('testing rootdir...')
   #print(rootdir())
    assert homedir().startswith(rootdir())

   #print('testing sep...')
   #print(sep())
   #print(sep('ext'))
#   print(sep('foo'))

   #print('testing mkdir...')
    newdir = sep().join(['xxxtest','testxxx'])
    assert mkdir(newdir).rstrip(sep()).endswith(newdir)
   #print('cleaning up...')
    os.removedirs(newdir)

   #print('testing walk...')
   #print(walk('/usr/local','*',recurse=False,folders=True,files=False))
    folders = walk(rootdir(),'*',recurse=False,folders=True,files=False)
    assert len(folders) > 0
    assert all(not os.path.isfile(folder) for folder in folders)
    home = walk(homedir()+sep()+os.pardir, username(), False, True)[0]
    assert home == homedir()

   #print('testing where...')
    shells = walk(home,'.bashrc',recurse=0)
    bashrc = where('.bashrc',home)
    if bashrc:
        assert bashrc in shells
    else:
        assert not shells
   #print(bashrc)

   #print('testing minpath...')
   #print(minpath(os.path.expandvars('$PATH')))
    path = expandvars('$PATH')
    assert minpath(path).count(sep('path')) <= path.count(sep('path'))

   #print('testing env...')
    assert env('ACSDAGHQSBFCASDCOMAOCMQOMCQWMOCQOMCOMQRCVOMQOCMQORMCQ') == {}
    if 'HOME' not in os.environ:
        os.environ['HOME'] = homedir()
    assert env('HOME',all=False) or env('USERPROFILE',all=False) == homedir()
    pathdict = env('*PATH*',minimal=True)
    assert len(pathdict) > 0
    assert all('PATH' in key for key in pathdict)

   #print('testing which...')
    assert which('python').endswith(('python','python.exe'))
    assert which('python') in which('python',all=True)

   #print('testing find...')
   #print(find('python','/usr/local',type='l'))
   #print(find('*py;*txt'))
    x = 'tests' if find('setup.py', recurse=False) else '.'
    assert find('__init__*;test_*',x,False,'f') == find('*py',x,recurse=False)

   #print('testing shellsub...')
    command = '${HOME}/bin/which foo("bar")'
   #print(repr(command))
   #print(repr(shellsub(command)))
    assert shellsub(command) == '\\${HOME}/bin/which foo\\(\\"bar\\"\\)'

    return


if __name__=='__main__':
    test_shutils()

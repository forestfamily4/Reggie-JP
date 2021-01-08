#!/usr/bin/python
# -*- coding: latin-1 -*-

# Reggie Next - New Super Mario Bros. Wii Level Editor
# Milestone 3
# Copyright (C) 2009-2014 Treeki, Tempus, angelsl, JasonP27, Kamek64,
# MalStar1000, RoadrunnerWMC, 2017 Stella/AboodXD, John10v10

# This file is part of Reggie Next.

# Reggie Next is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Reggie Next is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Reggie Next.  If not, see <http://www.gnu.org/licenses/>.


# windows_build.py
# Builds Reggie! to a Windows binary (*.exe)
# Use the values below to configure the release:

PackageName = 'reggie_next_m3a2_win32'
Version = '0.3.2'  # This must be a valid float in string format

################################################################
################################################################

# Imports
import os.path
import shutil
import sys

try:
    from cx_Freeze import setup, Executable
except ImportError:
    print('>> Imports failed; please install cx_Freeze.')

# Verbose flag
verboseFlag = False
if '-v' in sys.argv:
    sys.argv.remove('-v')
    verboseFlag = True
if '--verbose' in sys.argv:
    sys.argv.remove('--verbose')
    verboseFlag = True


# Useful function to print text only if in verbose mode
def printv(text):
    """Convenience function"""
    if verboseFlag: print(text)


# UPX flag
upxFlag = False
if '-upx' in sys.argv:
    sys.argv.remove('-upx')
    upxFlag = True

# Pick a build directory
dir_ = 'distrib/' + PackageName
printv('>> Build directory will be ' + dir_)

# Print some stuff
print('[[ Freezing Reggie! Next ]]')
print('>> Destination directory: %s' % dir_)

# Add the "build" parameter to the system argument list
if 'build' not in sys.argv:
    sys.argv.append('build')

# Clear the directory
printv('>> Clearing/creating directory...')
if os.path.isdir(dir_): shutil.rmtree(dir_)
os.makedirs(dir_)
printv('>> Directory ready!')

# exclude QtWebKit to save space, plus Python stuff we don't use
excludes = []

# Set it up
printv('>> Running build functions...')
base  = None
if sys.platform == 'win32':
    base = 'Win32GUI' 
 
exe = Executable(script='reggie.py', base = "Console", icon='reggiedata/win_icon.ico')

setup(
    name='Reggie! Level Editor Next',
    version=Version,
    description='Reggie! Level Editor Next',
    options={
        'build_exe': {
            'excludes': excludes,
            'packages': [ 'encodings', 'encodings.hex_codec', 'encodings.utf_8'],
            'build_exe': dir_
        },
    },
    executables=[exe]
)
print('>> Built frozen executable!')

# Now that it's built, configure everything


# Remove a useless file we don't need
printv('>> Attempting to remove w9xpopen.exe ...')
try:
    os.unlink(dir_ + '/w9xpopen.exe')
except:
    pass
printv('>> Done.')

if upxFlag:
    if os.path.isfile('upx/upx.exe'):
        print('>> Found UPX, using it to compress the executables!')
        files = os.listdir(dir_)
        upx = []
        for f in files:
            if f.endswith('.exe') or f.endswith('.dll') or f.endswith('.pyd'):
                upx.append('"%s/%s"' % (dir_, f))
        os.system('upx/upx.exe -9 ' + ' '.join(upx))
        print('>> Compression complete.')
    else:
        print('>> UPX not found, binaries can\'t be compressed.')
        print('>> In order to build Reggie! with UPX, place the upx.exe file into '
              'a subdirectory named "upx".')
else:
    print('>> No \'-upx\' flag specified, so UPX compression will not be attempted.')

print('>> Attempting to copy required files...')
if os.path.isdir(dir_ + '/reggiedata'): shutil.rmtree(dir_ + '/reggiedata')
if os.path.isdir(dir_ + '/reggieextras'): shutil.rmtree(dir_ + '/reggieextras')
shutil.copytree('reggiedata', dir_ + '/reggiedata')
shutil.copytree('reggieextras', dir_ + '/reggieextras')
shutil.copy('license.txt', dir_)
shutil.copy('license_short.txt', dir_)
shutil.copy('readme.md', dir_)
if not os.path.isfile(dir_ + '/libEGL.dll'):
    shutil.copy('libEGL.dll', dir_)
print('>> Files copied!')

print('>> Attempting to write a new release.txt ...')
release = open(dir_ + '/release.txt', 'w', encoding='utf-8')
release.write('windows')
release.close()
del release
print('>> release.txt written!')

print('>> Reggie has been frozen to %s !' % dir_)

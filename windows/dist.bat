:: Gnerating the LinkChecker Windows .exe installer
:: Copyright (C) 2010-2011 Bastian Kleineidam
:: This program is free software; you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
:: the Free Software Foundation; either version 2 of the License, or
:: (at your option) any later version.
::
:: This program is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: GNU General Public License for more details.
::
:: You should have received a copy of the GNU General Public License along
:: with this program; if not, write to the Free Software Foundation, Inc.,
:: 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
@echo off
set PYDIR=C:\Python27
set SZ_EXE="C:\Programme\7-Zip\7z.exe"
set UPX_EXE="C:\Software\upx307w\upx.exe"
for /f "usebackq tokens=*" %%a in (`%PYDIR%\python.exe setup.py --version`) do set VERSION="%%a"
set PORTDIR=LinkChecker-%VERSION%
rd /s /q build > nul
call windows\build.bat
rd /s /q dist > nul
%PYDIR%\python.exe setup.py py2exe

echo Building portable distribution
rd /s /q %PORTDIR% > nul
xcopy /e /i dist %PORTDIR%
echo Compressing executables
for /r %PORTDIR% %%e in (*.pyd,*.dll,*.exe) do %UPX_EXE% "%%e" --best
%SZ_EXE% a -mx=9 -md=32m LinkChecker-%VERSION%-portable.zip %PORTDIR%
rd /s /q %PORTDIR%
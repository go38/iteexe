#!/bin/bash

# ===========================================================================
# eXe
# Copyright 2012-2013, Pedro Peña Pérez, Open Phoenix IT
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Changes
# -------
# 2013-10:
# 	* Usage of Babel1.3
# 		Uses python Babel 1.3 patched to include 'Language' header 
#		(https://dl.dropboxusercontent.com/s/k1i7ph2m2g4s7kx/Babel-1.3.tar.gz)
# 		as discussed here: 
# 		https://forja.cenatic.es/tracker/index.php?func=detail&aid=1905&group_id=197&atid=883
#	* Changed --version from '1.04.1' to '2.0' (JRF)
#===========================================================================


echo -e " *** Extracting messages from python exe files and jsui javascript files ***\n"
pybabel extract --keyword=x_ --project "eXeLearning" --version "2.0" -F pybabel.conf --sort-by-file . > exe/locale/messages.pot
sed -i "s/^#, fuzzy\$//" exe/locale/messages.pot
echo -e "\n\n\n *** Updating *.po files ***\n"
pybabel update -D exe -i exe/locale/messages.pot -d exe/locale/ -N
echo -e "\n\n\n *** Compiling *.mo files ***\n"
pybabel compile -D exe -d exe/locale/ --statistics
echo -e "\n\n\n *** Compiling javascript for jsui files ***\n"
python tools/po2json.py --domain exe --directory exe/locale --output-dir exe/jsui/scripts/i18n

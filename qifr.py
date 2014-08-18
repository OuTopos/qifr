#!/usr/bin/env python
# encoding: utf-8
"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os
import re

FORMATS = []
FORMATS.append(("Swedbank Account (Copy paste)", 2, 3, 5, 0, "\s*([0-9][0-9]-[0-9][0-9]-[0-9][0-9])\t([0-9][0-9]-[0-9][0-9]-[0-9][0-9]) \t(.*)\t(-?[0-9 ]*,[0-9 ][0-9 ])\t(-?[0-9 ]*,[0-9 ][0-9 ])"))
FORMATS.append(("Swedbank Credit Card (Copy paste)", 1, 2, 4, 3, "\s*([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])\t (.*)\t (.*)\t (-?[0-9 ]*,[0-9 ][0-9 ])"))

def help():
	print("Usage: python qifr.py [FILE] [FORMAT]")
	help_formats()

def help_formats():
	print("Available formats:")
	for i, v in enumerate(FORMATS):
		print("  " + str(i) + " - " + v[0])
	print("Use the number as argument.")

def convert(path, format_index):
	if not os.path.exists(path):
		print("Error: File " + path + " not found!")
		sys.exit(1)
	elif format_index < 1 or format_index > len(FORMATS):
		print(len(FORMATS))
		print("Error: Pattern not found!")
		help_formats()
		sys.exit(1)
	else:
		print("Converting file " + path + " with format " + FORMATS[format_index-1][0])
		file_in = file(path)
		file_out = file(path + ".qif", 'w')

		pattern = FORMATS[format_index-1][5]
		d = FORMATS[format_index-1][1]
		p = FORMATS[format_index-1][2]
		t = FORMATS[format_index-1][3]
		m = FORMATS[format_index-1][4]

		reg = re.compile(pattern)
		for line in file_in.readlines():
			line = unicode(line, 'ascii', "ignore")
			match = reg.match(line)
			if match is not None:
				file_out.write("!Type:Bank\n")
				file_out.write("D%s\n" % match.group(d))
				file_out.write("P%s\n" % match.group(p))
				file_out.write("T%f\n" % float(match.group(t).replace(' ', '').replace(',', '.')))
				if m != 0:
					file_out.write("M%s\n" % match.group(m))
				file_out.write("^\n")

if len(sys.argv) is not 3:
	help()
	sys.exit(1)
else:
	try:
		convert(sys.argv[1], int(sys.argv[2]))
	except ValueError:
		print "Format not a number!"
		help()
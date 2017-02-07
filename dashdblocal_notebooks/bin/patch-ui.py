#!/usr/bin/env python3
# (c) Copyright IBM Corporation 2016
# LICENSE: BSD-3, https://opensource.org/licenses/BSD-3-Clause

# Patch the Jupyter base page template to display user and target host
# in the page header

import sys, os, socket, fileinput, re

PATCH_TARGET='/opt/conda/lib/python3.5/site-packages/notebook/templates/page.html'
PATCH_BAK = PATCH_TARGET + '.bak'

print("Patching {0}".format(PATCH_TARGET))
if os.path.isfile(PATCH_BAK):
	print("File already patched");
else:
	DASHDBHOST = os.environ.get('DASHDBHOST') or 'localhost'
	DASHDBUSER = os.environ.get('DASHDBUSER')
	if (DASHDBHOST == 'localhost' or DASHDBHOST =='127.0.0.1'): DASHDBHOST = socket.getfqdn()
	if (not DASHDBUSER): sys.exit("DASHDBUSER variable must be defined")
	dashdb_header_line = ('  <div id="dashdb-header" class="container">Notebook server for {0}@{1}</div>\n'
						.format(DASHDBUSER, DASHDBHOST))

	os.rename(PATCH_TARGET, PATCH_BAK)
	with open(PATCH_BAK, "r") as infile, open(PATCH_TARGET, "w") as outfile:
		for line in infile:
			if (re.match(r'\s*<div class="header-bar">', line)):
				# insert extra info before header bar
				outfile.write(dashdb_header_line)
			outfile.write(line)
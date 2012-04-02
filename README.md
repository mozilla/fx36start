Firefox 3.6 Start Page
======================
This is a very simple static website generator for the Firefox 3.6 start page.

Based on [nocturnal](https://github.com/mozilla/nocturnal/), it takes a single
jinja2 template, throws in some translations from .lang files,, and generates a
bunch of static, localized output files.

Usage
-----
Checkout
~~~~~~~~

    git clone git://github.com/mozilla/fx36start.git

The localization files live in SVN. Check them out into the subdirectory
"locale" to pull in translations.

    cd fx36start
    svn checkout https://svn.mozilla.org/projects/l10n-misc/trunk/fx36start/locale/

Generating output files
~~~~~~~~~~~~~~~~~~~~~~~
Specify an output directory (it shouldn't be the same directory as the
repo) and allow a few seconds for the script to scrape Mozilla's FTP
server.

    ./generate.py --output-dir html

To delete the output dir before generating the output (careful!), use
the --force option.

    ./generate.py --output-dir html -f

Extracting .lang files
~~~~~~~~~~~~~~~~~~~~~~
If you change localizable strings in the templates, you'll want to extract those
strings and add them to the .lang files.

    ./l10n_extract.py

should do the trick. This relies on gettext for the extraction.

License
-------
This software is licensed under the [Mozilla Tri-License][MPL]:

    ***** BEGIN LICENSE BLOCK *****
    Version: MPL 1.1/GPL 2.0/LGPL 2.1

    The contents of this file are subject to the Mozilla Public License Version
    1.1 (the "License"); you may not use this file except in compliance with
    the License. You may obtain a copy of the License at
    http://www.mozilla.org/MPL/

    Software distributed under the License is distributed on an "AS IS" basis,
    WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
    for the specific language governing rights and limitations under the
    License.

    The Original Code is Nocturnal.

    The Initial Developer of the Original Code is Mozilla.
    Portions created by the Initial Developer are Copyright (C) 2012
    the Initial Developer. All Rights Reserved.

    Contributor(s):
      Matthew Riley MacPherson <tofumatt@mozilla.com>
      James Long <jlong@mozilla.com>
      Fred Wenzel <fwenzel@mozilla.com>

    Alternatively, the contents of this file may be used under the terms of
    either the GNU General Public License Version 2 or later (the "GPL"), or
    the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
    in which case the provisions of the GPL or the LGPL are applicable instead
    of those above. If you wish to allow use of your version of this file only
    under the terms of either the GPL or the LGPL, and not to allow others to
    use your version of this file under the terms of the MPL, indicate your
    decision by deleting the provisions above and replace them with the notice
    and other provisions required by the GPL or the LGPL. If you do not delete
    the provisions above, a recipient may use your version of this file under
    the terms of any one of the MPL, the GPL or the LGPL.

    ***** END LICENSE BLOCK *****

[MPL]: http://www.mozilla.org/MPL/

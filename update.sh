#!/bin/bash
# Example update script. Adjust at will.

#set -x

function checkretval()
{
    retval=$?
        if [[ $retval -gt 0 ]]
        then
                $error "Error!!! Exit status of the last command was $retval"
                exit $retval
        fi
}

CODE_DIR="/data/fx36start"
WEB_DIR="/data/startpage"

echo -e "Updating code..."
pushd $CODE_DIR

git pull

if [ ! -d "locale" ]; then
    svn checkout https://svn.mozilla.org/projects/l10n-misc/trunk/fx36start/locale/
fi
pushd locale
svn up
popd

./generate.py --output-dir $WEB_DIR -f --nowarn
checkretval

popd

/data/startpage-dev/deploy -n start-dev.allizom.org

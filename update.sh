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
    git clone https://github.com/mozilla-l10n/fx36start-l10n locale
fi
pushd locale
git pull
popd

./generate.py --output-dir $WEB_DIR -f --nowarn
checkretval

popd

/data/startpage-dev/deploy -n start-dev.allizom.org

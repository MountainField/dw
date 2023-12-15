#!/usr/bin/env sh
# -*- coding: utf-8 -*-

# exit when error mode
set -e 

function test_dw() {
    local py_ver="${1}"
    
    echo "#######################################" 1>&2
    echo "# Switching Python version with ${py_ver}" 1>&2
    echo "#######################################" 1>&2

    pyenv local "${py_ver}"

    pip3 install --upgrade pip wheel
    pip3 install -e '..[dev]'

    python3 -m unittest discover -v -s ../src -p '*_spec.py'
}

#####################################################
# Main
function main() {
	local -r THIS_DIR="$(cd $(dirname $BASH_SOURCE); pwd)"
    cd "${THIS_DIR}"

    local -a py_vers=(
        3.6.15
        3.7.17
        3.8.18
        3.9.18
        3.10.13
        3.11.4
        3.12.1
    )

    for py_ver in "${py_vers[@]}" ; do
        test_dw "${py_ver}"
    done
}

main "$@"

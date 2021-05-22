#!/usr/bin/bash


function print_fig {
    figlet PodExtractr 2.0
}

if test -z $1
then
    print_fig
    python3 deploy/app.py
else
    if test $1 == "demo"
    then
        print_fig
        python3 demo/app.py
    fi
fi

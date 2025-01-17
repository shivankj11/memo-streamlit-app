#!/usr/bin/env python3
from subprocess import run
import os
path = os.path.dirname(__file__)
os.chdir(path)

if __name__ == '__main__':
    run(f'streamlit run webapp.py'.split())
#!D:\Users\2008g\PycharmProjects\fastapi_imooc\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pip==22.2.2','console_scripts','pip3.7'
__requires__ = 'pip==22.2.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pip==22.2.2', 'console_scripts', 'pip3.7')()
    )

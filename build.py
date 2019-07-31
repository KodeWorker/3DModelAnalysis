# -*- coding: utf-8 -*-

import os
import shutil

if __name__ == '__main__':
    # 清空前次編譯
    if os.path.exists('main.spec'):
        os.remove('main.spec')
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    # 編譯程式
    os.system('pyinstaller main.py')
    os.rename(os.path.join(os.path.dirname(__file__), 'dist', 'main', 'PyQt5', 'Qt', 'plugins', 'platforms'),
              os.path.join(os.path.dirname(__file__), 'dist', 'main', 'platforms'),)
    # 執行測試
    os.system('{}'.format(os.path.abspath('dist/main/main.exe')))
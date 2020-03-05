# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path

def pdftocairo(input_path, output_path, resolution=300):
    pdftocairo_path = Path('poppler-0.68.0/bin/pdftocairo.exe')
    cmd = [str(pdftocairo_path), '-png', '-r', str(resolution), str(input_path), str(output_path)]
    stdout, stderr = subprocess_popen(cmd)
    return stdout, stderr

def pdfinfo(path):
    pdfinfo_path = Path('poppler-0.68.0/bin/pdfinfo.exe')
    stdout, stderr = subprocess_popen( [str(pdfinfo_path), str(path)] )
    if not stderr == '':
        return stdout, stderr
    lines = [ line.split(':') for line in stdout.splitlines() ]
    dict_ = { line[0].strip() : ':'.join(line[1:]).strip() for line in lines }
    s = dict_['Page size'].split()
    dict2 = { 'Name':str(path.name), 'Path':str(path), 'height':s[0], 'width':s[2] }
    dict_.update(dict2)
    return dict_

def subprocess_popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    proc = subprocess.Popen(
        cmd, 
        encoding='cp932', 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        startupinfo=startupinfo
    )
    stdout, stderr = proc.communicate(timeout=1000)
    return stdout, stderr

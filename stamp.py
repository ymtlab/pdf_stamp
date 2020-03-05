# -*- coding: utf-8 -*-
import subprocess

def stamp(pdf_path, stamp_path, output_folder):
    output = output_folder / pdf_path.name
    cmd = ['pdftk.exe', str(pdf_path), 'stamp', str(stamp_path), 'output', str(output)]
    subprocess_popen(cmd)

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

if __name__ == '__main__':
    from pathlib import Path
    stamp(Path('Y19X02AUA501.pdf'), Path('__test__.pdf'), Path('output/'))

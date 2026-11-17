import os, shutil, subprocess
print('shutil.which:', shutil.which('ffprobe'))
print('PATH entries count:', len(os.environ.get('PATH','').split(os.pathsep)))
path = os.environ.get('PATH','')
print('\n-- PATH (tail 400 chars) --\n', path[-400:])
try:
    out = subprocess.check_output(['ffprobe','-version'], stderr=subprocess.STDOUT, text=True)
    print('\nsubprocess ffprobe output starts:\n', out.splitlines()[0])
except Exception as e:
    print('\nsubprocess error:', repr(e))

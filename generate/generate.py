import os
from math import log, floor
from random import choice

### vvv CONFIG vvv ###  (I am too lazy to ask the user for numbers)
CHARSET = 'abcdefghijklmnopqrstuvwxyz'  # characters used for folder and target names
NAMELEN = 8  # length of each folder's and target's name
DEPTH = 3  # 1 = one folder with TPF targets, 3 = SPF folders, SPF subfolders in each, TPF targets in each subfolder
SPF = 10  # subfolders per folder
TPF = 200  # targets per folder
BAZELVERSION = None  # if set to None, .bazelversion will not be created - otherwise, set to something like "5.4.0"
### ^^^ CONFIG ^^^ ###

SIZESET = ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q')
N = TPF * SPF ** (DEPTH - 1)


# for example, a project having 547928 targets will be called "bazel-500k"
def project_name():
  magn = floor(log(N, 10))
  letter = SIZESET[magn // 3]
  # ^^^ will cause an exception if there are more than 10^33 targets, but good luck in generating that many
  remaining0s = '0' * (magn % 3)
  mult = str(N)[0]
  return f'bazel-{mult}{remaining0s}{letter}'

def randname():
  return ''.join(
    (choice(CHARSET) for i in range(NAMELEN))
  )

def makeBUILD(prefix):
  with open(f'{prefix}BUILD', 'w') as f:
    for i in range(TPF):
      f.write(f'java_library(name = "{randname()}")\n')

def create(depth, prefix):
  if depth == 1:
    makeBUILD(prefix)
  elif depth > 1:
    for i in range(SPF):
      dirname = f'{prefix}{randname()}'
      os.mkdir(dirname)
      create(depth - 1, f'{dirname}/')


PROJECT = project_name()
if not os.path.exists(f'./{PROJECT}'):
  os.mkdir(PROJECT)
  create(DEPTH, f'{PROJECT}/')
  with open(f'{PROJECT}/WORKSPACE', 'w') as fp:
    pass
  if BAZELVERSION is not None:
    with open(f'{PROJECT}/.bazelversion', 'w') as bazelversion:
      bazelversion.write(BAZELVERSION)
  print(f'Generated {N} targets (project "{PROJECT}")')
else:
  print(f'Folder "{PROJECT}" already exists.')

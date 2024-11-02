import os
from math import log, floor
from random import choice

### vvv CONFIG vvv ###  (I am too lazy to ask the user for numbers)
CHARSET = 'abcdefghijklmnopqrstuvwxyz'  # characters used for folder and target names
NAMELEN = 8  # length of each folder's and target's name
DEPTH = 2  # 1 = one folder with TPF targets, 3 = SPF folders, SPF subfolders in each, TPF targets in each subfolder
SUBFOLDERS_PER_FOLDER = 1  # subfolders per folder
TARGETS_PER_FOLDER = 1  # targets per folder
SOURCES_PER_TARGET = 20000
BAZELVERSION: str | None = None  # if set to None, .bazelversion will not be created - otherwise, set to something like "5.4.0"
### ^^^ CONFIG ^^^ ###

SIZESET = ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q')
N = TARGETS_PER_FOLDER * SUBFOLDERS_PER_FOLDER ** (DEPTH - 1)


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
    (choice(CHARSET) for _ in range(NAMELEN))
  )

def make_target_sources(prefix):
  sources = []
  for i in range(SOURCES_PER_TARGET):
    class_name = randname().capitalize()
    src_name = f'{class_name}.java'
    with open(f'{prefix}{src_name}', 'w') as src_file:
        # Write a simple Java class
        src_file.write(f'public class {class_name} {{\n')
        src_file.write('    // TODO: Implement\n')
        src_file.write('}\n')

    sources.append(src_name)

  return sources

def make_target(prefix):
  with open(f'{prefix}BUILD', 'w') as f:
    for i in range(TARGETS_PER_FOLDER):
      target_name = randname()
      sources_list = make_target_sources(prefix)
      f.write(f'java_library(\n')
      f.write(f'    name = "{target_name}",\n')
      f.write(f'    srcs = glob({str(sources_list)}),\n')
      f.write(')\n')

def create(depth, prefix):
  if depth == 1:
    make_target(prefix)
  elif depth > 1:
    for i in range(SUBFOLDERS_PER_FOLDER):
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

import os

os.chdir("../authorizr")
assert os.path.isfile("manage.py")
trg = os.path.expanduser("~/deploy/authorizr")
assert os.path.isdir(trg)
os.system("cp -r * " + trg)


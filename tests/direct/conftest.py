import os
_u=os.unlink
def safe(p,*a,**k):
 try:return _u(p,*a,**k)
 except PermissionError:return None
os.unlink=safe
CONTRACT=os.path.join('contracts','contract.py')

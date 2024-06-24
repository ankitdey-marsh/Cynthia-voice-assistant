import ctypes

def lock_windows():
    ctypes.windll.user32.LockWorkStation()


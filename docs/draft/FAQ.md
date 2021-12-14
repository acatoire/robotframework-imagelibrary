

Run in venv
samples\win-calc> cd .\venv\
samples\win-calc\venv> activate
(venv) samples\win-calc\venv> cd ..
(venv) samples\win-calc>

setup packages

Issue with puautogui
[ ERROR ] Error in file 'xxx' on line 5: Importing library 'ImageLibrary' failed: ImportError: cannot import name 'POINT'
 from 'pyautogui._pyautogui_win' (xxx\pyautogui\_pyautogui_win.py)
Traceback (most recent call last):
  File [...]
  File "xxx\ImageLibrary\GUIProcess\_gui_win.py", line 3, in <module>
    from pyautogui._pyautogui_win import POINT

python -m pip install pyautogui

(1, "Error, unknown command line argument '-psm'");
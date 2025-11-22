# Tic Tac Toe (GUI)

This project contains a simple Tic Tac Toe implementation and a GUI frontend using `tkinter`.

Files:
- `Code2.py` - original console-based Tic Tac Toe (human vs human or human vs computer).
- `tic_tac_toe_gui.py` - new GUI application using `tkinter`.

Running GUI:

Make sure you have Python 3 installed. Then run:

```bash
python3 tic_tac_toe_gui.py
```

Packaging for distribution (optional):

To create a single-file executable for Linux, install `pyinstaller` and build:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed tic_tac_toe_gui.py
```

The executable will appear under `dist/tic_tac_toe_gui` (or with .exe on Windows).

Notes:
- The GUI uses `tkinter`, which is included in the standard Python distribution on most platforms. On some minimal Linux installs you may need to install `python3-tk`.
- If you want the GUI logic merged into `Code2.py` or prefer a different GUI toolkit (PyQt, Kivy), tell me and I can adapt it.

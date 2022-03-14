main:
	python3 src/Main.py
resources:
	pyrcc5 ../icon/resources.qrc -o Resources.py
binary:
	pyinstaller --onefile --windowed --icon=icon/ico.ico src/Main.py
search:
	findstr /s setSelected .\src\*
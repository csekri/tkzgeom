main:
	python3 src/Main.py
resources:
	pyrcc5 ../../icon/resource.qrc -o Resources.py
binary:
	pyinstaller --onefile --windowed src/Main.py
search:
	findstr /s setSelected .\src\*
@echo on

echo Setting Variables
set disFolder="Genshin Stopwatch"
set Txt="requirements.txt"
set Spec="./src/python/main.spec"

echo Installing Dependencies
pip install -r %Txt%

echo Running Pyinstaller
pyinstaller --clean %Spec% --distpath ./%disFolder%

echo Installation Finished!
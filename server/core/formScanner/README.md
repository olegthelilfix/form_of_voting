**Константы в начале файла AlgorithmScan.py определяют относительные пути к папкам, от которых зависит исходный код.**
Имя исходного файла с изображением бланка задается как значение константы **SOURCE_IMAGE**, либо в качестве параметра командной строки.

ScanFormAPI.py предоставляет интерфейс для генерации маркера и старта работы алгоритма распознавания.

Файл TokenData содержит в себе информацию о результатах распознавания. При необходимости размещать эти данные в файле с другим именем 
делается поправка значения константы **RESULTS_FILE_NAME** в файле ScanResultEnums.py

Фотографии бланка:
https://www.sendspace.com/file/z0w20p

**Необходимые библиотеки:**

*OpenCV 3.0*

http://www.pyimagesearch.com/2015/07/20/install-opencv-3-0-and-python-3-4-on-ubuntu/

*Pillow*

sudo apt-get install python-imaging

http://pillow.readthedocs.org/en/3.1.x/installation.html

*libzbar*

https://pypi.python.org/pypi/libzbar-cffi

*numpy*

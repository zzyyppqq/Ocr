[软件截图](screen.png)


### Mac环境

- Tesseract是一个开源的OCR引擎，能识别100多种语言（中，英，韩，日，德，法...等等），但是Tesseract对手写的识别能力较差。

```sh
//安装tesseract的同时安装训练工具
brew install --with-training-tools tesseract
 
//安装tesseract的同时安装所有语言，语言包比较大，如果安装的话时间较长，建议不安装，按需选择
brew install  --all-languages tesseract
 
//安装tesseract，并安装训练工具和语言
brew install --all-languages --with-training-tools tesseract 
 
//只安装tesseract，不安装训练工具
brew install tesseract

```
- 下载语言库chi_sim.traineddata 

地址：https://github.com/tesseract-ocr/tessdata

拷贝到/usr/local/Cellar/tesseract/4.0.0/share/tessdata/chi_sim.traineddata

```sh
$ pip install PIL 
$ pip install pytesseract 


from PIL import Image
import pytesseract
#图片文字识别
text=pytesseract.image_to_string(Image.open('image.png'),lang='chi_sim')
print(text)

```

# 打包
```sh
$ pyinstaller --windowed --onefile --icon=icon.icns --clean --noconfirm ocr_main.py

```
- convert png to icns 
https://cloudconvert.com/png-to-icns


- pytesseract psm options

```
0 定向脚本监测（OSD）
1 使用OSD自动分页
2 自动分页，但是不使用OSD或OCR（Optical Character Recognition，光学字符识别）
3 全自动分页，但是没有使用OSD（默认）
4 假设可变大小的一个文本列。
5 假设垂直对齐文本的单个统一块。
6 假设一个统一的文本块。
7 将图像视为单个文本行。
8 将图像视为单个词。
9 将图像视为圆中的单个词。
10 将图像视为单个字符。
```
#### UI
- pyqt5 Designer 
```
下载Anaconda3 ,其内置Designer ,默认安装在用户根目录下：~/anaconda3
https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/

Designer位置：~/anaconda3/bin/Designer.app

其他可以自行搜索：PyCharm+PyQt5+QtDesigner配置

```

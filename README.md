# 番茄闹钟 - 独立桌面应用

## 说明
这是一个将网页版番茄钟转换为独立桌面应用的项目。用户可以双击运行，无需在浏览器中打开。

## 使用方法
1. 双击 `PomodoroTimer.exe` 文件即可运行应用
2. 或者双击 `番茄闹钟.bat` 文件运行（需要安装Python和依赖）

## 项目结构
- `app.py` - 主程序文件，使用pywebview库将网页应用封装为桌面应用
- `index.html` - 应用界面
- `script.js` - 应用逻辑
- `style.css` - 应用样式
- `build_app.bat` - 构建脚本，用于生成可执行文件

## 构建说明
如需重新构建可执行文件，请运行：
```
.\build_app.bat
```

生成的可执行文件将位于 `dist` 文件夹中。

## 依赖
- Python 3.x
- pywebview
- pyinstaller
import webview
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import socket
from datetime import datetime

class Api:
    """提供Python API给前端调用"""

    def log(self, message):
        """写入日志到文件"""
        log_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(log_dir, 'tomato.log')

        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(message)
            return True
        except Exception as e:
            print(f"写入日志失败: {e}")
            return False

def find_free_port():
    """查找一个可用的端口"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def start_server():
    """启动本地HTTP服务器"""
    # 更改到当前脚本目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 查找一个可用端口
    port = find_free_port()
    
    # 启动HTTP服务器
    server = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    
    # 在新线程中启动服务器
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    return server, port

def main():
    # 启动本地服务器
    server, port = start_server()

    # 构建应用URL
    url = f'http://localhost:{port}/index.html'

    # 创建API实例
    api = Api()

    # 创建webview窗口
    webview.create_window(
        '番茄闹钟',
        url=url,
        width=300,
        height=320,
        resizable=False,
        min_size=(240, 280),
        js_api=api  # 添加JavaScript API
    )
    webview.start(debug=False)  # 关闭调试模式以便双击运行

    # 应用关闭后停止服务器
    server.shutdown()

if __name__ == '__main__':
    main()
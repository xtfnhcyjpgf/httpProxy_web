#!/usr/bin/env python3
"""
部署脚本 - 将项目部署到生产服务器
"""
import paramiko
from paramiko import SSHClient, AutoAddPolicy
import os
import tarfile
import time
import sys


SERVER_CONFIG = {
    'host': '8.137.176.50',
    'port': 22,
    'username': 'root',
    'password': 'YLtm9awnku7ps5fq'
}

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE_DIR = '/root/httpProxy_web'
WEB_PORT = 8080
API_PORT = 8090


def create_tar_archive():
    """创建项目压缩包"""
    print("正在创建项目压缩包...")
    tar_path = os.path.join(PROJECT_DIR, 'project.tar.gz')
    
    with tarfile.open(tar_path, 'w:gz') as tar:
        tar.add(os.path.join(PROJECT_DIR, 'app.py'), 'app.py')
        tar.add(os.path.join(PROJECT_DIR, 'config.py'), 'config.py')
        tar.add(os.path.join(PROJECT_DIR, 'database.py'), 'database.py')
        tar.add(os.path.join(PROJECT_DIR, 'requirements.txt'), 'requirements.txt')
        tar.add(os.path.join(PROJECT_DIR, 'frontend', 'dist'), 'frontend/dist', recursive=True)
        
    print(f"压缩包已创建: {tar_path}")
    return tar_path


def ssh_connect():
    """连接到服务器"""
    print(f"正在连接服务器 {SERVER_CONFIG['host']}...")
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(
        hostname=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        username=SERVER_CONFIG['username'],
        password=SERVER_CONFIG['password']
    )
    print("SSH连接成功")
    return ssh


def execute_command(ssh, command):
    """执行远程命令"""
    print(f"执行命令: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    if output:
        print(output)
    if error:
        print(f"错误: {error}")
    return output, error


def upload_file(ssh, local_path, remote_path):
    """上传文件到服务器"""
    print(f"正在上传文件 {local_path} -> {remote_path}...")
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)
    sftp.close()
    print("文件上传成功")


def deploy():
    """部署流程"""
    try:
        # 1. 创建压缩包
        tar_path = create_tar_archive()
        
        # 2. 连接服务器
        ssh = ssh_connect()
        
        # 3. 停止旧进程
        print("\n停止旧进程...")
        execute_command(ssh, f"pkill -f 'python.*app.py' || true")
        execute_command(ssh, f"pkill -f 'gunicorn' || true")
        
        # 4. 创建远程目录
        print(f"\n创建远程目录 {REMOTE_DIR}...")
        execute_command(ssh, f"mkdir -p {REMOTE_DIR}")
        execute_command(ssh, f"mkdir -p {REMOTE_DIR}/uploads")
        
        # 5. 上传压缩包
        remote_tar_path = f"{REMOTE_DIR}/project.tar.gz"
        upload_file(ssh, tar_path, remote_tar_path)
        
        # 6. 解压文件
        print("\n解压文件...")
        execute_command(ssh, f"cd {REMOTE_DIR} && tar -xzf project.tar.gz")
        
        # 7. 安装依赖
        print("\n安装Python依赖...")
        execute_command(ssh, "apt update && apt install -y python3-pip python3-venv nginx || true")
        execute_command(ssh, f"cd {REMOTE_DIR} && python3 -m venv venv")
        execute_command(ssh, f"cd {REMOTE_DIR} && source venv/bin/activate && pip install -r requirements.txt gunicorn")
        
        # 8. 创建Gunicorn服务配置
        print("\n配置Gunicorn服务...")
        gunicorn_service = f"""[Unit]
Description=Gunicorn instance to serve httpProxy_web
After=network.target

[Service]
User=root
Group=root
WorkingDirectory={REMOTE_DIR}
Environment="PATH={REMOTE_DIR}/venv/bin"
ExecStart={REMOTE_DIR}/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:{API_PORT} app:app

[Install]
WantedBy=multi-user.target
"""
        execute_command(ssh, f"cat > /etc/systemd/system/httpProxy_web.service << 'EOF'\n{gunicorn_service}\nEOF")
        
        # 9. 配置Nginx
        print("\n配置Nginx...")
        nginx_config = f"""server {{
    listen {WEB_PORT};
    server_name _;

    # 前端静态文件
    location / {{
        root {REMOTE_DIR}/frontend/dist;
        try_files $uri $uri/ /index.html;
    }}

    # API代理
    location /api/ {{
        proxy_pass http://127.0.0.1:{API_PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
        execute_command(ssh, f"cat > /etc/nginx/sites-available/httpProxy_web << 'EOF'\n{nginx_config}\nEOF")
        execute_command(ssh, "rm -f /etc/nginx/sites-enabled/httpProxy_web")
        execute_command(ssh, "ln -s /etc/nginx/sites-available/httpProxy_web /etc/nginx/sites-enabled/")
        execute_command(ssh, "rm -f /etc/nginx/sites-enabled/default || true")
        
        # 10. 启动服务
        print("\n启动服务...")
        execute_command(ssh, "systemctl daemon-reload")
        execute_command(ssh, "systemctl enable httpProxy_web")
        execute_command(ssh, "systemctl restart httpProxy_web")
        execute_command(ssh, "systemctl restart nginx")
        
        # 11. 检查服务状态
        print("\n检查服务状态...")
        time.sleep(2)
        execute_command(ssh, "systemctl status httpProxy_web --no-pager || true")
        execute_command(ssh, "systemctl status nginx --no-pager || true")
        
        print("\n部署完成！")
        print(f"Web访问地址: http://{SERVER_CONFIG['host']}:{WEB_PORT}")
        print(f"API访问地址: http://{SERVER_CONFIG['host']}:{API_PORT}")
        
        ssh.close()
        
        # 清理本地压缩包
        os.remove(tar_path)
        
    except Exception as e:
        print(f"部署失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    deploy()

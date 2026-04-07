#!/usr/bin/env python3
"""
修复权限问题
"""
import paramiko
from paramiko import SSHClient, AutoAddPolicy


SERVER_CONFIG = {
    'host': '8.137.176.50',
    'port': 22,
    'username': 'root',
    'password': 'YLtm9awnku7ps5fq'
}


def ssh_connect():
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(
        hostname=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        username=SERVER_CONFIG['username'],
        password=SERVER_CONFIG['password']
    )
    return ssh


def execute_command(ssh, command):
    print(f"--- 执行命令: {command} ---")
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    if output:
        print(output)
    if error:
        print(f"错误: {error}")
    return output, error


def fix():
    ssh = ssh_connect()
    try:
        print("=" * 50)
        print("将项目移动到 /var/www 目录")
        print("=" * 50)
        execute_command(ssh, "mkdir -p /var/www")
        execute_command(ssh, "mv /root/httpProxy_web /var/www/")
        execute_command(ssh, "chown -R www-data:www-data /var/www/httpProxy_web")
        execute_command(ssh, "chmod -R 755 /var/www/httpProxy_web")
        
        print("\n" + "=" * 50)
        print("更新 Gunicorn 服务配置")
        print("=" * 50)
        gunicorn_service = """[Unit]
Description=Gunicorn instance to serve httpProxy_web
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/httpProxy_web
Environment="PATH=/var/www/httpProxy_web/venv/bin"
ExecStart=/var/www/httpProxy_web/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8090 app:app

[Install]
WantedBy=multi-user.target
"""
        execute_command(ssh, f"cat > /etc/systemd/system/httpProxy_web.service << 'EOF'\n{gunicorn_service}\nEOF")
        
        print("\n" + "=" * 50)
        print("更新 Nginx 配置")
        print("=" * 50)
        nginx_config = """server {
    listen 8080;
    server_name _;

    # 前端静态文件
    location / {
        root /var/www/httpProxy_web/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
"""
        execute_command(ssh, f"cat > /etc/nginx/sites-available/httpProxy_web << 'EOF'\n{nginx_config}\nEOF")
        
        print("\n" + "=" * 50)
        print("重启服务")
        print("=" * 50)
        execute_command(ssh, "systemctl daemon-reload")
        execute_command(ssh, "systemctl restart httpProxy_web")
        execute_command(ssh, "systemctl restart nginx")
        
        print("\n" + "=" * 50)
        print("检查服务状态")
        print("=" * 50)
        import time
        time.sleep(2)
        execute_command(ssh, "systemctl status httpProxy_web --no-pager")
        execute_command(ssh, "systemctl status nginx --no-pager")
        
        print("\n权限修复完成！")
        
    finally:
        ssh.close()


if __name__ == '__main__':
    fix()

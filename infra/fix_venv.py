#!/usr/bin/env python3
"""
修复虚拟环境权限
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
        print("修复虚拟环境可执行文件权限")
        print("=" * 50)
        execute_command(ssh, "chmod -R 755 /var/www/httpProxy_web/venv/bin")
        
        print("\n" + "=" * 50)
        print("确保上传目录可写")
        print("=" * 50)
        execute_command(ssh, "chmod -R 775 /var/www/httpProxy_web/uploads")
        execute_command(ssh, "chown -R www-data:www-data /var/www/httpProxy_web/uploads")
        
        print("\n" + "=" * 50)
        print("更新服务配置，使用 root 用户运行后端（简化权限问题）")
        print("=" * 50)
        gunicorn_service = """[Unit]
Description=Gunicorn instance to serve httpProxy_web
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/httpProxy_web
Environment="PATH=/var/www/httpProxy_web/venv/bin"
ExecStart=/var/www/httpProxy_web/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8090 app:app

[Install]
WantedBy=multi-user.target
"""
        execute_command(ssh, f"cat > /etc/systemd/system/httpProxy_web.service << 'EOF'\n{gunicorn_service}\nEOF")
        
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
        
        print("\n修复完成！")
        
    finally:
        ssh.close()


if __name__ == '__main__':
    fix()

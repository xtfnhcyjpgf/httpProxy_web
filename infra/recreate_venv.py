#!/usr/bin/env python3
"""
重新创建虚拟环境
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
        print("删除并重新创建虚拟环境")
        print("=" * 50)
        execute_command(ssh, "cd /var/www/httpProxy_web && rm -rf venv")
        execute_command(ssh, "cd /var/www/httpProxy_web && python3 -m venv venv")
        execute_command(ssh, "cd /var/www/httpProxy_web && source venv/bin/activate && pip install -r requirements.txt gunicorn")
        
        print("\n" + "=" * 50)
        print("初始化数据库")
        print("=" * 50)
        execute_command(ssh, "cd /var/www/httpProxy_web && source venv/bin/activate && python3 -c \"from database import init_database; init_database()\"")
        
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
        time.sleep(3)
        execute_command(ssh, "systemctl status httpProxy_web --no-pager")
        execute_command(ssh, "systemctl status nginx --no-pager")
        
        print("\n完成！")
        
    finally:
        ssh.close()


if __name__ == '__main__':
    fix()

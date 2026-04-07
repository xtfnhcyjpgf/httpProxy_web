#!/usr/bin/env python3
"""
检查服务器日志
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


def check():
    ssh = ssh_connect()
    try:
        print("=" * 50)
        print("检查 Nginx 错误日志")
        print("=" * 50)
        execute_command(ssh, "tail -50 /var/log/nginx/error.log")
        
        print("\n" + "=" * 50)
        print("检查应用服务日志")
        print("=" * 50)
        execute_command(ssh, "journalctl -u httpProxy_web -n 100 --no-pager")
        
        print("\n" + "=" * 50)
        print("检查前端文件是否存在")
        print("=" * 50)
        execute_command(ssh, "ls -la /root/httpProxy_web/")
        execute_command(ssh, "ls -la /root/httpProxy_web/frontend/ || true")
        execute_command(ssh, "ls -la /root/httpProxy_web/frontend/dist/ || true")
        
    finally:
        ssh.close()


if __name__ == '__main__':
    check()

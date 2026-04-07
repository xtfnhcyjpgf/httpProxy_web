#!/usr/bin/env python3
"""
检查Nginx配置和日志
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
        print("查看Nginx配置文件")
        print("=" * 50)
        execute_command(ssh, "cat /etc/nginx/sites-available/httpProxy_web")
        
        print("\n" + "=" * 50)
        print("检查Nginx语法")
        print("=" * 50)
        execute_command(ssh, "nginx -t")
        
        print("\n" + "=" * 50)
        print("查看Nginx错误日志")
        print("=" * 50)
        execute_command(ssh, "tail -100 /var/log/nginx/error.log")
        
        print("\n" + "=" * 50)
        print("查看Nginx访问日志")
        print("=" * 50)
        execute_command(ssh, "tail -100 /var/log/nginx/access.log")
        
    finally:
        ssh.close()


if __name__ == '__main__':
    check()

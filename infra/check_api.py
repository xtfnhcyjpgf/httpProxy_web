#!/usr/bin/env python3
"""
检查API接口问题
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
        print("检查服务状态")
        print("=" * 50)
        execute_command(ssh, "systemctl status httpProxy_web --no-pager")
        execute_command(ssh, "systemctl status nginx --no-pager")
        
        print("\n" + "=" * 50)
        print("检查端口监听")
        print("=" * 50)
        execute_command(ssh, "netstat -tlnp || ss -tlnp || true")
        
        print("\n" + "=" * 50)
        print("检查防火墙状态")
        print("=" * 50)
        execute_command(ssh, "ufw status || iptables -L -n || true")
        
        print("\n" + "=" * 50)
        print("本地测试API健康检查")
        print("=" * 50)
        execute_command(ssh, "curl -s http://127.0.0.1:8090/api/health")
        
        print("\n" + "=" * 50)
        print("本地测试工单查询API")
        print("=" * 50)
        execute_command(ssh, "curl -X POST -s http://127.0.0.1:8090/api/work-orders/query -H 'Content-Type: application/json' -d '{\"orderIds\": []}'")
        
        print("\n" + "=" * 50)
        print("查看应用日志")
        print("=" * 50)
        execute_command(ssh, "journalctl -u httpProxy_web -n 50 --no-pager")
        
    finally:
        ssh.close()


if __name__ == '__main__':
    check()

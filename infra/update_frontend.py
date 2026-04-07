#!/usr/bin/env python3
"""
更新前端代码到服务器
"""
import paramiko
from paramiko import SSHClient, AutoAddPolicy
import os
import tarfile


SERVER_CONFIG = {
    'host': '8.137.176.50',
    'port': 22,
    'username': 'root',
    'password': 'YLtm9awnku7ps5fq'
}

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE_DIR = '/var/www/httpProxy_web'


def create_tar_archive():
    """创建前端压缩包"""
    print("正在创建前端压缩包...")
    tar_path = os.path.join(PROJECT_DIR, 'frontend.tar.gz')
    
    frontend_dist = os.path.join(PROJECT_DIR, 'frontend', 'dist')
    
    if not os.path.exists(frontend_dist):
        print(f"错误: 前端构建目录不存在: {frontend_dist}")
        print("请先运行 npm run build 构建前端")
        return None
    
    with tarfile.open(tar_path, 'w:gz') as tar:
        tar.add(frontend_dist, arcname='frontend/dist')
        
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


def update():
    """更新流程"""
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{REMOTE_DIR}/frontend_backup_{timestamp}"
    
    try:
        # 1. 创建压缩包
        tar_path = create_tar_archive()
        if not tar_path:
            return
        
        # 2. 连接服务器
        ssh = ssh_connect()
        
        # 3. 备份当前前端（使用时间戳目录）
        print(f"\n备份当前前端到 {backup_dir}...")
        execute_command(ssh, f"mkdir -p {backup_dir}")
        execute_command(ssh, f"cd {REMOTE_DIR} && cp -a frontend/dist/* {backup_dir}/ 2>/dev/null || true")
        execute_command(ssh, f"ls -la {backup_dir}/ || true")
        
        print(f"\n[OK] 备份已保存到: {backup_dir}")
        
        # 4. 上传压缩包
        remote_tar_path = f"{REMOTE_DIR}/frontend.tar.gz"
        upload_file(ssh, tar_path, remote_tar_path)
        
        # 5. 备份并替换前端
        print("\n替换前端文件...")
        execute_command(ssh, f"cd {REMOTE_DIR} && rm -rf frontend/dist.old || true")
        execute_command(ssh, f"cd {REMOTE_DIR} && mv -f frontend/dist frontend/dist.old 2>/dev/null || true")
        
        # 6. 解压文件
        print("\n解压文件...")
        execute_command(ssh, f"cd {REMOTE_DIR} && tar -xzf frontend.tar.gz")
        
        # 7. 设置权限
        print("\n设置权限...")
        execute_command(ssh, f"chown -R www-data:www-data {REMOTE_DIR}/frontend/dist")
        execute_command(ssh, f"chmod -R 755 {REMOTE_DIR}/frontend/dist")
        
        # 8. 清理
        print("\n清理...")
        execute_command(ssh, f"rm -f {REMOTE_DIR}/frontend.tar.gz")
        
        # 9. 验证
        print("\n验证文件...")
        execute_command(ssh, f"ls -la {REMOTE_DIR}/frontend/dist/")
        
        print("\n" + "=" * 60)
        print("[OK] 前端更新完成！")
        print("=" * 60)
        print(f"[OK] 备份位置: {backup_dir}")
        
        ssh.close()
        
        # 清理本地压缩包
        os.remove(tar_path)
        
    except Exception as e:
        print(f"\n[ERROR] 更新失败: {e}")
        import sys
        sys.exit(1)


if __name__ == '__main__':
    update()

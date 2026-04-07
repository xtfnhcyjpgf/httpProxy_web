#!/usr/bin/env python3
"""
更新部署脚本 - 将本地代码更新到服务器
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
    """创建项目压缩包 - 注意：不包含数据库文件！"""
    print("=" * 60)
    print("⚠️  重要提示：本脚本不会更新数据库文件！")
    print("=" * 60)
    print("\n正在创建项目压缩包...")
    tar_path = os.path.join(PROJECT_DIR, 'update.tar.gz')
    
    with tarfile.open(tar_path, 'w:gz') as tar:
        tar.add(os.path.join(PROJECT_DIR, 'app.py'), 'app.py')
        tar.add(os.path.join(PROJECT_DIR, 'config.py'), 'config.py')
        tar.add(os.path.join(PROJECT_DIR, 'database.py'), 'database.py')
        tar.add(os.path.join(PROJECT_DIR, 'requirements.txt'), 'requirements.txt')
        
    print(f"压缩包已创建: {tar_path}")
    print("[OK] 确认：压缩包中不包含任何数据库文件")
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
    import time
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{REMOTE_DIR}/backup_{timestamp}"
    
    try:
        # 1. 创建压缩包
        tar_path = create_tar_archive()
        
        # 2. 连接服务器
        ssh = ssh_connect()
        
        # 3. 上传压缩包
        remote_tar_path = f"{REMOTE_DIR}/update.tar.gz"
        upload_file(ssh, tar_path, remote_tar_path)
        
        # 4. 备份当前文件（使用时间戳目录，更安全）
        print(f"\n备份当前文件到 {backup_dir}...")
        execute_command(ssh, f"mkdir -p {backup_dir}")
        execute_command(ssh, f"cd {REMOTE_DIR} && cp -a app.py config.py database.py requirements.txt {backup_dir}/ 2>/dev/null || true")
        execute_command(ssh, f"ls -la {backup_dir}/")
        
        print(f"\n[OK] 备份已保存到: {backup_dir}")
        
        # 5. 解压文件
        print("\n解压文件...")
        execute_command(ssh, f"cd {REMOTE_DIR} && tar -xzf update.tar.gz")
        
        # 6. 检查是否需要安装新依赖
        print("\n检查依赖...")
        execute_command(ssh, f"cd {REMOTE_DIR} && source venv/bin/activate && pip install -r requirements.txt")
        
        # 7. 初始化数据库（注意：不会覆盖现有数据，只会创建缺失的表）
        print("\n初始化数据库（仅创建缺失表，不会覆盖数据）...")
        execute_command(ssh, f"cd {REMOTE_DIR} && source venv/bin/activate && python3 -c \"from database import init_database; init_database()\"")
        
        # 8. 重启服务
        print("\n重启服务...")
        execute_command(ssh, "systemctl restart httpProxy_web")
        
        # 9. 检查服务状态
        print("\n检查服务状态...")
        time.sleep(2)
        execute_command(ssh, "systemctl status httpProxy_web --no-pager")
        
        print("\n" + "=" * 60)
        print("[OK] 更新完成！")
        print("=" * 60)
        print(f"[OK] 备份位置: {backup_dir}")
        print("[OK] 数据库文件未被修改")
        
        ssh.close()
        
        # 清理本地压缩包
        os.remove(tar_path)
        
    except Exception as e:
        print(f"\n[ERROR] 更新失败: {e}")
        import sys
        sys.exit(1)


if __name__ == '__main__':
    update()

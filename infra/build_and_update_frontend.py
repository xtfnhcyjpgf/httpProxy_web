#!/usr/bin/env python3
"""
一键构建并更新前端到服务器
"""
import subprocess
import os
import sys


def build_frontend():
    """构建前端"""
    print("=" * 50)
    print("1. 构建前端")
    print("=" * 50)
    
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')
    
    try:
        import platform
        import sys
        encoding = sys.getdefaultencoding()
        
        if platform.system() == 'Windows':
            result = subprocess.run(
                ['cmd.exe', '/c', 'npm run build'],
                cwd=frontend_dir,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
        else:
            result = subprocess.run(
                ['npm', 'run', 'build'],
                cwd=frontend_dir,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print("\n[OK] 前端构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] 前端构建失败: {e}")
        if hasattr(e, 'stdout'):
            print(e.stdout)
        if hasattr(e, 'stderr'):
            print(e.stderr)
        return False


def update_frontend():
    """更新前端到服务器"""
    print("\n" + "=" * 50)
    print("2. 更新前端到服务器")
    print("=" * 50)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    update_script = os.path.join(script_dir, 'update_frontend.py')
    
    try:
        result = subprocess.run(
            [sys.executable, update_script],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] 更新失败: {e}")
        print(e.stdout)
        print(e.stderr)
        return False


if __name__ == '__main__':
    success = build_frontend()
    if success:
        update_frontend()

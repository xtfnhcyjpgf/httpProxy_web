"""
配置文件 - 包含数据库路径、SECRET_KEY等配置信息
所有配置从本文件读取，不硬编码
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')

# Flask配置
SECRET_KEY = 'httpProxy_web_secret_key_2024_change_in_production'
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
SESSION_USE_SIGNER = True

# CORS配置
CORS_ORIGINS = ['*']

# JWT配置
JWT_EXPIRATION_HOURS = 24

# 上传配置
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB最大文件大小

# 服务器地址配置（用于生成完整的图片访问URL）
SERVER_URL = 'http://8.137.176.50:8080'

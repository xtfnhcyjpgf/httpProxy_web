"""
数据库模块 - SQLite数据库初始化和操作
users表：id, username, password_hash, created_at（无外键）
work_orders表：工单主表
work_order_details表：工单详情
work_order_feedbacks表：操作记录（动态数组）
work_order_products表：产品信息（动态数组）
work_order_nodes表：节点记录
work_order_settlements表：结算记录（动态数组）
work_order_attachments表：附件表（分组多图片）
"""
import sqlite3
import bcrypt
import os
from datetime import datetime
from config import DATABASE_PATH


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """初始化数据库，创建所有表（无外键约束）"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 创建users表（无外键约束）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 创建work_orders表 - 工单主表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            orderid TEXT UNIQUE NOT NULL,
            new_orderid TEXT DEFAULT '',
            contact_name TEXT DEFAULT '',
            contact_phone TEXT DEFAULT '',
            created_date TEXT DEFAULT '',
            appoint_begin_time TEXT DEFAULT '',
            appoint_end_time TEXT DEFAULT '',
            work_order_complete_time TEXT DEFAULT '',
            last_evaluation_time TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 为已存在的work_orders表添加new_orderid字段（如果不存在）
    try:
        cursor.execute('ALTER TABLE work_orders ADD COLUMN new_orderid TEXT DEFAULT ""')
    except:
        pass

    # 创建work_order_details表 - 工单详情（无外键）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_order_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_order_id INTEGER NOT NULL,
            evaluation_time TEXT DEFAULT '',
            expect_door_to_door_begin_time TEXT DEFAULT '',
            expect_door_to_door_end_time TEXT DEFAULT '',
            delivery_time TEXT DEFAULT '',
            sign_in_location TEXT DEFAULT ''
        )
    ''')

    # 创建work_order_feedbacks表 - 操作记录（动态数组，无外键）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_order_feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_order_id INTEGER NOT NULL,
            feedback_index INTEGER NOT NULL,
            last_modified_date TEXT DEFAULT '',
            content TEXT DEFAULT ''
        )
    ''')

    # 创建work_order_products表 - 产品信息（动态数组，无外键）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_order_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_order_id INTEGER NOT NULL,
            product_index INTEGER NOT NULL,
            buy_time TEXT DEFAULT ''
        )
    ''')

    # 创建work_order_nodes表 - 节点记录（无外键）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_order_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_order_id INTEGER NOT NULL,
            node_type TEXT NOT NULL,
            node_index INTEGER NOT NULL,
            created_date TEXT DEFAULT ''
        )
    ''')

    # 创建work_order_settlements表 - 结算记录（动态数组，无外键）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_order_settlements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_order_id INTEGER NOT NULL,
            settlement_index INTEGER NOT NULL,
            fksj TEXT DEFAULT '',
            gmsj TEXT DEFAULT '',
            scazsj TEXT DEFAULT ''
        )
    ''')

    # 创建work_order_attachments表 - 附件表（分组多图片，无外键）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_order_attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_order_id INTEGER NOT NULL,
            attachment_group INTEGER NOT NULL,
            annex_name TEXT DEFAULT '',
            image_file_path TEXT DEFAULT ''
        )
    ''')

    # 检查是否已存在admin账号，不存在则创建
    cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',))
    if cursor.fetchone() is None:
        # 使用bcrypt加密密码
        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            ('admin', password_hash.decode('utf-8'))
        )
        print("已创建默认管理员账号: admin/admin123")

    conn.commit()
    conn.close()


def verify_user(username, password):
    """验证用户账号密码"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return {'id': user['id'], 'username': user['username']}
    return None


def get_all_users():
    """获取所有用户（不包含密码）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, created_at FROM users ORDER BY id')
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]


def create_user(username, password):
    """创建新用户"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 检查用户名是否已存在
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return None, "用户名已存在"

    # 使用bcrypt加密密码
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash.decode('utf-8'))
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {'id': user_id, 'username': username}, None
    except Exception as e:
        conn.close()
        return None, str(e)


def update_user_password(user_id, new_password):
    """更新用户密码"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 使用bcrypt加密新密码
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            'UPDATE users SET password_hash = ? WHERE id = ?',
            (password_hash.decode('utf-8'), user_id)
        )
        conn.commit()
        affected = cursor.rowcount
        conn.close()

        if affected > 0:
            return True, None
        return False, "用户不存在"
    except Exception as e:
        conn.close()
        return False, str(e)


def delete_user(user_id):
    """删除用户"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()

        if affected > 0:
            return True, None
        return False, "用户不存在"
    except Exception as e:
        conn.close()
        return False, str(e)


# ==================== 工单相关函数 ====================

def create_work_order(order_data):
    """创建工单及其关联数据
    适配前端发送的驼峰命名、扁平结构数据格式
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 插入工单主表（前端发送扁平格式：contactName, createdDate等）
        cursor.execute('''
            INSERT INTO work_orders (orderid, new_orderid, contact_name, contact_phone, created_date,
                appoint_begin_time, appoint_end_time, work_order_complete_time, last_evaluation_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_data.get('orderid', ''),
            order_data.get('newOrderid', ''),
            order_data.get('contactName', ''),
            order_data.get('contactPhone', ''),
            order_data.get('createdDate', ''),
            order_data.get('appointmentStartTime', ''),
            order_data.get('appointmentEndTime', ''),
            order_data.get('completeTime', ''),
            order_data.get('evaluationTime', '')
        ))
        work_order_id = cursor.lastrowid

        # 插入工单详情（前端发送扁平格式：expectedStartTime, outboundTime等）
        cursor.execute('''
            INSERT INTO work_order_details (work_order_id, evaluation_time,
                expect_door_to_door_begin_time, expect_door_to_door_end_time,
                delivery_time, sign_in_location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            work_order_id,
            order_data.get('evaluationTime', ''),
            order_data.get('expectedStartTime', ''),
            order_data.get('expectedEndTime', ''),
            order_data.get('outboundTime', ''),
            order_data.get('signInLocation', '')
        ))

        # 插入操作记录（前端发送：operationRecords数组，每项有lastModifiedDate, content）
        operation_records = order_data.get('operationRecords', [])
        for idx, fb in enumerate(operation_records):
            cursor.execute('''
                INSERT INTO work_order_feedbacks (work_order_id, feedback_index, last_modified_date, content)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, idx, fb.get('lastModifiedDate', ''), fb.get('content', '')))

        # 插入产品信息（前端发送：products数组，每项有buyTime）
        products = order_data.get('products', [])
        for idx, prod in enumerate(products):
            cursor.execute('''
                INSERT INTO work_order_products (work_order_id, product_index, buy_time)
                VALUES (?, ?, ?)
            ''', (work_order_id, idx, prod.get('buyTime', '')))

        # 插入节点记录
        # completeFeedbackList: 网点完工（4条）
        complete_list = order_data.get('completeFeedbackList', [])
        for idx, node in enumerate(complete_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'complete', idx, node.get('createdDate', '')))

        # createdFeedbackList: 创建时间（1条）
        created_list = order_data.get('createdFeedbackList', [])
        for idx, node in enumerate(created_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'created', idx, node.get('createdDate', '')))

        # inServiceFeedbackList: 服务中（3条）
        in_service_list = order_data.get('inServiceFeedbackList', [])
        for idx, node in enumerate(in_service_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'inService', idx, node.get('createdDate', '')))

        # sendOrdersFeedbackList: 派单（3条）
        send_orders_list = order_data.get('sendOrdersFeedbackList', [])
        for idx, node in enumerate(send_orders_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'sendOrders', idx, node.get('createdDate', '')))

        # 插入结算记录（前端发送：settlementList数组，每项有fksj, gmsj, scazsj）
        settlements = order_data.get('settlementList', [])
        for idx, settlement in enumerate(settlements):
            cursor.execute('''
                INSERT INTO work_order_settlements (work_order_id, settlement_index, fksj, gmsj, scazsj)
                VALUES (?, ?, ?, ?, ?)
            ''', (work_order_id, idx, settlement.get('fksj', ''), settlement.get('gmsj', ''), settlement.get('scazsj', '')))

        # 插入附件（前端发送：attachmentGroups数组，每组有imgreplace）
        # attachmentGroups格式: [{imgreplace: [{annexName, imageFilePath}, ...]}, ...]
        attachment_groups = order_data.get('attachmentGroups', [])
        for group_idx, group in enumerate(attachment_groups):
            imgreplace = group.get('imgreplace', [])
            for att in imgreplace:
                if isinstance(att, dict):
                    annex_name = att.get('annexName', '')
                    image_path = att.get('imageFilePath', '')
                else:
                    annex_name = ''
                    image_path = att
                cursor.execute('''
                    INSERT INTO work_order_attachments (work_order_id, attachment_group, annex_name, image_file_path)
                    VALUES (?, ?, ?, ?)
                ''', (work_order_id, group_idx, annex_name, image_path))

        conn.commit()
        conn.close()
        return {'id': work_order_id, 'orderid': order_data.get('orderid', '')}, None
    except Exception as e:
        conn.close()
        return None, str(e)


def get_work_order_by_id(work_order_id):
    """根据ID获取工单详情"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取工单主表
    cursor.execute('SELECT * FROM work_orders WHERE id = ?', (work_order_id,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        return None

    result = dict(order)

    # 获取工单详情
    cursor.execute('SELECT * FROM work_order_details WHERE work_order_id = ?', (work_order_id,))
    detail = cursor.fetchone()
    if detail:
        result['detail'] = dict(detail)

    # 获取操作记录（按索引排序）
    cursor.execute('SELECT * FROM work_order_feedbacks WHERE work_order_id = ? ORDER BY feedback_index', (work_order_id,))
    feedbacks = [dict(row) for row in cursor.fetchall()]
    result['feedbacks'] = feedbacks

    # 获取产品信息（按索引排序）
    cursor.execute('SELECT * FROM work_order_products WHERE work_order_id = ? ORDER BY product_index', (work_order_id,))
    products = [dict(row) for row in cursor.fetchall()]
    result['products'] = products

    # 获取节点记录（按类型和索引排序）
    cursor.execute('SELECT * FROM work_order_nodes WHERE work_order_id = ? ORDER BY node_type, node_index', (work_order_id,))
    nodes = [dict(row) for row in cursor.fetchall()]
    result['nodes'] = nodes

    # 获取结算记录（按索引排序）
    cursor.execute('SELECT * FROM work_order_settlements WHERE work_order_id = ? ORDER BY settlement_index', (work_order_id,))
    settlements = [dict(row) for row in cursor.fetchall()]
    result['settlements'] = settlements

    # 获取附件（按分组和索引排序）
    cursor.execute('SELECT * FROM work_order_attachments WHERE work_order_id = ? ORDER BY attachment_group', (work_order_id,))
    attachments_raw = [dict(row) for row in cursor.fetchall()]

    # 按分组组织附件
    attachments_dict = {}
    for att in attachments_raw:
        group = att['attachment_group']
        if group not in attachments_dict:
            attachments_dict[group] = []
        attachments_dict[group].append({
            'annexName': att['annex_name'],
            'imageFilePath': att['image_file_path']
        })

    # 转换为 imgreplace 格式
    attachments = []
    for group_idx in sorted(attachments_dict.keys()):
        attachments.append({'imgreplace': attachments_dict[group_idx]})
    result['attachments'] = attachments

    conn.close()
    return result


def get_work_order_by_orderid(orderid):
    """根据orderid获取工单"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM work_orders WHERE orderid = ?', (orderid,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        return None

    conn.close()
    return get_work_order_by_id(order['id'])


def get_all_work_orders():
    """获取所有工单列表（不含详情）"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM work_orders ORDER BY orderid')
    orders = cursor.fetchall()

    conn.close()
    return [dict(order) for order in orders]


def update_work_order(work_order_id, order_data):
    """更新工单及其关联数据
    适配前端发送的驼峰命名、扁平结构数据格式
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 更新工单主表（前端发送扁平格式：contactName, createdDate等）
        cursor.execute('''
            UPDATE work_orders SET
                new_orderid = ?,
                contact_name = ?,
                contact_phone = ?,
                created_date = ?,
                appoint_begin_time = ?,
                appoint_end_time = ?,
                work_order_complete_time = ?,
                last_evaluation_time = ?
            WHERE id = ?
        ''', (
            order_data.get('newOrderid', ''),
            order_data.get('contactName', ''),
            order_data.get('contactPhone', ''),
            order_data.get('createdDate', ''),
            order_data.get('appointmentStartTime', ''),
            order_data.get('appointmentEndTime', ''),
            order_data.get('completeTime', ''),
            order_data.get('evaluationTime', ''),
            work_order_id
        ))

        # 更新工单详情 - 先删除再插入
        cursor.execute('DELETE FROM work_order_details WHERE work_order_id = ?', (work_order_id,))
        cursor.execute('''
            INSERT INTO work_order_details (work_order_id, evaluation_time,
                expect_door_to_door_begin_time, expect_door_to_door_end_time,
                delivery_time, sign_in_location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            work_order_id,
            order_data.get('evaluationTime', ''),
            order_data.get('expectedStartTime', ''),
            order_data.get('expectedEndTime', ''),
            order_data.get('outboundTime', ''),
            order_data.get('signInLocation', '')
        ))

        # 更新操作记录 - 先删除再插入
        cursor.execute('DELETE FROM work_order_feedbacks WHERE work_order_id = ?', (work_order_id,))
        operation_records = order_data.get('operationRecords', [])
        for idx, fb in enumerate(operation_records):
            cursor.execute('''
                INSERT INTO work_order_feedbacks (work_order_id, feedback_index, last_modified_date, content)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, idx, fb.get('lastModifiedDate', ''), fb.get('content', '')))

        # 更新产品信息 - 先删除再插入
        cursor.execute('DELETE FROM work_order_products WHERE work_order_id = ?', (work_order_id,))
        products = order_data.get('products', [])
        for idx, prod in enumerate(products):
            cursor.execute('''
                INSERT INTO work_order_products (work_order_id, product_index, buy_time)
                VALUES (?, ?, ?)
            ''', (work_order_id, idx, prod.get('buyTime', '')))

        # 更新节点记录 - 先删除再插入
        cursor.execute('DELETE FROM work_order_nodes WHERE work_order_id = ?', (work_order_id,))

        # completeFeedbackList: 网点完工
        complete_list = order_data.get('completeFeedbackList', [])
        for idx, node in enumerate(complete_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'complete', idx, node.get('createdDate', '')))

        # createdFeedbackList: 创建时间
        created_list = order_data.get('createdFeedbackList', [])
        for idx, node in enumerate(created_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'created', idx, node.get('createdDate', '')))

        # inServiceFeedbackList: 服务中
        in_service_list = order_data.get('inServiceFeedbackList', [])
        for idx, node in enumerate(in_service_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'inService', idx, node.get('createdDate', '')))

        # sendOrdersFeedbackList: 派单
        send_orders_list = order_data.get('sendOrdersFeedbackList', [])
        for idx, node in enumerate(send_orders_list):
            cursor.execute('''
                INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, 'sendOrders', idx, node.get('createdDate', '')))

        # 更新结算记录 - 先删除再插入
        cursor.execute('DELETE FROM work_order_settlements WHERE work_order_id = ?', (work_order_id,))
        settlements = order_data.get('settlementList', [])
        for idx, settlement in enumerate(settlements):
            cursor.execute('''
                INSERT INTO work_order_settlements (work_order_id, settlement_index, fksj, gmsj, scazsj)
                VALUES (?, ?, ?, ?, ?)
            ''', (work_order_id, idx, settlement.get('fksj', ''), settlement.get('gmsj', ''), settlement.get('scazsj', '')))

        # 更新附件 - 先删除再插入
        # attachmentGroups格式: [{imgreplace: [{annexName, imageFilePath}, ...]}, ...]
        cursor.execute('DELETE FROM work_order_attachments WHERE work_order_id = ?', (work_order_id,))
        attachment_groups = order_data.get('attachmentGroups', [])
        for group_idx, group in enumerate(attachment_groups):
            imgreplace = group.get('imgreplace', [])
            for att in imgreplace:
                if isinstance(att, dict):
                    annex_name = att.get('annexName', '')
                    image_path = att.get('imageFilePath', '')
                else:
                    annex_name = ''
                    image_path = att
                cursor.execute('''
                    INSERT INTO work_order_attachments (work_order_id, attachment_group, annex_name, image_file_path)
                    VALUES (?, ?, ?, ?)
                ''', (work_order_id, group_idx, annex_name, image_path))

        conn.commit()
        conn.close()
        return {'id': work_order_id, 'orderid': order_data.get('orderid', '')}, None
    except Exception as e:
        conn.close()
        return None, str(e)


def delete_work_order(work_order_id):
    """删除工单及所有关联数据和图片文件"""
    from config import UPLOAD_FOLDER

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 先获取所有附件图片路径
        cursor.execute('SELECT image_file_path FROM work_order_attachments WHERE work_order_id = ?', (work_order_id,))
        attachments = cursor.fetchall()

        # 删除数据库记录（按顺序删除子表，最后删除主表）
        cursor.execute('DELETE FROM work_order_attachments WHERE work_order_id = ?', (work_order_id,))
        cursor.execute('DELETE FROM work_order_settlements WHERE work_order_id = ?', (work_order_id,))
        cursor.execute('DELETE FROM work_order_nodes WHERE work_order_id = ?', (work_order_id,))
        cursor.execute('DELETE FROM work_order_products WHERE work_order_id = ?', (work_order_id,))
        cursor.execute('DELETE FROM work_order_feedbacks WHERE work_order_id = ?', (work_order_id,))
        cursor.execute('DELETE FROM work_order_details WHERE work_order_id = ?', (work_order_id,))
        cursor.execute('DELETE FROM work_orders WHERE id = ?', (work_order_id,))

        conn.commit()
        conn.close()

        # 删除图片文件
        for att in attachments:
            if att['image_file_path']:
                file_path = os.path.join(UPLOAD_FOLDER, att['image_file_path'])
                if os.path.exists(file_path):
                    os.remove(file_path)

        return True, None
    except Exception as e:
        conn.close()
        return False, str(e)


def search_work_orders(keyword=None, contact_name=None, contact_phone=None,
                       created_date_from=None, created_date_to=None,
                       orderid=None):
    """条件查询工单"""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM work_orders WHERE 1=1'
    params = []

    if orderid:
        query += ' AND orderid = ?'
        params.append(orderid)

    if keyword:
        query += ' AND (orderid LIKE ? OR contact_name LIKE ? OR contact_phone LIKE ?)'
        params.extend([f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'])

    if contact_name:
        query += ' AND contact_name LIKE ?'
        params.append(f'%{contact_name}%')

    if contact_phone:
        query += ' AND contact_phone LIKE ?'
        params.append(f'%{contact_phone}%')

    if created_date_from:
        query += ' AND created_date >= ?'
        params.append(created_date_from)

    if created_date_to:
        query += ' AND created_date <= ?'
        params.append(created_date_to)

    query += ' ORDER BY orderid'

    cursor.execute(query, params)
    orders = cursor.fetchall()
    conn.close()

    return [dict(order) for order in orders]


def batch_query_work_orders(order_ids):
    """批量查询工单（用于外部调用，返回order.txt格式）"""
    if not order_ids:
        return {}

    conn = get_db_connection()
    cursor = conn.cursor()

    # 获取工单列表，按orderid排序
    placeholders = ','.join(['?'] * len(order_ids))
    cursor.execute(f'SELECT * FROM work_orders WHERE orderid IN ({placeholders}) ORDER BY orderid', order_ids)
    orders = cursor.fetchall()

    if not orders:
        conn.close()
        return {}

    result = {}

    for order in orders:
        order_data = dict(order)
        work_order_id = order_data['id']
        orderid = order_data['orderid']

        # 构建单个工单的order.txt格式
        order_result = {
            'orderid': orderid,
            'searchWorkOrderListEs': [],
            'searchWorkOrderDetail': [],
            'getWorkOrderDetailList': [],
            'searchWorkOrderNodeResp': [],
            'searchAzWgmxDetail': [],
            'download': []
        }

        # searchWorkOrderListEs - 工单主表信息
        order_result['searchWorkOrderListEs'] = [
            {'key': 'id', 'value': order_data.get('new_orderid', ''), 'path': 'data', 'info': '新工单编号'},
            {'key': 'contactName', 'value': order_data.get('contact_name', ''), 'path': 'data', 'info': '联系人姓名'},
            {'key': 'contactPhone', 'value': order_data.get('contact_phone', ''), 'path': 'data', 'info': '联系人手机号'},
            {'key': 'createdDate', 'value': order_data.get('created_date', ''), 'path': 'data', 'info': '创建时间'},
            {'key': 'appointBeginTime', 'value': order_data.get('appoint_begin_time', ''), 'path': 'data', 'info': '预约开始时间'},
            {'key': 'appointEndTime', 'value': order_data.get('appoint_end_time', ''), 'path': 'data', 'info': '预约结束时间'},
            {'key': 'workOrderCompleteTime', 'value': order_data.get('work_order_complete_time', ''), 'path': 'data', 'info': '完工时间'},
            {'key': 'lastEvaluationTime', 'value': order_data.get('last_evaluation_time', ''), 'path': 'data', 'info': '评价时间'}
        ]

        # 获取详情信息
        cursor.execute('SELECT * FROM work_order_details WHERE work_order_id = ?', (work_order_id,))
        detail = cursor.fetchone()

        # searchWorkOrderDetail
        detail_dict = dict(detail) if detail else {}
        feedbacks_list = []

        # 获取操作记录（按索引排序）
        cursor.execute('SELECT * FROM work_order_feedbacks WHERE work_order_id = ? ORDER BY feedback_index', (work_order_id,))
        feedbacks = cursor.fetchall()

        for fb in feedbacks:
            fb_dict = dict(fb)
            feedbacks_list.append({
                'key': 'lastModifiedDate',
                'value': fb_dict.get('last_modified_date', ''),
                'path': f'data.workOrderFeedbackRespList[{fb_dict.get("feedback_index", 0)}]',
                'info': f'操作记录时间{fb_dict.get("feedback_index", 0) + 1}'
            })
            feedbacks_list.append({
                'key': 'content',
                'value': fb_dict.get('content', ''),
                'path': f'data.workOrderFeedbackRespList[{fb_dict.get("feedback_index", 0)}]',
                'info': f'操作内容{fb_dict.get("feedback_index", 0) + 1}'
            })

        # searchWorkOrderDetail - 预约时间从主表order_data获取，详情从detail表获取
        order_result['searchWorkOrderDetail'] = [
            {'key': 'evaluationTime', 'value': detail_dict.get('evaluation_time', ''), 'path': 'data.workOrderEvaluationRespList', 'info': '评价时间'},
            {'key': 'appointBeginTime', 'value': order_data.get('appoint_begin_time', ''), 'path': 'data.workOrderResp', 'info': '预约开始时间'},
            {'key': 'appointEndTime', 'value': order_data.get('appoint_end_time', ''), 'path': 'data.workOrderResp', 'info': '结束预约时间'},
            {'key': 'expectDoorToDoorBeginTime', 'value': detail_dict.get('expect_door_to_door_begin_time', ''), 'path': 'data.workOrderResp', 'info': '期望上门开始时间'},
            {'key': 'expectDoorToDoorEndTime', 'value': detail_dict.get('expect_door_to_door_end_time', ''), 'path': 'data.workOrderResp', 'info': '期望上门结束时间'},
            {'key': 'deliveryTime', 'value': detail_dict.get('delivery_time', ''), 'path': 'data.workOrderResp', 'info': '出库时间'},
            {'key': 'signInLocation', 'value': detail_dict.get('sign_in_location', ''), 'path': 'data.workOrderResp', 'info': '签到定位'}
        ] + feedbacks_list

        # getWorkOrderDetailList - 产品信息
        cursor.execute('SELECT * FROM work_order_products WHERE work_order_id = ? ORDER BY product_index', (work_order_id,))
        products = cursor.fetchall()
        for prod in products:
            prod_dict = dict(prod)
            order_result['getWorkOrderDetailList'].append({
                'key': 'buyTime',
                'value': prod_dict.get('buy_time', ''),
                'path': f'data.workOrderDetailProductInfoVOList[{prod_dict.get("product_index", 0)}]',
                'info': f'产品{prod_dict.get("product_index", 0) + 1}购买时间'
            })

        # searchWorkOrderNodeResp - 节点记录
        cursor.execute('SELECT * FROM work_order_nodes WHERE work_order_id = ? ORDER BY node_type, node_index', (work_order_id,))
        nodes = cursor.fetchall()

        complete_list = []
        created_list = []
        in_service_list = []
        send_orders_list = []

        for node in nodes:
            node_dict = dict(node)
            node_type = node_dict.get('node_type', '')
            node_info = {
                'key': 'createdDate',
                'value': node_dict.get('created_date', ''),
                'path': '',
                'info': ''
            }

            if node_type == 'complete':
                node_info['path'] = f'data.completeFeedbackList[{node_dict.get("node_index", 0)}]'
                node_info['info'] = '网点完工时间'
                complete_list.append(node_info)
            elif node_type == 'created':
                node_info['path'] = f'data.createdFeedbackList[{node_dict.get("node_index", 0)}]'
                node_info['info'] = '创建时间'
                created_list.append(node_info)
            elif node_type == 'inService':
                node_info['path'] = f'data.inServiceFeedbackList[{node_dict.get("node_index", 0)}]'
                node_info['info'] = '服务中时间'
                in_service_list.append(node_info)
            elif node_type == 'sendOrders':
                node_info['path'] = f'data.sendOrdersFeedbackList[{node_dict.get("node_index", 0)}]'
                node_info['info'] = '派单时间'
                send_orders_list.append(node_info)

        order_result['searchWorkOrderNodeResp'] = complete_list + created_list + in_service_list + send_orders_list

        # searchAzWgmxDetail - 结算记录
        cursor.execute('SELECT * FROM work_order_settlements WHERE work_order_id = ? ORDER BY settlement_index', (work_order_id,))
        settlements = cursor.fetchall()

        settlement_list = []
        gmsj = ''
        scazsj = ''

        for settlement in settlements:
            settlement_dict = dict(settlement)
            settlement_list.append({
                'key': 'fksj',
                'value': settlement_dict.get('fksj', ''),
                'path': f"data.azdMxSpgcList[{settlement_dict.get('settlement_index', 0)}]",
                'info': f"结算单查询-操作时间{settlement_dict.get('settlement_index', 0) + 1}"
            })
            if settlement_dict.get('gmsj'):
                gmsj = settlement_dict.get('gmsj', '')
            if settlement_dict.get('scazsj'):
                scazsj = settlement_dict.get('scazsj', '')

        order_result['searchAzWgmxDetail'] = settlement_list + [
            {'key': 'gmsj', 'value': gmsj, 'path': 'data', 'info': '结算单查询-购买时间'},
            {'key': 'scazsj', 'value': scazsj, 'path': 'data', 'info': '结算单查询-安装时间'}
        ]

        # download - 附件
        cursor.execute('SELECT * FROM work_order_attachments WHERE work_order_id = ? ORDER BY attachment_group', (work_order_id,))
        attachments_raw = cursor.fetchall()

        attachments_dict = {}
        for att in attachments_raw:
            att_dict = dict(att)
            group = att_dict.get('attachment_group', 0)
            if group not in attachments_dict:
                attachments_dict[group] = []
            attachments_dict[group].append({
                'annexName': att_dict.get('annex_name', ''),
                'imageFilePath': att_dict.get('image_file_path', '')
            })

        download_list = []
        for group_idx in sorted(attachments_dict.keys()):
            download_list.append({'imgreplace': attachments_dict[group_idx]})

        if not download_list:
            download_list = [{'imgreplace': []}]

        order_result['download'] = download_list

        # 合并到结果（按orderid）
        result[orderid] = order_result

    conn.close()
    return result


def get_work_order_id_by_orderid(orderid):
    """根据orderid获取工单ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM work_orders WHERE orderid = ?', (orderid,))
    order = cursor.fetchone()
    conn.close()

    return order['id'] if order else None


def work_order_exists(orderid):
    """检查工单号是否已存在"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as count FROM work_orders WHERE orderid = ?', (orderid,))
    result = cursor.fetchone()
    conn.close()

    return result['count'] > 0 if result else False


def download_image(url):
    """下载远程图片到本地目录，返回本地文件名
    如果url不是HTTP地址，返回空字符串
    """
    import requests
    import os

    if not url or not url.startswith(('http://', 'https://')):
        return ''

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'image' in content_type:
                ext = '.png'
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'gif' in content_type:
                    ext = '.gif'
                elif 'webp' in content_type:
                    ext = '.webp'

                filename = f"{uuid.uuid4().hex}{ext}"
                file_path = os.path.join(os.path.dirname(__file__), 'uploads', filename)

                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                return filename
    except Exception as e:
        print(f"下载图片失败: {url}, 错误: {e}")

    return ''


def create_work_order_from_upload(order_data):
    """从第三方上传的数据格式创建工单
    解析扁平化的key-value格式数据
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        orderid = order_data.get('orderid', '')

        search_list_es = order_data.get('searchWorkOrderListEs', [])
        basic_data = {}
        for item in search_list_es:
            key = item.get('key', '')
            value = item.get('value', '')
            if key:
                basic_data[key] = value

        search_detail = order_data.get('searchWorkOrderDetail', [])
        detail_data = {}
        for item in search_detail:
            key = item.get('key', '')
            value = item.get('value', '')
            if key:
                detail_data[key] = value

        cursor.execute('''
            INSERT INTO work_orders (orderid, new_orderid, contact_name, contact_phone, created_date,
                appoint_begin_time, appoint_end_time, work_order_complete_time, last_evaluation_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            orderid,
            basic_data.get('newOrderid', ''),
            basic_data.get('contactName', ''),
            basic_data.get('contactPhone', ''),
            basic_data.get('createdDate', ''),
            basic_data.get('appointBeginTime', ''),
            basic_data.get('appointEndTime', ''),
            basic_data.get('workOrderCompleteTime', ''),
            basic_data.get('lastEvaluationTime', '')
        ))
        work_order_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO work_order_details (work_order_id, evaluation_time,
                expect_door_to_door_begin_time, expect_door_to_door_end_time,
                delivery_time, sign_in_location)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            work_order_id,
            detail_data.get('evaluationTime', ''),
            detail_data.get('expectDoorToDoorBeginTime', ''),
            detail_data.get('expectDoorToDoorEndTime', ''),
            detail_data.get('deliveryTime', ''),
            detail_data.get('signInLocation', '')
        ))

        feedbacks = order_data.get('searchWorkOrderDetail', [])
        feedback_index_map = {}
        current_idx = 0
        for fb in feedbacks:
            if fb.get('key') == 'lastModifiedDate':
                path = fb.get('path', '')
                import re
                match = re.search(r'\[(\d+)\]', path)
                if match:
                    current_idx = int(match.group(1))
                feedback_index_map[current_idx] = {'lastModifiedDate': fb.get('value', ''), 'content': ''}
            elif fb.get('key') == 'content':
                path = fb.get('path', '')
                import re
                match = re.search(r'\[(\d+)\]', path)
                if match:
                    idx = int(match.group(1))
                    if idx in feedback_index_map:
                        feedback_index_map[idx]['content'] = fb.get('value', '')

        for idx in sorted(feedback_index_map.keys()):
            fb_data = feedback_index_map[idx]
            cursor.execute('''
                INSERT INTO work_order_feedbacks (work_order_id, feedback_index, last_modified_date, content)
                VALUES (?, ?, ?, ?)
            ''', (work_order_id, idx, fb_data.get('lastModifiedDate', ''), fb_data.get('content', '')))

        products = order_data.get('getWorkOrderDetailList', [])
        for prod in products:
            if prod.get('key') == 'buyTime':
                path = prod.get('path', '')
                import re
                match = re.search(r'\[(\d+)\]', path)
                idx = int(match.group(1)) if match else 0
                cursor.execute('''
                    INSERT INTO work_order_products (work_order_id, product_index, buy_time)
                    VALUES (?, ?, ?)
                ''', (work_order_id, idx, prod.get('value', '')))

        nodes = order_data.get('searchWorkOrderNodeResp', [])
        for node in nodes:
            node_type = None
            path = node.get('path', '')
            if 'completeFeedbackList' in path:
                node_type = 'complete'
            elif 'createdFeedbackList' in path:
                node_type = 'created'
            elif 'inServiceFeedbackList' in path:
                node_type = 'inService'
            elif 'sendOrdersFeedbackList' in path:
                node_type = 'sendOrders'

            if node_type:
                import re
                match = re.search(r'\[(\d+)\]', path)
                node_idx = int(match.group(1)) if match else 0
                cursor.execute('''
                    INSERT INTO work_order_nodes (work_order_id, node_type, node_index, created_date)
                    VALUES (?, ?, ?, ?)
                ''', (work_order_id, node_type, node_idx, node.get('value', '')))

        settlements = order_data.get('searchAzWgmxDetail', [])
        gmsj = ''
        scazsj = ''
        fksj_list = []

        for settlement in settlements:
            key = settlement.get('key', '')
            value = settlement.get('value', '')
            path = settlement.get('path', '')

            if key == 'gmsj':
                gmsj = value
            elif key == 'scazsj':
                scazsj = value
            elif key == 'fksj' and 'azdMxSpgcList' in path:
                import re
                match = re.search(r'\[(\d+)\]', path)
                idx = int(match.group(1)) if match else len(fksj_list)
                while len(fksj_list) <= idx:
                    fksj_list.append('')
                fksj_list[idx] = value

        for idx, fksj in enumerate(fksj_list):
            cursor.execute('''
                INSERT INTO work_order_settlements (work_order_id, settlement_index, fksj, gmsj, scazsj)
                VALUES (?, ?, ?, ?, ?)
            ''', (work_order_id, idx, fksj, gmsj, scazsj))

        downloads = order_data.get('download', [])
        for group_idx, group in enumerate(downloads):
            imgreplace = group.get('imgreplace', [])
            for img in imgreplace:
                annex_name = img.get('annexName', '')
                image_url = img.get('imageFilePath', '')
                local_filename = download_image(image_url)
                cursor.execute('''
                    INSERT INTO work_order_attachments (work_order_id, attachment_group, annex_name, image_file_path)
                    VALUES (?, ?, ?, ?)
                ''', (work_order_id, group_idx, annex_name, local_filename))

        conn.commit()
        conn.close()
        return {'id': work_order_id, 'orderid': orderid}, None

    except Exception as e:
        conn.close()
        return None, str(e)


# 初始化数据库
if __name__ == '__main__':
    init_database()

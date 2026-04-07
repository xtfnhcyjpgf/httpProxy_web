"""
Flask应用入口 - 提供REST API服务
包含用户登录、退出、账号管理、工单管理等功能
"""
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from functools import wraps
from werkzeug.utils import secure_filename
import os
import uuid
from config import SECRET_KEY, CORS_ORIGINS, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH, SERVER_URL
from database import (
    init_database,
    verify_user,
    get_all_users,
    create_user,
    update_user_password,
    delete_user,
    create_work_order,
    get_work_order_by_id,
    get_work_order_by_orderid,
    get_all_work_orders,
    update_work_order,
    delete_work_order,
    search_work_orders,
    batch_query_work_orders,
    get_work_order_id_by_orderid,
    work_order_exists,
    create_work_order_from_upload,
    get_config_value,
    set_config_value,
    get_work_orders_with_new_orderid
)

# 初始化Flask应用
# 设置static_folder指向前端构建目录，url_path设为空使根路径访问index.html
frontend_dist = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
app = Flask(__name__, static_folder=frontend_dist, static_url_path='')
app.secret_key = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CORS跨域支持
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})


# ============ 辅助函数 ============

def get_base_url():
    """获取服务器配置的基础URL（协议+主机+端口）"""
    return SERVER_URL.rstrip('/')


def build_full_image_url(image_path):
    """构建完整的图片访问URL"""
    if not image_path:
        return ''
    if image_path.startswith('http://') or image_path.startswith('https://'):
        return image_path
    return f'{get_base_url()}/api/work-orders/uploads/{image_path}'


def convert_attachment_urls(data, processed=None):
    """递归转换data中的附件URL为完整地址"""
    if processed is None:
        processed = set()

    obj_id = id(data)
    if obj_id in processed:
        return data
    processed.add(obj_id)

    if isinstance(data, dict):
        if 'download' in data:
            download_list = data['download']
            for item in download_list:
                if 'imgreplace' in item:
                    for img in item['imgreplace']:
                        if 'imageFilePath' in img:
                            img['imageFilePath'] = build_full_image_url(img['imageFilePath'])
        for key, value in data.items():
            convert_attachment_urls(value, processed)
    elif isinstance(data, list):
        for item in data:
            convert_attachment_urls(item, processed)
    return data


# ============ 中间件和装饰器 ============

def login_required(f):
    """会话验证中间件"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'message': '请先登录'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def api_response(success, data=None, message=None, status_code=200):
    """统一API响应格式"""
    response = {'success': success}
    if data is not None:
        response['data'] = data
    if message is not None:
        response['message'] = message
    return jsonify(response), status_code


# ============ 认证API ============

@app.route('/api/login', methods=['POST'])
def login():
    """
    用户登录API
    请求体: {"username": "xxx", "password": "xxx"}
    """
    data = request.get_json()

    if not data:
        return api_response(False, message='请求数据无效', status_code=400)

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return api_response(False, message='用户名和密码不能为空', status_code=400)

    user = verify_user(username, password)

    if user:
        # 设置会话
        session['user_id'] = user['id']
        session['username'] = user['username']
        return api_response(True, data=user, message='登录成功')
    else:
        return api_response(False, message='账号或密码错误', status_code=401)


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """
    用户退出API
    """
    username = session.get('username')
    session.clear()
    return api_response(True, message=f'{username} 已退出登录')


@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """
    获取当前登录状态API
    """
    if 'user_id' in session:
        return api_response(True, data={
            'isLoggedIn': True,
            'user': {
                'id': session['user_id'],
                'username': session['username']
            }
        })
    else:
        return api_response(True, data={'isLoggedIn': False})


# ============ 账号管理API ============

@app.route('/api/accounts', methods=['GET'])
@login_required
def list_accounts():
    """
    获取账号列表API
    返回除密码外的用户信息
    """
    users = get_all_users()
    return api_response(True, data=users)


@app.route('/api/accounts', methods=['POST'])
@login_required
def add_account():
    """
    添加账号API
    请求体: {"username": "xxx", "password": "xxx"}
    """
    data = request.get_json()

    if not data:
        return api_response(False, message='请求数据无效', status_code=400)

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return api_response(False, message='用户名和密码不能为空', status_code=400)

    if len(username) < 2 or len(username) > 20:
        return api_response(False, message='用户名长度需在2-20个字符之间', status_code=400)

    if len(password) < 6:
        return api_response(False, message='密码长度不能少于6个字符', status_code=400)

    user, error = create_user(username, password)

    if error:
        return api_response(False, message=error, status_code=400)

    return api_response(True, data=user, message='账号创建成功')


@app.route('/api/accounts/<int:user_id>/password', methods=['PUT'])
@login_required
def change_password(user_id):
    """
    修改密码API
    请求体: {"password": "xxx"}
    """
    data = request.get_json()

    if not data:
        return api_response(False, message='请求数据无效', status_code=400)

    new_password = data.get('password', '')

    if not new_password:
        return api_response(False, message='新密码不能为空', status_code=400)

    if len(new_password) < 6:
        return api_response(False, message='密码长度不能少于6个字符', status_code=400)

    success, error = update_user_password(user_id, new_password)

    if error:
        return api_response(False, message=error, status_code=400)

    return api_response(True, message='密码修改成功')


@app.route('/api/accounts/<int:user_id>', methods=['DELETE'])
@login_required
def delete_account(user_id):
    """
    删除账号API
    """
    # 不允许删除自己
    if user_id == session['user_id']:
        return api_response(False, message='不能删除当前登录账号', status_code=400)

    success, error = delete_user(user_id)

    if error:
        return api_response(False, message=error, status_code=400)

    return api_response(True, message='账号删除成功')


# ============ 健康检查 ============

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查API"""
    return api_response(True, message='服务运行正常')


# ============ 启动应用 ============

@app.route('/')
def serve_index():
    """服务前端SPA应用"""
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
    """SPA路由支持 - 所有未匹配的路由返回index.html"""
    if request.path.startswith('/api/'):
        return api_response(False, message='接口不存在', status_code=404)
    return app.send_static_file('index.html')


# ==================== 工单管理API ====================

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/work-orders', methods=['GET'])
@login_required
def list_work_orders():
    """
    获取工单列表API
    返回所有工单列表（不含详情）
    """
    orders = get_all_work_orders()
    return api_response(True, data=orders)


@app.route('/api/work-orders/<int:work_order_id>', methods=['GET'])
@login_required
def get_work_order(work_order_id):
    """
    获取工单详情API（order.txt格式）
    """
    order = get_work_order_by_id(work_order_id)

    if not order:
        return api_response(False, message='工单不存在', status_code=404)

    # 转换为order.txt格式
    result = {
        'orderid': order.get('orderid', ''),
        'searchWorkOrderListEs': [
            {'key': 'newOrderid', 'value': order.get('new_orderid', ''), 'path': 'data', 'info': '新工单编号'},
            {'key': 'contactName', 'value': order.get('contact_name', ''), 'path': 'data', 'info': '联系人姓名'},
            {'key': 'contactPhone', 'value': order.get('contact_phone', ''), 'path': 'data', 'info': '联系人手机号'},
            {'key': 'createdDate', 'value': order.get('created_date', ''), 'path': 'data', 'info': '创建时间'},
            {'key': 'appointBeginTime', 'value': order.get('appoint_begin_time', ''), 'path': 'data', 'info': '预约开始时间'},
            {'key': 'appointEndTime', 'value': order.get('appoint_end_time', ''), 'path': 'data', 'info': '预约结束时间'},
            {'key': 'workOrderCompleteTime', 'value': order.get('work_order_complete_time', ''), 'path': 'data', 'info': '完工时间'},
            {'key': 'lastEvaluationTime', 'value': order.get('last_evaluation_time', ''), 'path': 'data', 'info': '评价时间'}
        ],
        'searchWorkOrderDetail': [],
        'getWorkOrderDetailList': [],
        'searchWorkOrderNodeResp': [],
        'searchAzWgmxDetail': [],
        'download': []
    }

    detail = order.get('detail', {})
    feedbacks = order.get('feedbacks', [])

    # searchWorkOrderDetail
    feedbacks_list = []
    for fb in feedbacks:
        feedbacks_list.append({
            'key': 'lastModifiedDate',
            'value': fb.get('last_modified_date', ''),
            'path': f"data.workOrderFeedbackRespList[{fb.get('feedback_index', 0)}]",
            'info': f"操作记录时间{fb.get('feedback_index', 0) + 1}"
        })
        feedbacks_list.append({
            'key': 'content',
            'value': fb.get('content', ''),
            'path': f"data.workOrderFeedbackRespList[{fb.get('feedback_index', 0)}]",
            'info': f"操作内容{fb.get('feedback_index', 0) + 1}"
        })

    result['searchWorkOrderDetail'] = [
        {'key': 'evaluationTime', 'value': detail.get('evaluation_time', ''), 'path': 'data.workOrderEvaluationRespList', 'info': '评价时间'},
        {'key': 'appointBeginTime', 'value': order.get('appoint_begin_time', ''), 'path': 'data.workOrderResp', 'info': '预约开始时间'},
        {'key': 'appointEndTime', 'value': order.get('appoint_end_time', ''), 'path': 'data.workOrderResp', 'info': '结束预约时间'},
        {'key': 'expectDoorToDoorBeginTime', 'value': detail.get('expect_door_to_door_begin_time', ''), 'path': 'data.workOrderResp', 'info': '期望上门开始时间'},
        {'key': 'expectDoorToDoorEndTime', 'value': detail.get('expect_door_to_door_end_time', ''), 'path': 'data.workOrderResp', 'info': '期望上门结束时间'},
        {'key': 'deliveryTime', 'value': detail.get('delivery_time', ''), 'path': 'data.workOrderResp', 'info': '出库时间'},
        {'key': 'signInLocation', 'value': detail.get('sign_in_location', ''), 'path': 'data.workOrderResp', 'info': '签到定位'}
    ] + feedbacks_list

    # getWorkOrderDetailList - 产品信息
    products = order.get('products', [])
    for prod in products:
        result['getWorkOrderDetailList'].append({
            'key': 'buyTime',
            'value': prod.get('buy_time', ''),
            'path': f"data.workOrderDetailProductInfoVOList[{prod.get('product_index', 0)}]",
            'info': f"产品{prod.get('product_index', 0) + 1}购买时间"
        })

    # searchWorkOrderNodeResp - 节点记录
    nodes = order.get('nodes', [])
    complete_list = []
    created_list = []
    in_service_list = []
    send_orders_list = []

    for node in nodes:
        node_type = node.get('node_type', '')
        node_info = {
            'key': 'createdDate',
            'value': node.get('created_date', ''),
            'path': '',
            'info': ''
        }

        if node_type == 'complete':
            node_info['path'] = f"data.completeFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '网点完工时间'
            complete_list.append(node_info)
        elif node_type == 'created':
            node_info['path'] = f"data.createdFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '创建时间'
            created_list.append(node_info)
        elif node_type == 'inService':
            node_info['path'] = f"data.inServiceFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '服务中时间'
            in_service_list.append(node_info)
        elif node_type == 'sendOrders':
            node_info['path'] = f"data.sendOrdersFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '派单时间'
            send_orders_list.append(node_info)

    result['searchWorkOrderNodeResp'] = complete_list + created_list + in_service_list + send_orders_list

    # searchAzWgmxDetail - 结算记录
    settlements = order.get('settlements', [])
    settlement_list = []
    gmsj = ''
    scazsj = ''

    for settlement in settlements:
        settlement_list.append({
            'key': 'fksj',
            'value': settlement.get('fksj', ''),
            'path': f"data.azdMxSpgcList[{settlement.get('settlement_index', 0)}]",
            'info': f"结算单查询-操作时间{settlement.get('settlement_index', 0) + 1}"
        })
        if settlement.get('gmsj'):
            gmsj = settlement.get('gmsj', '')
        if settlement.get('scazsj'):
            scazsj = settlement.get('scazsj', '')

    result['searchAzWgmxDetail'] = settlement_list + [
        {'key': 'gmsj', 'value': gmsj, 'path': 'data', 'info': '结算单查询-购买时间'},
        {'key': 'scazsj', 'value': scazsj, 'path': 'data', 'info': '结算单查询-安装时间'}
    ]

    # download - 附件
    attachments = order.get('attachments', [])
    result['download'] = attachments if attachments else [{'imgreplace': []}]

    # 转换附件URL为完整地址
    result = convert_attachment_urls(result)

    return api_response(True, data=result)


@app.route('/api/work-orders', methods=['POST'])
@login_required
def add_work_order():
    """
    创建工单API
    请求体: 工单数据（包含主表、详情、操作记录、产品、节点、结算、附件等）
    """
    data = request.get_json()

    if not data:
        return api_response(False, message='请求数据无效', status_code=400)

    orderid = data.get('orderid', '').strip()
    if not orderid:
        return api_response(False, message='工单编号不能为空', status_code=400)

    # 检查orderid是否已存在
    existing = get_work_order_by_orderid(orderid)
    if existing:
        return api_response(False, message='工单编号已存在', status_code=400)

    order, error = create_work_order(data)

    if error:
        return api_response(False, message=error, status_code=400)

    return api_response(True, data=order, message='工单创建成功')


@app.route('/api/work-orders/<int:work_order_id>', methods=['PUT'])
@login_required
def edit_work_order(work_order_id):
    """
    更新工单API
    """
    data = request.get_json()

    if not data:
        return api_response(False, message='请求数据无效', status_code=400)

    # 检查工单是否存在
    existing = get_work_order_by_id(work_order_id)
    if not existing:
        return api_response(False, message='工单不存在', status_code=404)

    success, error = update_work_order(work_order_id, data)

    if error:
        return api_response(False, message=error, status_code=400)

    return api_response(True, message='工单更新成功')


@app.route('/api/work-orders/<int:work_order_id>', methods=['DELETE'])
@login_required
def remove_work_order(work_order_id):
    """
    删除工单API（含关联数据和图片文件删除）
    """
    # 检查工单是否存在
    existing = get_work_order_by_id(work_order_id)
    if not existing:
        return api_response(False, message='工单不存在', status_code=404)

    success, error = delete_work_order(work_order_id)

    if error:
        return api_response(False, message=error, status_code=400)

    return api_response(True, message='工单删除成功')


@app.route('/api/work-orders/search', methods=['GET'])
@login_required
def search_work_orders_api():
    """
    条件查询工单API
    查询参数: keyword, contact_name, contact_phone, created_date_from, created_date_to, orderid
    """
    keyword = request.args.get('keyword', '')
    contact_name = request.args.get('contact_name', '')
    contact_phone = request.args.get('contact_phone', '')
    created_date_from = request.args.get('created_date_from', '')
    created_date_to = request.args.get('created_date_to', '')
    orderid = request.args.get('orderid', '')

    orders = search_work_orders(
        keyword=keyword if keyword else None,
        contact_name=contact_name if contact_name else None,
        contact_phone=contact_phone if contact_phone else None,
        created_date_from=created_date_from if created_date_from else None,
        created_date_to=created_date_to if created_date_to else None,
        orderid=orderid if orderid else None
    )

    return api_response(True, data=orders)


@app.route('/api/work-orders/upload', methods=['POST'])
@login_required
def upload_image():
    """
    图片上传API
    上传文件到uploads目录，返回文件路径
    """
    if 'file' not in request.files:
        return api_response(False, message='没有文件', status_code=400)

    file = request.files['file']

    if file.filename == '':
        return api_response(False, message='没有选择文件', status_code=400)

    if file and allowed_file(file.filename):
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        return api_response(True, data={'path': filename, 'filename': filename}, message='上传成功')

    return api_response(False, message='不支持的文件类型', status_code=400)


@app.route('/api/work-orders/uploads/<filename>', methods=['GET'])
def serve_upload(filename):
    """
    访问上传的图片文件
    """
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/api/work-orders/by-orderid/<orderid>', methods=['GET'])
def get_work_order_by_orderid_api(orderid):
    """
    按工单编号查询工单API（返回order.txt格式）
    请求参数: orderid（工单编号）
    返回: 按order.txt的JSON结构组装的数据
    """
    order = get_work_order_by_orderid(orderid)

    if not order:
        return api_response(False, message='工单不存在', status_code=404)

    # 转换为order.txt格式
    result = {
        'orderid': order.get('orderid', ''),
        'searchWorkOrderListEs': [
            {'key': 'newOrderid', 'value': order.get('new_orderid', ''), 'path': 'data', 'info': '新工单编号'},
            {'key': 'contactName', 'value': order.get('contact_name', ''), 'path': 'data', 'info': '联系人姓名'},
            {'key': 'contactPhone', 'value': order.get('contact_phone', ''), 'path': 'data', 'info': '联系人手机号'},
            {'key': 'createdDate', 'value': order.get('created_date', ''), 'path': 'data', 'info': '创建时间'},
            {'key': 'appointBeginTime', 'value': order.get('appoint_begin_time', ''), 'path': 'data', 'info': '预约开始时间'},
            {'key': 'appointEndTime', 'value': order.get('appoint_end_time', ''), 'path': 'data', 'info': '预约结束时间'},
            {'key': 'workOrderCompleteTime', 'value': order.get('work_order_complete_time', ''), 'path': 'data', 'info': '完工时间'},
            {'key': 'lastEvaluationTime', 'value': order.get('last_evaluation_time', ''), 'path': 'data', 'info': '评价时间'}
        ],
        'searchWorkOrderDetail': [],
        'getWorkOrderDetailList': [],
        'searchWorkOrderNodeResp': [],
        'searchAzWgmxDetail': [],
        'download': []
    }

    detail = order.get('detail', {})
    feedbacks = order.get('feedbacks', [])

    # searchWorkOrderDetail
    feedbacks_list = []
    for fb in feedbacks:
        feedbacks_list.append({
            'key': 'lastModifiedDate',
            'value': fb.get('last_modified_date', ''),
            'path': f"data.workOrderFeedbackRespList[{fb.get('feedback_index', 0)}]",
            'info': f"操作记录时间{fb.get('feedback_index', 0) + 1}"
        })
        feedbacks_list.append({
            'key': 'content',
            'value': fb.get('content', ''),
            'path': f"data.workOrderFeedbackRespList[{fb.get('feedback_index', 0)}]",
            'info': f"操作内容{fb.get('feedback_index', 0) + 1}"
        })

    result['searchWorkOrderDetail'] = [
        {'key': 'evaluationTime', 'value': detail.get('evaluation_time', ''), 'path': 'data.workOrderEvaluationRespList', 'info': '评价时间'},
        {'key': 'appointBeginTime', 'value': order.get('appoint_begin_time', ''), 'path': 'data.workOrderResp', 'info': '预约开始时间'},
        {'key': 'appointEndTime', 'value': order.get('appoint_end_time', ''), 'path': 'data.workOrderResp', 'info': '结束预约时间'},
        {'key': 'expectDoorToDoorBeginTime', 'value': detail.get('expect_door_to_door_begin_time', ''), 'path': 'data.workOrderResp', 'info': '期望上门开始时间'},
        {'key': 'expectDoorToDoorEndTime', 'value': detail.get('expect_door_to_door_end_time', ''), 'path': 'data.workOrderResp', 'info': '期望上门结束时间'},
        {'key': 'deliveryTime', 'value': detail.get('delivery_time', ''), 'path': 'data.workOrderResp', 'info': '出库时间'},
        {'key': 'signInLocation', 'value': detail.get('sign_in_location', ''), 'path': 'data.workOrderResp', 'info': '签到定位'}
    ] + feedbacks_list

    # getWorkOrderDetailList - 产品信息
    products = order.get('products', [])
    for prod in products:
        result['getWorkOrderDetailList'].append({
            'key': 'buyTime',
            'value': prod.get('buy_time', ''),
            'path': f"data.workOrderDetailProductInfoVOList[{prod.get('product_index', 0)}]",
            'info': f"产品{prod.get('product_index', 0) + 1}购买时间"
        })

    # searchWorkOrderNodeResp - 节点记录
    nodes = order.get('nodes', [])
    complete_list = []
    created_list = []
    in_service_list = []
    send_orders_list = []

    for node in nodes:
        node_type = node.get('node_type', '')
        node_info = {
            'key': 'createdDate',
            'value': node.get('created_date', ''),
            'path': '',
            'info': ''
        }

        if node_type == 'complete':
            node_info['path'] = f"data.completeFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '网点完工时间'
            complete_list.append(node_info)
        elif node_type == 'created':
            node_info['path'] = f"data.createdFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '创建时间'
            created_list.append(node_info)
        elif node_type == 'inService':
            node_info['path'] = f"data.inServiceFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '服务中时间'
            in_service_list.append(node_info)
        elif node_type == 'sendOrders':
            node_info['path'] = f"data.sendOrdersFeedbackList[{node.get('node_index', 0)}]"
            node_info['info'] = '派单时间'
            send_orders_list.append(node_info)

    result['searchWorkOrderNodeResp'] = complete_list + created_list + in_service_list + send_orders_list

    # searchAzWgmxDetail - 结算记录
    settlements = order.get('settlements', [])
    settlement_list = []
    gmsj = ''
    scazsj = ''

    for settlement in settlements:
        settlement_list.append({
            'key': 'fksj',
            'value': settlement.get('fksj', ''),
            'path': f"data.azdMxSpgcList[{settlement.get('settlement_index', 0)}]",
            'info': f"结算单查询-操作时间{settlement.get('settlement_index', 0) + 1}"
        })
        if settlement.get('gmsj'):
            gmsj = settlement.get('gmsj', '')
        if settlement.get('scazsj'):
            scazsj = settlement.get('scazsj', '')

    result['searchAzWgmxDetail'] = settlement_list + [
        {'key': 'gmsj', 'value': gmsj, 'path': 'data', 'info': '结算单查询-购买时间'},
        {'key': 'scazsj', 'value': scazsj, 'path': 'data', 'info': '结算单查询-安装时间'}
    ]

    # download - 附件
    attachments = order.get('attachments', [])
    result['download'] = attachments if attachments else [{'imgreplace': []}]

    # 转换附件URL为完整地址
    result = convert_attachment_urls(result)

    return api_response(True, data=result)


@app.route('/api/work-orders/query', methods=['POST'])
def batch_query_api():
    """
    批量查询API（外部调用，返回order.txt格式）
    请求体: {"orderIds": ["orderid1", "orderid2", ...]}
    返回: 按order.txt的JSON结构组装的数据数组
    """
    data = request.get_json()

    if not data or 'orderIds' not in data:
        return api_response(False, message='请求数据无效，需要orderIds数组', status_code=400)

    order_ids = data.get('orderIds', [])

    if not order_ids:
        return jsonify({'success': True, 'orders': [], 'message': ''})

    # 批量查询工单
    result_dict = batch_query_work_orders(order_ids)

    # 如果没有查到任何工单，返回空数组
    if not result_dict:
        return jsonify({'success': True, 'orders': [], 'message': ''})

    # 对每个工单数据转换附件URL为完整地址，并转换为数组
    result_array = []
    for orderid in result_dict:
        order_data = convert_attachment_urls(result_dict[orderid])
        result_array.append(order_data)

    # 批量查询使用 orders 而不是 data
    all_url = [
        {"key": "searchWorkOrderListEs", "Method": "POST", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/searchWorkOrderListEs", "info": "查询工单列表"},
        {"key": "searchWorkOrderDetail", "Method": "GET", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/searchWorkOrderDetail", "info": "查询工单详情"},
        {"key": "getWorkOrderDetailList", "Method": "POST", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/getWorkOrderDetailList", "info": "查询工单详情列表详情"},
        {"key": "searchWorkOrderNodeResp", "Method": "GET", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/searchWorkOrderNodeResp", "info": "查询工单节点详情"},
        {"key": "searchAzWgmxDetail", "Method": "POST", "url": "https://sms.gree.com/api/sso/autoapp-default-server-installaccounts/mvp/azwgmx/searchAzWgmxDetail", "info": "查询工单详情列表"},
        {"key": "download", "Method": "GET", "url": "https://sms.gree.com/api/pub/nts-foundation-attachmentmanager/api/v2/attachment/download", "info": "下载图片"}
    ]

    return jsonify({'success': True, 'orders': result_array, 'all_url': all_url, 'message': ''})


@app.route('/api/work-orders/upload-external', methods=['POST'])
def upload_work_order():
    """
    第三方上传工单接口
    请求体: 第三方上传数据格式（order.txt格式）
    返回: 创建结果
    """
    data = request.get_json()

    if not data:
        return api_response(False, message='请求数据无效', status_code=400)

    orderid = data.get('orderid', '')
    if not orderid:
        return api_response(False, message='工单编号不能为空', status_code=400)

    if work_order_exists(orderid):
        return api_response(False, message=f'工单编号 {orderid} 已存在', status_code=409)

    result, error = create_work_order_from_upload(data)

    if error:
        return api_response(False, message=f'创建工单失败: {error}', status_code=500)

    return api_response(True, data=result, message='工单创建成功')


# ============ 系统配置接口 ============

@app.route('/api/config/system', methods=['GET'])
def get_system_config():
    """
    获取系统配置（第三方调用，无需鉴权）
    """
    enable_work_order = get_config_value('enable_work_order', 'false')
    return api_response(True, data={
        'enable_work_order': enable_work_order.lower() in ['true', '1', 'yes']
    })


@app.route('/api/config/system', methods=['PUT'])
@login_required
def set_system_config():
    """
    设置系统配置（需要登录）
    """
    data = request.get_json()
    if not data:
        return api_response(False, message='请求数据无效', status_code=400)

    enable_work_order = data.get('enable_work_order', False)
    success = set_config_value('enable_work_order', 'true' if enable_work_order else 'false')

    if success:
        return api_response(True, message='配置更新成功')
    else:
        return api_response(False, message='配置更新失败', status_code=500)


@app.route('/api/work-orders/new-orderids', methods=['GET'])
def get_new_orderids():
    """
    获取有新工单编号的工单列表（第三方调用，无需鉴权）
    如果 启用本系统工单数据 设置为false，返回空数组
    """
    enable_work_order = get_config_value('enable_work_order', 'false')
    if enable_work_order.lower() not in ['true', '1', 'yes']:
        return api_response(True, data=[])
    
    result = get_work_orders_with_new_orderid()
    return api_response(True, data=result)


# ============ 启动应用 ============

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    # 启动Flask服务
    app.run(host='0.0.0.0', port=5000, debug=True)

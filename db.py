import sqlite3
import datetime
from typing import List, Dict

# 数据库连接
def get_db_connection():
    conn = sqlite3.connect('smart_wallet.db')
    conn.row_factory = sqlite3.Row  # 支持字典式读取
    return conn

# 初始化所有表（第一次运行自动创建）
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. 账单表（覆盖你要求的所有记账字段）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_type TEXT NOT NULL,  -- 交易类型：支出/收入/转账等10种
        amount REAL NOT NULL,     -- 金额
        date TEXT NOT NULL,       -- 日期
        time TEXT NOT NULL,       -- 时间
        category1 TEXT,           -- 1级分类
        category2 TEXT,           -- 2级分类
        category3 TEXT,           -- 3级分类
        account TEXT NOT NULL,    -- 账户
        remark TEXT,              -- 备注
        tags TEXT,                -- 标签
        merchant TEXT,            -- 商家
        project TEXT,             -- 项目
        member TEXT,              -- 成员
        img_path TEXT,            -- 图片附件路径
        is_deleted INTEGER DEFAULT 0  -- 回收站标记：0=正常，1=删除
    )
    ''')

    # 2. 分类表（多级分类管理）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level INTEGER NOT NULL,   -- 分类等级：1/2/3
        name TEXT NOT NULL,       -- 分类名称
        parent_name TEXT,         -- 父分类名称
        icon TEXT,                -- 分类图标
        color TEXT,               -- 分类颜色
        sort INTEGER DEFAULT 0    -- 排序
    )
    ''')

    # 3. 账户表（多账户管理）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_type TEXT NOT NULL, -- 账户类型：现金/支付宝等
        account_name TEXT NOT NULL, -- 账户名称
        balance REAL DEFAULT 0,     -- 余额
        currency TEXT DEFAULT 'CNY',-- 币种
        is_hidden INTEGER DEFAULT 0 -- 是否隐藏
    )
    ''')

    # 4. 预算表（预算管理）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cycle TEXT NOT NULL,        -- 周期：日/周/月/年
        category TEXT,              -- 分类预算
        amount REAL NOT NULL,       -- 预算金额
        used REAL DEFAULT 0,        -- 已用金额
        year TEXT NOT NULL,
        month TEXT
    )
    ''')

    conn.commit()
    conn.close()

# ------------------- 账单操作 -------------------
# 添加账单
def add_bill(data: Dict):
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    data['date'] = data.get('date', now.strftime('%Y-%m-%d'))
    data['time'] = data.get('time', now.strftime('%H:%M:%S'))
    cursor.execute('''
    INSERT INTO bills (trade_type, amount, date, time, category1, category2, category3, 
                      account, remark, tags, merchant, project, member, img_path)
    VALUES (:trade_type, :amount, :date, :time, :category1, :category2, :category3,
            :account, :remark, :tags, :merchant, :project, :member, :img_path)
    ''', data)
    # 更新账户余额
    update_account_balance(data['account'], data['amount'], data['trade_type'])
    # 更新预算
    update_budget_used(data['category1'], data['amount'], data['date'])
    conn.commit()
    conn.close()

# 查询账单
def query_bills(condition: Dict = None) -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM bills WHERE is_deleted=0"
    params = []
    if condition:
        for k, v in condition.items():
            sql += f" AND {k}=?"
            params.append(v)
    sql += " ORDER BY date DESC, time DESC"
    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# ------------------- 账户操作 -------------------
def update_account_balance(account_name: str, amount: float, trade_type: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    # 收入/充值/报销/退款 → 余额增加
    if trade_type in ['收入', '充值', '报销', '退款']:
        cursor.execute("UPDATE accounts SET balance=balance+? WHERE account_name=?", (amount, account_name))
    # 支出/提现 → 余额减少
    elif trade_type in ['支出', '提现']:
        cursor.execute("UPDATE accounts SET balance=balance-? WHERE account_name=?", (amount, account_name))
    conn.commit()
    conn.close()

# 初始化默认账户
def init_default_accounts():
    conn = get_db_connection()
    cursor = conn.cursor()
    default_accounts = [
        ('现金', '现金', 0), ('储蓄卡', '储蓄卡', 0), ('信用卡', '信用卡', 0),
        ('支付宝', '支付宝', 0), ('微信', '微信', 0), ('余额宝', '余额宝', 0)
    ]
    for name, type_, bal in default_accounts:
        cursor.execute("SELECT 1 FROM accounts WHERE account_name=?", (name,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO accounts (account_type, account_name, balance) VALUES (?,?,?)", (type_, name, bal))
    conn.commit()
    conn.close()

# ------------------- 初始化执行 -------------------
if __name__ == '__main__':
    init_db()
    init_default_accounts()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import matplotlib.pyplot as plt
from db import init_db, init_default_accounts, add_bill, query_bills
from utils import export_bills_to_excel, simple_calculator

# ------------------- 主程序类 -------------------
class SmartWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("智能记账软件 - 核心版")
        self.root.geometry("900x700")
        # 初始化数据库
        init_db()
        init_default_accounts()
        # 交易类型（你要求的10种）
        self.trade_types = ['支出', '收入', '转账', '借入', '借出', '还款', '报销', '退款', '充值', '提现']
        # 创建标签页
        self.create_tabs()

    # 创建多标签页
    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)
        # 1. 快速记账页
        self.tab1 = ttk.Frame(tab_control)
        tab_control.add(self.tab1, text='快速记账')
        self.create_bill_tab()
        # 2. 分类管理页
        self.tab2 = ttk.Frame(tab_control)
        tab_control.add(self.tab2, text='分类管理')
        # 3. 账户管理页
        self.tab3 = ttk.Frame(tab_control)
        tab_control.add(self.tab3, text='账户管理')
        # 4. 预算管理页
        self.tab4 = ttk.Frame(tab_control)
        tab_control.add(self.tab4, text='预算管理')
        # 5. 数据报表页
        self.tab5 = ttk.Frame(tab_control)
        tab_control.add(self.tab5, text='数据报表')
        # 6. 快捷操作页
        self.tab6 = ttk.Frame(tab_control)
        tab_control.add(self.tab6, text='快捷操作')
        self.create_tools_tab()

        tab_control.pack(expand=1, fill='both')

    # 快速记账页面
    def create_bill_tab(self):
        # 表单框架
        frame = ttk.LabelFrame(self.tab1, text="记账信息")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # 交易类型
        ttk.Label(frame, text="交易类型：").grid(row=0, column=0, sticky='w')
        self.trade_var = tk.StringVar(value=self.trade_types[0])
        ttk.Combobox(frame, textvariable=self.trade_var, values=self.trade_types, state='readonly').grid(row=0, column=1)

        # 金额
        ttk.Label(frame, text="金额：").grid(row=1, column=0, sticky='w')
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=1, column=1)

        # 三级分类
        ttk.Label(frame, text="1级分类：").grid(row=2, column=0, sticky='w')
        self.c1_entry = ttk.Entry(frame)
        self.c1_entry.grid(row=2, column=1)
        ttk.Label(frame, text="2级分类：").grid(row=3, column=0, sticky='w')
        self.c2_entry = ttk.Entry(frame)
        self.c2_entry.grid(row=3, column=1)
        ttk.Label(frame, text="3级分类：").grid(row=4, column=0, sticky='w')
        self.c3_entry = ttk.Entry(frame)
        self.c3_entry.grid(row=4, column=1)

        # 账户
        ttk.Label(frame, text="账户：").grid(row=5, column=0, sticky='w')
        self.account_var = tk.StringVar(value='微信')
        ttk.Combobox(frame, textvariable=self.account_var, values=['现金','储蓄卡','信用卡','支付宝','微信','余额宝']).grid(row=5, column=1)

        # 备注
        ttk.Label(frame, text="备注：").grid(row=6, column=0, sticky='w')
        self.remark_entry = ttk.Entry(frame)
        self.remark_entry.grid(row=6, column=1)

        # 保存按钮
        ttk.Button(frame, text="保存账单", command=self.save_bill).grid(row=7, column=0, columnspan=2, pady=10)

    # 保存账单
    def save_bill(self):
        try:
            data = {
                'trade_type': self.trade_var.get(),
                'amount': float(self.amount_entry.get()),
                'category1': self.c1_entry.get(),
                'category2': self.c2_entry.get(),
                'category3': self.c3_entry.get(),
                'account': self.account_var.get(),
                'remark': self.remark_entry.get(),
                'img_path': ''
            }
            add_bill(data)
            messagebox.showinfo("成功", "账单保存成功！")
            # 清空输入框
            self.amount_entry.delete(0, tk.END)
            self.remark_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("错误", "请输入有效数字！")

    # 快捷操作页面
    def create_tools_tab(self):
        frame = ttk.LabelFrame(self.tab6, text="快捷工具")
        frame.pack(padx=10, pady=10, fill='x')
        ttk.Button(frame, text="计算器", command=simple_calculator).pack(fill='x', pady=5)
        ttk.Button(frame, text="导出账单Excel", command=lambda: export_bills_to_excel(query_bills())).pack(fill='x', pady=5)
        ttk.Button(frame, text="导入CSV账单", command=lambda: filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])).pack(fill='x', pady=5)

# ------------------- 启动程序 -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartWalletApp(root)
    root.mainloop()
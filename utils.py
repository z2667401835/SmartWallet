import pandas as pd
from tkinter import messagebox
import datetime

# 导出账单为Excel
def export_bills_to_excel(bills):
    if not bills:
        messagebox.showwarning("提示", "无账单可导出！")
        return
    df = pd.DataFrame(bills)
    filename = f"记账账单_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.xlsx"
    df.to_excel(filename, index=False)
    messagebox.showinfo("成功", f"账单已导出至：{filename}")

# 导入CSV账单
def import_bills_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        # 这里可扩展字段匹配逻辑
        messagebox.showinfo("成功", f"导入成功！共{len(df)}条账单")
    except Exception as e:
        messagebox.showerror("错误", f"导入失败：{str(e)}")

# 简易计算器
def simple_calculator():
    import tkinter as tk
    from tkinter import simpledialog
    root = tk.Tk()
    root.withdraw()
    expr = simpledialog.askstring("计算器", "输入计算式（如：100+50*2）：")
    if expr:
        try:
            res = eval(expr)
            messagebox.showinfo("计算结果", f"{expr} = {res}")
            return res
        except:
            messagebox.showerror("错误", "输入格式错误！")
    return None
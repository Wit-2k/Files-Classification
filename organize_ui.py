import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# ==============================================================================
# 核心整理逻辑 (从之前的脚本中直接迁移)
# ==============================================================================
def organize_directory_robust(path):
    """
    健壮且可重复运行的目录整理函数。
    它将文件移动到扩展名文件夹，对压缩包文件夹进行分组，
    并将所有原始用户目录移动到“Misc”文件夹中。
    """
    # 打印信息到控制台，以便在需要时进行调试
    print(f"开始整理目录: {path}")

    archive_extensions = {'7z', 'zip', 'rar', 'iso', 'gz', 'tar', 'bz2', 'dmg', 'tgz'}
    special_dirs = {'Misc', '压缩包'}

    misc_folder_path = os.path.join(path, 'Misc')
    archive_master_folder_path = os.path.join(path, '压缩包')
    os.makedirs(misc_folder_path, exist_ok=True)
    os.makedirs(archive_master_folder_path, exist_ok=True)

    initial_items = os.listdir(path)
    extension_folders_this_run = set()

    # 第一步：处理所有文件
    for entry in initial_items:
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path):
            _, file_extension = os.path.splitext(entry)
            target_folder_name = file_extension[1:].lower() if file_extension else 'No_Extension'
            extension_folders_this_run.add(target_folder_name)
            
            target_folder_path = os.path.join(path, target_folder_name)
            os.makedirs(target_folder_path, exist_ok=True)
            shutil.move(entry_path, target_folder_path)
            print(f"文件 '{entry}' -> '{target_folder_name}'")

    # 第二步：处理所有文件夹
    current_items = os.listdir(path)
    for entry in current_items:
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            if entry in special_dirs:
                continue
            
            if entry.lower() in archive_extensions:
                shutil.move(entry_path, archive_master_folder_path)
                print(f"压缩包文件夹 '{entry}' -> '压缩包'")
            elif entry in extension_folders_this_run:
                continue
            else:
                shutil.move(entry_path, misc_folder_path)
                print(f"原始文件夹 '{entry}' -> 'Misc'")
    
    print("整理完成！")


# ==============================================================================
# UI 界面部分
# ==============================================================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("文件整理工具")
        self.root.geometry("500x150") # 设置窗口大小

        # 创建主框架
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 路径输入部分
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        path_label = tk.Label(path_frame, text="目标路径:")
        path_label.pack(side=tk.LEFT, padx=(0, 5))

        self.path_entry_var = tk.StringVar()
        self.path_entry = tk.Entry(path_frame, textvariable=self.path_entry_var, width=40)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.browse_button = tk.Button(path_frame, text="浏览...", command=self.browse_directory)
        self.browse_button.pack(side=tk.LEFT, padx=(5, 0))

        # 操作按钮部分
        self.start_button = tk.Button(main_frame, text="开始整理", command=self.start_organization, bg="#4CAF50", fg="white", height=2)
        self.start_button.pack(fill=tk.X, pady=10)

    def browse_directory(self):
        # 打开文件夹选择对话框
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry_var.set(directory)

    def start_organization(self):
        # 从输入框获取路径
        target_path = self.path_entry_var.get().strip()

        # --- 输入验证 ---
        if not target_path:
            messagebox.showerror("错误", "路径不能为空，请输入或选择一个文件夹路径。")
            return
        
        if not os.path.isdir(target_path):
            messagebox.showerror("错误", f"提供的路径无效或不是一个文件夹:\n{target_path}")
            return
        
        # --- 执行与反馈 ---
        try:
            # 禁用按钮，防止重复点击
            self.start_button.config(state=tk.DISABLED, text="整理中...")
            self.root.update_idletasks() # 立即更新UI

            # 调用核心整理函数
            organize_directory_robust(target_path)
            
            # 成功反馈
            messagebox.showinfo("成功", "文件夹整理完成！")

        except Exception as e:
            # 失败反馈
            messagebox.showerror("发生错误", f"整理过程中出现问题:\n{str(e)}")
        finally:
            # 无论成功失败，都恢复按钮状态
            self.start_button.config(state=tk.NORMAL, text="开始整理")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
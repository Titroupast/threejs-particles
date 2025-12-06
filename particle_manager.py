import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import random
import re

# 设置外观
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ParticleManagerPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("3D 粒子项目管理器 (Pro版) - 归档与删除")
        self.geometry("600x650")
        self.resizable(False, False)

        # 变量
        self.project_path = ctk.StringVar(value="")
        self.image_path = ctk.StringVar(value="")
        self.model_name = ctk.StringVar(value="")
        self.model_key = ctk.StringVar(value="")
        self.particle_count = ctk.IntVar(value=15000)
        self.scale_factor = ctk.DoubleVar(value=0.05)
        self.status_msg = ctk.StringVar(value="等待选择项目...")
        
        # 存储当前扫描到的模型列表
        self.existing_models = [] 

        self.create_widgets()

    def create_widgets(self):
        # --- 顶部：项目路径选择 ---
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(top_frame, text="📂 项目根目录 (index.html 所在位置):", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        
        path_box = ctk.CTkFrame(top_frame, fg_color="transparent")
        path_box.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkEntry(path_box, textvariable=self.project_path, placeholder_text="未选择...", state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(path_box, text="选择文件夹", width=100, command=self.select_project_folder).pack(side="right")

        # --- 中间：选项卡视图 (新增 vs 删除) ---
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=10)

        # 创建两个标签页
        self.tab_add = self.tab_view.add("✨ 新增模型")
        self.tab_manage = self.tab_view.add("🗑️ 删除管理")

        # === 页面 1: 新增模型 ===
        self.setup_add_tab()

        # === 页面 2: 删除管理 ===
        self.setup_manage_tab()

        # --- 底部：状态栏 ---
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_msg, text_color="gray", wraplength=550)
        self.status_label.pack(side="bottom", pady=10)

    def setup_add_tab(self):
        # 图片选择
        ctk.CTkLabel(self.tab_add, text="1. 选择源图片 (推荐透明背景 PNG):").pack(anchor="w", padx=10, pady=(10, 0))
        img_box = ctk.CTkFrame(self.tab_add, fg_color="transparent")
        img_box.pack(fill="x", padx=10, pady=5)
        ctk.CTkEntry(img_box, textvariable=self.image_path, placeholder_text="未选择图片...", state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(img_box, text="选择图片", width=100, command=self.select_image).pack(side="right")
        
        # 参数设置
        ctk.CTkLabel(self.tab_add, text="2. 模型信息:").pack(anchor="w", padx=10, pady=(10, 0))
        info_grid = ctk.CTkFrame(self.tab_add)
        info_grid.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(info_grid, text="名称 (中文):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(info_grid, textvariable=self.model_name, placeholder_text="如: 刻晴").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(info_grid, text="ID (英文):").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        ctk.CTkEntry(info_grid, textvariable=self.model_key, placeholder_text="如: keqing").grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # 粒子数
        ctk.CTkLabel(self.tab_add, text="3. 粒子数量 (建议 10000 - 30000):").pack(anchor="w", padx=10, pady=(10, 0))
        slider_box = ctk.CTkFrame(self.tab_add, fg_color="transparent")
        slider_box.pack(fill="x", padx=10)
        self.slider_label = ctk.CTkLabel(slider_box, text="15000", width=50)
        self.slider_label.pack(side="right")
        ctk.CTkSlider(slider_box, from_=5000, to=50000, number_of_steps=45, variable=self.particle_count, command=lambda v: self.slider_label.configure(text=str(int(v)))).pack(side="left", fill="x", expand=True)

        # 生成按钮
        ctk.CTkButton(self.tab_add, text="⚡ 生成并注入到 models 文件夹 ⚡", height=40, fg_color="#00cc44", hover_color="#00aa33", font=("Arial", 14, "bold"), command=self.run_generation).pack(fill="x", padx=20, pady=30)

    def setup_manage_tab(self):
        ctk.CTkLabel(self.tab_manage, text="这里列出了 index.html 中引用的所有外部模型:", text_color="#aaa").pack(pady=(10, 5))
        
        # 下拉菜单选择要删除的模型
        self.model_menu = ctk.CTkOptionMenu(self.tab_manage, dynamic_resizing=False, width=300, values=["请先选择项目..."])
        self.model_menu.pack(pady=10)
        
        ctk.CTkButton(self.tab_manage, text="🔄 刷新列表", width=100, fg_color="gray", command=self.scan_html_for_models).pack(pady=5)
        
        # 删除按钮
        ctk.CTkButton(self.tab_manage, text="🗑️ 彻底删除选中模型", height=40, fg_color="#cc0000", hover_color="#aa0000", font=("Arial", 14, "bold"), command=self.delete_selected_model).pack(fill="x", padx=40, pady=40)
        
        ctk.CTkLabel(self.tab_manage, text="注意：删除操作会移除 JS 文件并清理 HTML 标签。", text_color="#888", font=("Arial", 10)).pack(side="bottom", pady=10)

    # --- 逻辑功能 ---

    def select_project_folder(self):
        path = filedialog.askdirectory()
        if path:
            if os.path.exists(os.path.join(path, "index.html")):
                self.project_path.set(path)
                self.status_msg.set(f"✅ 已加载项目: {os.path.basename(path)}")
                
                # 自动创建 models 文件夹
                models_dir = os.path.join(path, "models")
                if not os.path.exists(models_dir):
                    os.makedirs(models_dir)
                    print("已创建 models 文件夹")
                
                self.scan_html_for_models() # 扫描现有模型
            else:
                messagebox.showerror("错误", "该文件夹下找不到 index.html！")

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if path:
            self.image_path.set(path)
            # 自动猜测 ID
            filename = os.path.basename(path).split('.')[0]
            clean_id = re.sub(r'[^a-zA-Z0-9]', '', filename).lower()
            if not self.model_key.get(): self.model_key.set(clean_id)
            if not self.model_name.get(): self.model_name.set(filename)

    def generate_particle_js(self, img_path, model_name, model_key, max_particles, scale):
        # (与之前相同的生成逻辑，略微简化代码展示)
        try:
            img = Image.open(img_path).convert('RGBA')
        except Exception:
            return None, "无法打开图片"
            
        width, height = img.size
        pixels = []
        for y in range(height):
            for x in range(width):
                r, g, b, a = img.getpixel((x, y))
                if a > 128: pixels.append((x, y, r, g, b))
        
        if not pixels: return None, "图片是全透明的"

        sampled = random.sample(pixels, max_particles) if len(pixels) > max_particles else pixels
        positions, colors = [], []
        for x, y, r, g, b in sampled:
            positions.extend([(x - width/2)*scale, -(y - height/2)*scale, (random.random()-0.5)*2.0])
            colors.extend([r/255.0, g/255.0, b/255.0])

        pos_str = ",".join([f"{v:.3f}" for v in positions])
        col_str = ",".join([f"{v:.2f}" for v in colors])

        content = f"""
// Auto-generated: {model_name}
window.IMAGE_MODELS = window.IMAGE_MODELS || {{}};
window.IMAGE_MODELS['{model_key}'] = {{ name: '{model_name}', count: {len(sampled)}, positions: new Float32Array([{pos_str}]), colors: new Float32Array([{col_str}]) }};
"""
        return content, len(sampled)

    def run_generation(self):
        proj_dir = self.project_path.get()
        if not proj_dir: return messagebox.showerror("错误", "请先选择项目文件夹")
        
        m_key = self.model_key.get().strip()
        if not m_key or " " in m_key: return messagebox.showerror("错误", "ID 必须是纯英文且无空格")

        self.status_msg.set("正在处理图片...")
        self.update()

        js_content, count = self.generate_particle_js(
            self.image_path.get(), self.model_name.get(), m_key, 
            self.particle_count.get(), self.scale_factor.get()
        )
        
        if js_content is None: return messagebox.showerror("错误", count)

        # 1. 写入文件到 models 文件夹
        js_filename = f"{m_key}_data.js"
        models_dir = os.path.join(proj_dir, "models")
        if not os.path.exists(models_dir): os.makedirs(models_dir) # 双重保险
        
        full_js_path = os.path.join(models_dir, js_filename)
        with open(full_js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)

        # 2. 修改 HTML
        html_path = os.path.join(proj_dir, "index.html")
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # 注意这里的路径变成了 ./models/...
        script_tag = f'<script src="./models/{js_filename}"></script>'
        
        if script_tag not in html:
            # 兼容旧版：如果用户之前放在根目录，也尝试检测一下
            old_tag = f'<script src="./{js_filename}"></script>'
            if old_tag in html:
                # 这是一个迁移的好机会，但为了安全，我们只是追加新的，用户可以在删除面板删旧的
                pass 
                
            if "</head>" in html:
                html = html.replace("</head>", f"    {script_tag}\n</head>")
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                msg = f"🎉 成功！\nJS 文件已保存至: models/{js_filename}\nHTML 已注入引用。"
            else:
                msg = "⚠️ JS 生成了，但找不到 </head> 标签，无法自动注入。"
        else:
            msg = f"♻️ 更新成功！文件已覆盖: models/{js_filename}"

        messagebox.showinfo("完成", msg)
        self.status_msg.set(f"就绪 - 上次生成: {m_key}")
        self.scan_html_for_models() # 刷新删除列表

    # --- 核心新增：扫描与删除功能 ---

    def scan_html_for_models(self):
        """扫描 index.html 里的 script 标签"""
        proj_dir = self.project_path.get()
        if not proj_dir: return

        html_path = os.path.join(proj_dir, "index.html")
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # 正则匹配 src="./xxx.js" 或 src="./models/xxx.js"
            # 捕获组 1: 完整相对路径 (如 ./models/miku_data.js)
            # 捕获组 2: 文件名 (如 miku_data.js)
            pattern = re.compile(r'<script\s+src=["\'](\./(?:models/)?([^"\']+\.js))["\']\s*></script>')
            matches = pattern.findall(html)
            
            # 过滤掉 Three.js 等库文件，只保留包含 'data' 或我们在 Python 里生成的命名风格的文件
            # 或者简单的逻辑：只要是本地 JS 都可以列出来供删除，但要小心
            # 这里我们只列出位于 ./models/ 下的，或者文件名包含 _data 的
            self.existing_models = []
            
            display_values = []
            for full_path, filename in matches:
                # 简单的过滤逻辑：只允许删除看似是模型数据的文件
                # 防止误删 main.js 或 three.js
                if "data" in filename or "models" in full_path:
                    self.existing_models.append({'tag_path': full_path, 'filename': filename})
                    display_values.append(filename)

            if not display_values:
                display_values = ["HTML中未找到模型文件"]
                self.model_menu.configure(state="disabled")
            else:
                self.model_menu.configure(state="normal")
            
            self.model_menu.configure(values=display_values)
            self.model_menu.set(display_values[0])
            self.status_msg.set(f"列表已刷新，找到 {len(self.existing_models)} 个模型")

        except Exception as e:
            self.status_msg.set(f"扫描出错: {str(e)}")

    def delete_selected_model(self):
        selected_file = self.model_menu.get()
        proj_dir = self.project_path.get()
        
        if not proj_dir or selected_file == "HTML中未找到模型文件":
            return

        if not messagebox.askyesno("确认删除", f"确定要删除模型文件 '{selected_file}' 吗？\n此操作不可撤销。"):
            return

        # 1. 尝试删除物理文件
        # 可能是 ./models/xxx.js 或者是根目录的 xxx.js
        # 我们根据扫描到的结果来判断
        target_info = next((item for item in self.existing_models if item['filename'] == selected_file), None)
        
        if target_info:
            # 解析物理路径
            # tag_path 可能是 ./models/abc.js 或 ./abc.js
            rel_path = target_info['tag_path'].replace("./", "") # 去掉 ./ 
            # 适配系统分隔符
            file_path = os.path.join(proj_dir, rel_path.replace("/", os.sep))
            
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"文件已删除: {file_path}")
                else:
                    print(f"物理文件不存在，仅清理标签: {file_path}")
            except Exception as e:
                messagebox.showerror("文件删除失败", str(e))

            # 2. 清理 HTML 标签
            html_path = os.path.join(proj_dir, "index.html")
            with open(html_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            deleted = False
            for line in lines:
                # 如果这一行包含了选中的文件名，就跳过（即删除）
                if selected_file in line and "<script" in line:
                    deleted = True
                    continue # 跳过这一行
                new_lines.append(line)
            
            if deleted:
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                messagebox.showinfo("成功", "✅ 模型已删除 (HTML标签已移除)")
                self.scan_html_for_models() # 刷新列表
            else:
                messagebox.showwarning("提示", "文件删了，但在 HTML 里没找到对应的标签？请手动检查。")

if __name__ == "__main__":
    app = ParticleManagerPro()
    app.mainloop()
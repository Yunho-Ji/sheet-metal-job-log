import tkinter as tk
from tkinter import ttk, messagebox
import database
from gui_components import create_custom_button

class SplitByRatioDialog(tk.Toplevel):
    def __init__(self, parent, original_log_data, total_minutes):
        super().__init__(parent)
        self.parent = parent
        self.log_data = original_log_data
        self.total_minutes = total_minutes
        
        self.title("병행 작업 나누기 (비율 자동 배분)")
        self.geometry("550x450")
        self.configure(bg="#F4F6F9")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self.rows = []
        
        self.create_widgets()
        self.center_window()
        
        # 기본 2행 추가
        self.add_row()
        self.add_row()
        
        # 기존 폼의 제품명이 있으면 첫번째 줄에 세팅
        if self.log_data.get("product_name"):
            self.rows[0]["product_var"].set(self.log_data["product_name"])

    def center_window(self):
        self.update_idletasks()
        width = 550
        height = 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        main_frame = tk.Frame(self, bg="#FFFFFF", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 상단 정보
        info_text = f"원본 작업: {self.log_data['start_time']} ~ {self.log_data['end_time']} (총 {self.total_minutes}분)"
        tk.Label(main_frame, text=info_text, font=("맑은 고딕", 12, "bold"), bg="#FFFFFF", fg="#1E293B").pack(anchor="w", pady=(0, 15))
        
        tk.Label(main_frame, text="제품명과 수량을 입력하시면 5분 단위 규칙에 맞춰 시간이 자동 배분됩니다.", font=("맑은 고딕", 9), bg="#FFFFFF", fg="#64748B").pack(anchor="w", pady=(0, 10))
        
        # 테이블 헤더 프레임
        header_frame = tk.Frame(main_frame, bg="#F1F5F9", pady=5)
        header_frame.pack(fill="x", pady=(0, 5))
        tk.Label(header_frame, text="제품명 (필수)", font=("맑은 고딕", 9, "bold"), bg="#F1F5F9", width=20, anchor="w").pack(side="left", padx=10)
        tk.Label(header_frame, text="수량", font=("맑은 고딕", 9, "bold"), bg="#F1F5F9", width=8, anchor="center").pack(side="left", padx=5)
        tk.Label(header_frame, text="자동 배분 시간", font=("맑은 고딕", 9, "bold"), bg="#F1F5F9", width=15, anchor="center").pack(side="left", padx=10)
        
        # 동적 행 컨테이너
        self.rows_frame = tk.Frame(main_frame, bg="#FFFFFF")
        self.rows_frame.pack(fill="both", expand=True)
        
        # 추가 버튼
        btn_add = create_custom_button(main_frame, "[+] 제품 추가", "#E2E8F0", "#CBD5E1", self.add_row, fg="#1E293B", active_fg="#1E293B")
        btn_add.pack(anchor="w", pady=10)
        
        # 하단 제어 버튼
        btn_frame = tk.Frame(main_frame, bg="#FFFFFF")
        btn_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        btn_save = create_custom_button(btn_frame, "일괄 분할 저장", "#1E3A8A", "#1D4ED8", self.save_split)
        btn_save.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        btn_close = create_custom_button(btn_frame, "취소", "#E2E8F0", "#CBD5E1", self.destroy, fg="#1E293B", active_fg="#1E293B")
        btn_close.pack(side="left", fill="x", expand=True, padx=(5, 0))

    def add_row(self):
        row_frame = tk.Frame(self.rows_frame, bg="#FFFFFF", pady=5)
        row_frame.pack(fill="x")
        
        product_var = tk.StringVar()
        ent_product = ttk.Entry(row_frame, textvariable=product_var, width=22)
        ent_product.pack(side="left", padx=10)
        
        qty_var = tk.StringVar()
        ent_qty = ttk.Entry(row_frame, textvariable=qty_var, width=8, justify="right")
        ent_qty.pack(side="left", padx=5)
        
        lbl_time = tk.Label(row_frame, text="- 분", font=("맑은 고딕", 9, "bold"), fg="#D97706", bg="#FFFFFF", width=15, anchor="center")
        lbl_time.pack(side="left", padx=10)
        
        btn_del = tk.Button(row_frame, text="X", fg="#DC2626", bg="#FFFFFF", relief="flat", cursor="hand2", command=lambda f=row_frame: self.delete_row(f))
        btn_del.pack(side="left", padx=5)
        
        row_data = {
            "frame": row_frame,
            "product_var": product_var,
            "qty_var": qty_var,
            "time_lbl": lbl_time,
            "time_mins": 0
        }
        self.rows.append(row_data)
        
        qty_var.trace_add("write", self.calculate_ratios)
        
    def delete_row(self, frame_to_delete):
        if len(self.rows) <= 1:
            messagebox.showwarning("경고", "최소 1개의 항목은 존재해야 합니다.", parent=self)
            return
            
        for idx, row in enumerate(self.rows):
            if row["frame"] == frame_to_delete:
                frame_to_delete.destroy()
                self.rows.pop(idx)
                break
        self.calculate_ratios()

    def calculate_ratios(self, *args):
        total_qty = 0
        valid_rows = []
        for row in self.rows:
            qty_str = row["qty_var"].get().strip()
            if qty_str.isdigit() and int(qty_str) > 0:
                qty = int(qty_str)
                total_qty += qty
                valid_rows.append((row, qty))
            else:
                row["time_lbl"].config(text="- 분")
                row["time_mins"] = 0
                
        if total_qty == 0:
            return

        total_allocated = 0
        allocated_data = []
        
        for row, qty in valid_rows:
            raw_mins = (qty / total_qty) * self.total_minutes
            rounded_mins = round(raw_mins / 5) * 5
            row["time_mins"] = rounded_mins
            total_allocated += rounded_mins
            allocated_data.append((row, qty, rounded_mins))
            
        diff = self.total_minutes - total_allocated
        if diff != 0 and allocated_data:
            max_item = max(allocated_data, key=lambda x: x[1])
            max_row = max_item[0]
            max_row["time_mins"] += diff
            
        for row in self.rows:
            m = row["time_mins"]
            if m > 0:
                row["time_lbl"].config(text=f"{m}분 할당")
                
    def minutes_to_time_str(self, total_minutes):
        hours = total_minutes // 60
        mins = total_minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def add_minutes_to_time(self, time_str, add_mins):
        h, m = map(int, time_str.split(':'))
        total = h * 60 + m + add_mins
        return self.minutes_to_time_str(total)

    def save_split(self):
        # 1. 밸리데이션
        items_to_save = []
        for row in self.rows:
            p_name = row["product_var"].get().strip()
            qty_str = row["qty_var"].get().strip()
            mins = row["time_mins"]
            
            if p_name or qty_str or mins > 0:
                if not p_name:
                    messagebox.showerror("오류", "모든 항목의 제품명을 입력해주세요.", parent=self)
                    return
                if not qty_str.isdigit() or int(qty_str) <= 0:
                    messagebox.showerror("오류", f"'{p_name}'의 수량을 올바르게 입력해주세요.", parent=self)
                    return
                if mins <= 0:
                    messagebox.showerror("오류", f"'{p_name}'에 할당된 시간이 없습니다.", parent=self)
                    return
                items_to_save.append({
                    "product": p_name,
                    "qty": int(qty_str),
                    "duration_mins": mins
                })
                
        if not items_to_save:
            messagebox.showerror("오류", "분할할 작업 내역을 입력해주세요.", parent=self)
            return
            
        # 총 시간이 맞는지 한 번 더 검증
        if sum(item["duration_mins"] for item in items_to_save) != self.total_minutes:
            messagebox.showerror("오류", "배분된 시간의 합이 총 소요 시간과 일치하지 않습니다.", parent=self)
            return
            
        # 2. DB 업데이트 및 인서트 로직
        current_start = self.log_data["start_time"]
        
        for idx, item in enumerate(items_to_save):
            next_start = self.add_minutes_to_time(current_start, item["duration_mins"])
            
            dur_h = item["duration_mins"] // 60
            dur_m = item["duration_mins"] % 60
            dur_str = ""
            if dur_h > 0 and dur_m > 0: dur_str = f"{dur_h}시간 {dur_m}분"
            elif dur_h > 0: dur_str = f"{dur_h}시간"
            else: dur_str = f"{dur_m}분"
            
            if idx == 0:
                # 첫 항목은 기존 데이터 UPDATE
                database.update_log(
                    self.log_data["id"],
                    self.log_data["work_date"],
                    self.log_data["worker_name"],
                    current_start,
                    next_start,
                    dur_str,
                    self.log_data["lot_number"],
                    item["product"],
                    self.log_data["process_code"],
                    item["qty"],
                    self.log_data["remarks"]
                )
            else:
                # 두번째부터는 신규 데이터 INSERT
                database.insert_log(
                    self.log_data["work_date"],
                    self.log_data["worker_name"],
                    current_start,
                    next_start,
                    dur_str,
                    self.log_data["lot_number"],
                    item["product"],
                    self.log_data["process_code"],
                    item["qty"],
                    self.log_data["remarks"]
                )
                
            current_start = next_start
            
        messagebox.showinfo("성공", "성공적으로 병행 작업이 분할 등록되었습니다.", parent=self)
        self.destroy()
        self.parent.destroy() # 수정 창 닫기
        # 최상위 메인 창 갱신 (parent.parent)
        if hasattr(self.parent.parent, "load_data"):
            self.parent.parent.load_data()

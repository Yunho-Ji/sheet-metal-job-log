import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import database
from gui_components import create_custom_button, create_form_row

class JobLogDialog(tk.Toplevel):
    def __init__(self, parent, log_data=None):
        super().__init__(parent)
        self.parent = parent
        self.log_data = log_data  # None이면 추가 모드, 딕셔너리 데이터면 수정/삭제 모드
        
        self.title("작업일지 등록" if not log_data else "작업일지 수정/삭제")
        self.geometry("450x620")
        self.configure(bg="#F4F6F9")
        self.resizable(False, False)
        
        # 화면 중앙 배치
        self.center_window()
        
        # 모달창 설정 (부모 창 제어 잠금)
        self.transient(parent)
        self.grab_set()
        
        # 폰트 정의
        self.label_font = ("맑은 고딕", 10)
        self.btn_font = ("맑은 고딕", 10, "bold")
        self.title_font = ("맑은 고딕", 12, "bold")
        
        self.create_widgets()
        self.set_initial_data()
        
    def center_window(self):
        self.update_idletasks()
        width = 450
        height = 620
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        # 다이얼로그 메인 프레임
        main_frame = tk.Frame(self, bg="#FFFFFF", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 타이틀 라벨
        title_text = "📝 신규 작업 정보 등록" if not self.log_data else "✏️ 작업 정보 수정 및 삭제"
        lbl_title = tk.Label(main_frame, text=title_text, font=self.title_font, bg="#FFFFFF", fg="#1E293B")
        lbl_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        # 1. 날짜 및 요일
        tk.Label(main_frame, text="작성일 *", bg="#FFFFFF", font=self.label_font).grid(row=1, column=0, sticky="w", pady=6)
        date_frame = tk.Frame(main_frame, bg="#FFFFFF")
        date_frame.grid(row=1, column=1, columnspan=2, sticky="ew", pady=6)
        
        current_year = datetime.datetime.now().year
        self.cb_year = ttk.Combobox(date_frame, values=[str(y) for y in range(current_year-2, current_year+3)], width=6, state="readonly")
        self.cb_year.pack(side="left", padx=(0, 2))
        tk.Label(date_frame, text="년", bg="#FFFFFF", font=self.label_font).pack(side="left", padx=(0, 5))
        
        self.cb_month = ttk.Combobox(date_frame, values=[f"{m:02d}" for m in range(1, 13)], width=4, state="readonly")
        self.cb_month.pack(side="left", padx=(0, 2))
        tk.Label(date_frame, text="월", bg="#FFFFFF", font=self.label_font).pack(side="left", padx=(0, 5))
        
        self.cb_day = ttk.Combobox(date_frame, values=[f"{d:02d}" for d in range(1, 32)], width=4, state="readonly")
        self.cb_day.pack(side="left", padx=(0, 2))
        tk.Label(date_frame, text="일", bg="#FFFFFF", font=self.label_font).pack(side="left", padx=(0, 8))
        
        self.lbl_weekday = tk.Label(date_frame, text="(요일)", font=("맑은 고딕", 10, "bold"), fg="#2563EB", bg="#FFFFFF")
        self.lbl_weekday.pack(side="left")
        
        self.cb_year.bind("<<ComboboxSelected>>", self.update_weekday_label)
        self.cb_month.bind("<<ComboboxSelected>>", self.update_weekday_label)
        self.cb_day.bind("<<ComboboxSelected>>", self.update_weekday_label)
        
        # 2. 작업자
        self.ent_worker = create_form_row(main_frame, "작업자 *", 2, self.label_font, width=25)
        
        # 구분선
        ttk.Separator(main_frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        
        # 3. 시작 시간
        self.ent_start_time = create_form_row(main_frame, "시작 시간 *", 4, self.label_font, width=15, example_text="예) 08:30")
        
        # 4. 완료 시간
        self.ent_end_time = create_form_row(main_frame, "완료 시간 *", 5, self.label_font, width=15, example_text="예) 17:30")
        
        # 5. 소요 시간
        self.ent_duration = create_form_row(main_frame, "소요 시간", 6, self.label_font, width=22, state="readonly")
        
        # 시간 변경 바인딩
        self.ent_start_time.bind("<KeyRelease>", self.on_time_changed)
        self.ent_end_time.bind("<KeyRelease>", self.on_time_changed)
        self.ent_start_time.bind("<FocusOut>", self.on_time_changed)
        self.ent_end_time.bind("<FocusOut>", self.on_time_changed)
        
        # 구분선
        ttk.Separator(main_frame, orient="horizontal").grid(row=7, column=0, columnspan=3, sticky="ew", pady=10)
        
        # 6~10 일반 텍스트 입력창
        self.ent_lot = create_form_row(main_frame, "로트번호 및 구분", 8, self.label_font)
        self.ent_product = create_form_row(main_frame, "제품명", 9, self.label_font)
        self.ent_process = create_form_row(main_frame, "공정 및 도변", 10, self.label_font)
        self.ent_qty = create_form_row(main_frame, "작업수량", 11, self.label_font, width=18, example_text="단위 혼용(SET, EA) 가능")
        self.ent_remarks = create_form_row(main_frame, "비고", 12, self.label_font)
        
        # 11. 제어 버튼
        btn_frame = tk.Frame(main_frame, bg="#FFFFFF")
        btn_frame.grid(row=13, column=0, columnspan=3, sticky="ew", pady=(20, 0))
        
        if not self.log_data:
            # 추가 모드
            self.btn_action = create_custom_button(btn_frame, "저장 및 추가", "#1E3A8A", "#1D4ED8", self.add_log)
            self.btn_action.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            btn_close = create_custom_button(btn_frame, "닫기", "#E2E8F0", "#CBD5E1", self.destroy, fg="#1E293B", active_fg="#1E293B")
            btn_close.pack(side="left", fill="x", expand=True, padx=(5, 0))
        else:
            # 수정/삭제 모드
            self.btn_update = create_custom_button(btn_frame, "수정 완료", "#D97706", "#F59E0B", self.update_log)
            self.btn_update.pack(side="left", fill="x", expand=True, padx=(0, 4))
            
            self.btn_delete = create_custom_button(btn_frame, "내역 삭제", "#DC2626", "#EF4444", self.delete_log)
            self.btn_delete.pack(side="left", fill="x", expand=True, padx=4)
            
            btn_close = create_custom_button(btn_frame, "취소", "#E2E8F0", "#CBD5E1", self.destroy, fg="#1E293B", active_fg="#1E293B")
            btn_close.pack(side="left", fill="x", expand=True, padx=(4, 0))

    def set_initial_data(self):
        if not self.log_data:
            today = datetime.datetime.now()
            self.cb_year.set(str(today.year))
            self.cb_month.set(f"{today.month:02d}")
            self.cb_day.set(f"{today.day:02d}")
            self.update_weekday_label()
            
            if self.parent.tree.get_children():
                last_item = self.parent.tree.get_children()[0]
                last_vals = self.parent.tree.item(last_item, "values")
                if last_vals and len(last_vals) > 2:
                    self.ent_worker.insert(0, last_vals[2])
        else:
            d = self.log_data
            try:
                y, m, d_val = d["work_date"].split("-")
                self.cb_year.set(y)
                self.cb_month.set(m)
                self.cb_day.set(d_val)
                self.update_weekday_label()
            except Exception:
                pass
                
            self.ent_worker.insert(0, d["worker_name"])
            self.ent_start_time.insert(0, d["start_time"])
            self.ent_end_time.insert(0, d["end_time"])
            
            self.ent_duration.config(state="normal")
            self.ent_duration.insert(0, d["duration_time"])
            self.ent_duration.config(state="readonly")
            
            self.ent_lot.insert(0, d["lot_number"] or "")
            self.ent_product.insert(0, d["product_name"] or "")
            self.ent_process.insert(0, d["process_code"] or "")
            
            qty_clean = str(d["quantity"] or "").replace(",", "")
            self.ent_qty.insert(0, qty_clean)
            self.ent_remarks.insert(0, d["remarks"] or "")

    def update_weekday_label(self, event=None):
        try:
            y = int(self.cb_year.get())
            m = int(self.cb_month.get())
            d = int(self.cb_day.get())
            
            dt = datetime.date(y, m, d)
            weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
            self.lbl_weekday.config(text=f"({weekdays[dt.weekday()]})")
        except Exception:
            self.lbl_weekday.config(text="(요일 오류)")

    def on_time_changed(self, event=None):
        start_str = self.ent_start_time.get().strip()
        end_str = self.ent_end_time.get().strip()
        time_pattern = re.compile(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
        
        if time_pattern.match(start_str) and time_pattern.match(end_str):
            duration = self.calculate_duration(start_str, end_str)
            self.ent_duration.config(state="normal")
            self.ent_duration.delete(0, tk.END)
            self.ent_duration.insert(0, duration)
            self.ent_duration.config(state="readonly")
        else:
            self.ent_duration.config(state="normal")
            self.ent_duration.delete(0, tk.END)
            self.ent_duration.config(state="readonly")

    def calculate_duration(self, start_str, end_str):
        try:
            sh, sm = map(int, start_str.split(':'))
            eh, em = map(int, end_str.split(':'))
            
            start_mins = sh * 60 + sm
            end_mins = eh * 60 + em
            
            if end_mins < start_mins:
                end_mins += 24 * 60
                
            diff_mins = end_mins - start_mins
            
            meal_times = [
                (12 * 60 + 30, 13 * 60 + 30),
                (17 * 60 + 30, 18 * 60)
            ]
            
            meal_overlap = 0
            for m_start, m_end in meal_times:
                overlap_start = max(start_mins, m_start)
                overlap_end = min(end_mins, m_end)
                if overlap_start < overlap_end:
                    meal_overlap += (overlap_end - overlap_start)
                    
                next_m_start = m_start + 24 * 60
                next_m_end = m_end + 24 * 60
                overlap_start_next = max(start_mins, next_m_start)
                overlap_end_next = min(end_mins, next_m_end)
                if overlap_start_next < overlap_end_next:
                    meal_overlap += (overlap_end_next - overlap_start_next)
                    
            diff_mins -= meal_overlap
            if diff_mins < 0:
                diff_mins = 0
                
            dh = diff_mins // 60
            dm = diff_mins % 60
            
            if dh > 0 and dm > 0:
                return f"{dh}시간 {dm}분"
            elif dh > 0:
                return f"{dh}시간"
            else:
                return f"{dm}분"
        except Exception:
            return ""

    def get_selected_date_str(self):
        try:
            return f"{self.cb_year.get()}-{self.cb_month.get()}-{self.cb_day.get()}"
        except Exception:
            return ""

    def validate_inputs(self):
        if not self.cb_year.get() or not self.cb_month.get() or not self.cb_day.get():
            messagebox.showerror("입력 오류", "작성일을 정확히 선택해주세요.", parent=self)
            return False
            
        worker = self.ent_worker.get().strip()
        if not worker:
            messagebox.showerror("입력 오류", "작업자 성명을 기입해 주세요.", parent=self)
            self.ent_worker.focus()
            return False
            
        start = self.ent_start_time.get().strip()
        end = self.ent_end_time.get().strip()
        time_pattern = re.compile(r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
        
        if not start or not time_pattern.match(start):
            messagebox.showerror("입력 오류", "시작 시간을 HH:MM 형식으로 정확히 입력해 주세요. (예: 08:30)", parent=self)
            self.ent_start_time.focus()
            return False
            
        if not end or not time_pattern.match(end):
            messagebox.showerror("입력 오류", "완료 시간을 HH:MM 형식으로 정확히 입력해 주세요. (예: 17:30)", parent=self)
            self.ent_end_time.focus()
            return False
            
        return True

    def add_log(self):
        if not self.validate_inputs():
            return
            
        qty_str = self.ent_qty.get().strip()
        try:
            quantity = int(qty_str) if qty_str else None
        except ValueError:
            quantity = qty_str
            
        database.insert_log(
            self.get_selected_date_str(), self.ent_worker.get().strip(),
            self.ent_start_time.get().strip(), self.ent_end_time.get().strip(),
            self.ent_duration.get().strip(), self.ent_lot.get().strip(),
            self.ent_product.get().strip(), self.ent_process.get().strip(),
            quantity, self.ent_remarks.get().strip()
        )
        
        self.parent.load_data()
        messagebox.showinfo("성공", "작업 내역이 등록되었습니다.", parent=self)
        self.destroy()

    def update_log(self):
        if not self.log_data or "id" not in self.log_data:
            return
            
        if not self.validate_inputs():
            return
            
        qty_str = self.ent_qty.get().strip()
        try:
            quantity = int(qty_str) if qty_str else None
        except ValueError:
            quantity = qty_str
            
        database.update_log(
            self.log_data["id"], self.get_selected_date_str(),
            self.ent_worker.get().strip(), self.ent_start_time.get().strip(),
            self.ent_end_time.get().strip(), self.ent_duration.get().strip(),
            self.ent_lot.get().strip(), self.ent_product.get().strip(),
            self.ent_process.get().strip(), quantity, self.ent_remarks.get().strip()
        )
        
        self.parent.load_data()
        messagebox.showinfo("성공", "작업 내역이 수정되었습니다.", parent=self)
        self.destroy()

    def delete_log(self):
        if not self.log_data or "id" not in self.log_data:
            return
            
        confirm = messagebox.askyesno("삭제 확인", "선택하신 작업 내역을 정말로 삭제하시겠습니까?", parent=self)
        if not confirm:
            return
            
        database.delete_log(self.log_data["id"])
        self.parent.load_data()
        messagebox.showinfo("성공", "작업 내역이 삭제되었습니다.", parent=self)
        self.destroy()

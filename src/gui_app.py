import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import sys

import database
import excel_exporter
from gui_dialog import JobLogDialog
from gui_components import create_custom_button

class MetalJobLogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        database.init_db()
        
        self.title("생산1팀 절곡 작업일지 시스템")
        self.geometry("980x600")
        self.minsize(920, 480)
        self.configure(bg="#F4F6F9")
        
        self.title_font = ("맑은 고딕", 16, "bold")
        self.section_font = ("맑은 고딕", 11, "bold")
        self.label_font = ("맑은 고딕", 10)
        
        # 상태 변수 초기화
        self.keep_worker = False
        self.saved_worker = ""
        self.duration_in_minutes = False
        
        self.setup_styles()
        self.create_widgets()
        
        self.set_today_date()
        self.load_data()

    def setup_styles(self):
        self.style = ttk.Style(self)
        try:
            if sys.platform.startswith("win"):
                self.style.theme_use("vista")
            else:
                self.style.theme_use("clam")
        except Exception:
            self.style.theme_use("clam")
        
        self.style.configure("TFrame", background="#F4F6F9")
        self.style.configure("Card.TFrame", background="#FFFFFF", relief="solid", borderwidth=1)
        self.style.configure("TLabel", background="#F4F6F9", font=self.label_font, foreground="#333333")
        self.style.configure("Card.TLabel", background="#FFFFFF", font=self.label_font, foreground="#333333")
        self.style.configure("Header.TLabel", background="#FFFFFF", font=self.title_font, foreground="#1E293B")
        self.style.configure("Section.TLabel", background="#FFFFFF", font=self.section_font, foreground="#0F172A")
        
        self.style.configure("Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            fieldbackground="#FFFFFF",
            rowheight=28,
            font=("맑은 고딕", 9),
            borderwidth=1,
            relief="solid",
            bordercolor="#CBD5E1",
            lightcolor="#CBD5E1",
            darkcolor="#CBD5E1"
        )
        self.style.configure("Treeview.Heading",
            background="#F1F5F9",
            foreground="#0F172A",
            font=("맑은 고딕", 9, "bold"),
            borderwidth=1,
            relief="solid",
            bordercolor="#CBD5E1"
        )
        self.style.map("Treeview",
            background=[("selected", "#3B82F6")],
            foreground=[("selected", "#FFFFFF")]
        )

    def create_widgets(self):
        title_card = ttk.Frame(self, style="Card.TFrame")
        title_card.pack(fill="x", padx=15, pady=10)
        title_inner = tk.Frame(title_card, bg="#FFFFFF", padx=15, pady=12)
        title_inner.pack(fill="x")
        
        ttk.Label(title_inner, text="생산1팀 절곡 작업일지 시스템", style="Header.TLabel").pack(side="left")
        
        btn_frame = tk.Frame(title_inner, bg="#FFFFFF")
        btn_frame.pack(side="right")
        
        self.btn_excel = create_custom_button(btn_frame, "엑셀 내보내기 (A4 규격)", "#107C41", "#159B52", self.export_excel)
        self.btn_excel.pack(side="right", padx=5)
        
        self.btn_help = create_custom_button(btn_frame, "[ ? ] 도움말", "#F59E0B", "#D97706", self.show_help_info, fg="#FFFFFF", active_fg="#FFFFFF")
        self.btn_help.pack(side="right", padx=5)
        
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.right_frame = ttk.Frame(main_container, style="Card.TFrame")
        self.right_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        right_inner = tk.Frame(self.right_frame, bg="#FFFFFF", padx=15, pady=15)
        right_inner.pack(fill="both", expand=True)
        
        filter_frame = tk.Frame(right_inner, bg="#FFFFFF")
        filter_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(filter_frame, text="작업 내역 목록 조회", style="Section.TLabel").pack(side="left")
        
        self.btn_new_log = create_custom_button(filter_frame, "[+] 신규 일지 작성", "#1E3A8A", "#1D4ED8", self.open_add_dialog)
        self.btn_new_log.pack(side="left", padx=15)
        
        self.btn_show_all = create_custom_button(filter_frame, "전체 목록 조회", "#E2E8F0", "#CBD5E1", self.load_all_data, fg="#1E293B", active_fg="#1E293B")
        self.btn_show_all.pack(side="right", padx=5)
        
        self.btn_show_today = create_custom_button(filter_frame, "선택 날짜 조회", "#E2E8F0", "#CBD5E1", self.load_data, fg="#1E293B", active_fg="#1E293B")
        self.btn_show_today.pack(side="right", padx=5)
        
        filter_date_frame = tk.Frame(filter_frame, bg="#FFFFFF")
        filter_date_frame.pack(side="right", padx=15)
        
        current_year = datetime.datetime.now().year
        self.cb_year = ttk.Combobox(filter_date_frame, values=[str(y) for y in range(current_year-2, current_year+3)], width=6, state="readonly")
        self.cb_year.pack(side="left", padx=(0, 2))
        tk.Label(filter_date_frame, text="년", bg="#FFFFFF", font=self.label_font).pack(side="left", padx=(0, 5))
        
        self.cb_month = ttk.Combobox(filter_date_frame, values=[f"{m:02d}" for m in range(1, 13)], width=4, state="readonly")
        self.cb_month.pack(side="left", padx=(0, 2))
        tk.Label(filter_date_frame, text="월", bg="#FFFFFF", font=self.label_font).pack(side="left", padx=(0, 5))
        
        self.cb_day = ttk.Combobox(filter_date_frame, values=[f"{d:02d}" for d in range(1, 32)], width=4, state="readonly")
        self.cb_day.pack(side="left", padx=(0, 2))
        tk.Label(filter_date_frame, text="일", bg="#FFFFFF", font=self.label_font).pack(side="left", padx=(0, 5))
        
        self.cb_year.bind("<<ComboboxSelected>>", self.on_filter_date_changed)
        self.cb_month.bind("<<ComboboxSelected>>", self.on_filter_date_changed)
        self.cb_day.bind("<<ComboboxSelected>>", self.on_filter_date_changed)
        
        table_frame = ttk.Frame(right_inner)
        table_frame.pack(fill="both", expand=True)
        
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")
        
        columns = ("id", "start", "end", "duration", "lot", "product", "process", "qty", "remarks", "date", "worker")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.heading("id", text="")
        self.tree.heading("start", text="시작")
        self.tree.heading("end", text="완료")
        self.tree.heading("duration", text="소요 (시간)", command=self.toggle_duration_format)
        self.tree.heading("lot", text="로트번호 및 구분")
        self.tree.heading("product", text="제품명")
        self.tree.heading("process", text="공정 및 도변")
        self.tree.heading("qty", text="작업수량")
        self.tree.heading("remarks", text="비고")
        self.tree.heading("date", text="작성일")
        self.tree.heading("worker", text="작업자")
        
        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.column("start", width=60, anchor="center")
        self.tree.column("end", width=60, anchor="center")
        self.tree.column("duration", width=70, anchor="center")
        self.tree.column("lot", width=140, anchor="center")
        self.tree.column("product", width=140, anchor="w")
        self.tree.column("process", width=130, anchor="center")
        self.tree.column("qty", width=80, anchor="e")
        self.tree.column("remarks", width=140, anchor="w")
        self.tree.column("date", width=90, anchor="center")
        self.tree.column("worker", width=70, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # 엑셀처럼 행을 쉽게 구분할 수 있도록 홀짝 행(Zebra 패턴) 배경색 대비 강화
        self.tree.tag_configure('oddrow', background='#CBD5E1') # 뚜렷하고 짙은 회색
        self.tree.tag_configure('evenrow', background='#FFFFFF') # 흰색        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.bind("<Button-1>", self.on_tree_click)

        # 3. 최하단 회사명 및 개발자 정보 푸터 (공식 기여도 반영용)
        footer_frame = tk.Frame(self, bg="#F4F6F9", padx=15, pady=6)
        footer_frame.pack(side="bottom", fill="x")
        
        lbl_info = tk.Label(footer_frame, text="제작자: (주)제이오텍 생산1팀 지윤호", font=("맑은 고딕", 9, "bold"), fg="#475569", bg="#F4F6F9")
        lbl_info.pack(side="right")
        
        lbl_ver = tk.Label(footer_frame, text="💡 더블클릭: 행 수정/삭제  |  상태: 정상 작동 중", font=("맑은 고딕", 9), fg="#64748B", bg="#F4F6F9")
        lbl_ver.pack(side="left")

    def set_today_date(self):
        today = datetime.datetime.now()
        self.cb_year.set(str(today.year))
        self.cb_month.set(f"{today.month:02d}")
        self.cb_day.set(f"{today.day:02d}")

    def on_filter_date_changed(self, event=None):
        self.load_data()

    def get_selected_date_str(self):
        try:
            return f"{self.cb_year.get()}-{self.cb_month.get()}-{self.cb_day.get()}"
        except Exception:
            return ""

    def load_data(self):
        date_str = self.get_selected_date_str()
        if not date_str:
            return
        logs = database.fetch_logs_by_date(date_str)
        self.populate_tree(logs)

    def load_all_data(self):
        logs = database.fetch_all_logs()
        self.populate_tree(logs)

    def populate_tree(self, logs):
        self.current_logs = logs # 현재 표시된 로그 저장
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for i, log in enumerate(logs):
            qty_val = log.get("quantity")
            if qty_val is not None and qty_val != "":
                try:
                    qty_fmt = f"{int(qty_val):,}"
                except (ValueError, TypeError):
                    qty_fmt = str(qty_val)
            else:
                qty_fmt = ""
                
            tag = 'oddrow' if i % 2 != 0 else 'evenrow'
            
            # 완료 시간 및 소요 시간 변환 처리
            end_time_val = log.get("end_time", "")
            if not end_time_val or end_time_val.strip() == "":
                end_time_display = "작업 중"
            else:
                end_time_display = end_time_val
                
            duration_val = log.get("duration_time", "")
            if not duration_val or duration_val.strip() == "" or duration_val == "작업 중":
                duration_display = "작업 중"
            else:
                duration_display = self.convert_duration_format(duration_val, self.duration_in_minutes)
            
            self.tree.insert("", "end", values=(
                log["id"], log["start_time"], end_time_display, duration_display,
                log["lot_number"] or "", log["product_name"] or "",
                log["process_code"] or "", qty_fmt, log["remarks"] or "",
                log["work_date"], log["worker_name"]
            ), tags=(tag,))

    def toggle_duration_format(self):
        """소요 시간 표시 형식을 토글합니다. (시간 분 <-> 분) 주석은 한국어입니다."""
        self.duration_in_minutes = not self.duration_in_minutes
        new_text = "소요 (분)" if self.duration_in_minutes else "소요 (시간)"
        self.tree.heading("duration", text=new_text)
        if hasattr(self, 'current_logs'):
            self.populate_tree(self.current_logs)

    def convert_duration_format(self, duration_str, to_minutes=False):
        """소요 시간 문자열을 지정된 형식(시간/분 또는 분)으로 변환합니다. 주석은 한국어입니다."""
        if not duration_str:
            return ""
        if duration_str == "작업 중":
            return "작업 중"
            
        import re
        hours = 0
        minutes = 0
        
        hour_match = re.search(r'(\d+)\s*시간', duration_str)
        min_match = re.search(r'(\d+)\s*분', duration_str)
        
        if hour_match:
            hours = int(hour_match.group(1))
        if min_match:
            minutes = int(min_match.group(1))
            
        total_mins = hours * 60 + minutes
        
        if to_minutes:
            if total_mins > 0:
                return f"{total_mins}분"
            return ""
        else:
            if hours > 0 and minutes > 0:
                return f"{hours}시간 {minutes}분"
            elif hours > 0:
                return f"{hours}시간"
            elif minutes > 0:
                return f"{minutes}분"
            return ""

    def open_add_dialog(self):
        dialog = JobLogDialog(self)
        self.wait_window(dialog)

    def on_tree_double_click(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        item = selected_items[0]
        val = self.tree.item(item, "values")
        if not val:
            return
            
        log_data = {
            "id": int(val[0]), "start_time": val[1], "end_time": val[2],
            "duration_time": val[3], "lot_number": val[4], "product_name": val[5],
            "process_code": val[6], "quantity": val[7], "remarks": val[8],
            "work_date": val[9], "worker_name": val[10]
        }
        
        dialog = JobLogDialog(self, log_data=log_data)
        self.wait_window(dialog)

    def on_tree_click(self, event):
        """빈 공간 클릭 시 포커스(선택) 해제"""
        item = self.tree.identify_row(event.y)
        if not item:
            # 클릭된 항목이 없으면(빈 공간) 선택 해제
            if self.tree.selection():
                self.tree.selection_remove(self.tree.selection())

    def export_excel(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("내보내기 경고", "엑셀로 저장할 작업 내역 데이터가 없습니다. 먼저 내역을 추가해 주세요.")
            return
            
        logs_to_export = []
        for item in items:
            val = self.tree.item(item, "values")
            qty_val = val[7].replace(",", "")
            try:
                qty_parsed = int(qty_val) if qty_val else None
            except ValueError:
                qty_parsed = qty_val
                
            logs_to_export.append({
                "id": val[0], "start_time": val[1], "end_time": val[2],
                "duration_time": val[3], "lot_number": val[4], "product_name": val[5],
                "process_code": val[6], "quantity": qty_parsed, "remarks": val[8],
                "work_date": val[9], "worker_name": val[10]
            })
            
        work_date = self.get_selected_date_str()
        
        worker = "전체"
        if len(logs_to_export) > 0:
            worker = logs_to_export[0]["worker_name"]
            for l in logs_to_export:
                if l["worker_name"] != worker:
                    worker = "공동작업"
                    break
        
        default_filename = f"절곡작업일지_{work_date}_{worker}.xlsx"
        
        file_path = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            y, m, d = work_date.split("-")
            dt = datetime.date(int(y), int(m), int(d))
            weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
            date_korean = f"{y}년 {m}월 {d}일 {weekdays[dt.weekday()]}"
        except Exception:
            date_korean = work_date
            
        try:
            excel_exporter.export_to_excel(
                logs=logs_to_export,
                file_path=file_path,
                work_date_str=date_korean,
                worker_name_str=worker
            )
            messagebox.showinfo("저장 완료", f"작업일지 엑셀 파일이 성공적으로 생성되었습니다.\n경로: {file_path}")
        except Exception as e:
            messagebox.showerror("저장 오류", f"엑셀 생성에 실패하였습니다.\n오류 정보: {str(e)}")

    def show_help_info(self):
        help_text = (
            "💡 [ 생산1팀 작업일지 시스템 핵심 꿀팁 ] 💡\n\n"
            "1. 더블클릭 수정/삭제\n"
            "   목록에 등록된 작업을 더블클릭하시면 수정 또는 삭제할 수 있습니다.\n\n"
            "2. 소요 시간 단위 변경 (시간 ↔ 분)\n"
            "   목록 맨 위 테이블 헤더의 '소요 (시간)' 글자를 마우스로 클릭해 보세요.\n"
            "   1시간 30분 형태와 90분 형태가 클릭할 때마다 바로 바뀝니다!\n\n"
            "3. 시간 입력 자동 완성 (: 생략 가능)\n"
            "   시간을 입력하실 때 콜론(:) 없이 '830', '1530' 이라고만 치고 넘어가면,\n"
            "   프로그램이 알아서 '08:30', '15:30'으로 변환해 드립니다.\n\n"
            "4. 병행 작업 한 방에 나누기 (비율 자동 배분)\n"
            "   하나의 긴 작업 시간에 여러 제품을 섞어서 작업하셨나요?\n"
            "   기존 작업을 더블클릭하여 수정한 뒤, 창 하단의 [병행 작업 나누기] 버튼을 누르세요.\n"
            "   제품명과 세트 수량만 툭툭 입력하시면, 5분 단위 현장 규칙에 맞춰서\n"
            "   시간이 자동 계산되고 한 방에 여러 줄로 예쁘게 쪼개져 등록됩니다!"
        )
        messagebox.showinfo("도움말 및 이용 팁", help_text, parent=self)

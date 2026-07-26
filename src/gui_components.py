import tkinter as tk
from tkinter import ttk

def create_custom_button(parent, text, bg, active_bg, command, fg="#FFFFFF", active_fg="#FFFFFF", font=("맑은 고딕", 10, "bold"), padx=10, pady=4):
    """테마를 무시하고 일관된 색상을 유지하는 커스텀 버튼 생성 (tk.Button 래퍼)"""
    return tk.Button(parent, text=text, 
                     bg=bg, fg=fg, font=font,
                     activebackground=active_bg, activeforeground=active_fg,
                     relief="flat", bd=0, cursor="hand2", padx=padx, pady=pady,
                     command=command)

def create_form_row(parent, label_text, row, font=("맑은 고딕", 10), width=28, example_text=None, state="normal"):
    """라벨과 텍스트 입력창(Entry)을 한 행에 배치하는 헬퍼 함수"""
    tk.Label(parent, text=label_text, bg="#FFFFFF", font=font).grid(row=row, column=0, sticky="w", pady=6)
    
    ent = ttk.Entry(parent, width=width)
    if state != "normal":
        ent.config(state=state)
        
    if example_text:
        ent.grid(row=row, column=1, sticky="w", pady=6)
        tk.Label(parent, text=example_text, fg="#64748B", bg="#FFFFFF", font=("맑은 고딕", 8)).grid(row=row, column=2, sticky="w", padx=5)
    else:
        ent.grid(row=row, column=1, columnspan=2, sticky="w", pady=6)
        
    return ent

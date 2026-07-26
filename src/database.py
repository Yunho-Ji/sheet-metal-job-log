import sqlite3
import os
import sys

def get_db_path():
    """실행 파일 또는 스크립트 위치를 기준으로 work_log.db 파일의 절대 경로를 반환합니다."""
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드되어 실행되는 경우 (.exe 실행 파일 위치)
        base_dir = os.path.dirname(sys.executable)
    else:
        # 일반 python 스크립트로 실행되는 경우 (database.py가 위치한 폴더 기준)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # 만약 src 하위 디렉토리에 있다면 상위 폴더를 기준으로 잡음
        if os.path.basename(base_dir) == 'src':
            base_dir = os.path.dirname(base_dir)
    return os.path.join(base_dir, 'work_log.db')

def get_connection():
    """SQLite3 데이터베이스 연결 객체를 생성하여 반환합니다. Row 객체로 결과를 반환하도록 설정합니다."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """데이터베이스 테이블이 없을 경우 새롭게 생성하고 기초 스키마를 초기화합니다."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_date TEXT NOT NULL,         -- 작성일 (YYYY-MM-DD)
            worker_name TEXT NOT NULL,       -- 작업자 성명
            start_time TEXT NOT NULL,        -- 시작시간 (HH:MM)
            end_time TEXT NOT NULL,          -- 완료시간 (HH:MM)
            duration_time TEXT NOT NULL,     -- 소요시간 (자동 계산 결과 저장)
            lot_number TEXT,                 -- 로트번호 및 구분
            product_name TEXT,               -- 제품명
            process_code TEXT,               -- 공정 및 도번
            quantity INTEGER,                -- 작업수량
            remarks TEXT                     -- 비고
        )
    """)
    conn.commit()
    conn.close()

def insert_log(work_date, worker_name, start_time, end_time, duration_time, lot_number, product_name, process_code, quantity, remarks):
    """신규 작업일지 데이터를 데이터베이스에 저장합니다."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO work_logs (
            work_date, worker_name, start_time, end_time, duration_time,
            lot_number, product_name, process_code, quantity, remarks
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (work_date, worker_name, start_time, end_time, duration_time, lot_number, product_name, process_code, quantity, remarks))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id

def update_log(log_id, work_date, worker_name, start_time, end_time, duration_time, lot_number, product_name, process_code, quantity, remarks):
    """기존 작업일지 데이터를 데이터베이스에서 수정합니다."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE work_logs
        SET work_date = ?,
            worker_name = ?,
            start_time = ?,
            end_time = ?,
            duration_time = ?,
            lot_number = ?,
            product_name = ?,
            process_code = ?,
            quantity = ?,
            remarks = ?
        WHERE id = ?
    """, (work_date, worker_name, start_time, end_time, duration_time, lot_number, product_name, process_code, quantity, remarks, log_id))
    conn.commit()
    conn.close()

def delete_log(log_id):
    """지정한 ID의 작업일지 데이터를 삭제합니다."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM work_logs WHERE id = ?", (log_id,))
    conn.commit()
    conn.close()

def fetch_all_logs():
    """전체 작업일지 목록을 작성일 및 시작시간 내림차순(최신순)으로 반환합니다."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM work_logs ORDER BY work_date DESC, start_time DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def fetch_logs_by_date(work_date):
    """특정 작성일의 작업일지 목록을 정렬하여 반환합니다."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM work_logs WHERE work_date = ? ORDER BY start_time ASC", (work_date,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

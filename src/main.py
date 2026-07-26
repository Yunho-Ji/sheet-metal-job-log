import os
import sys

# src 디렉토리를 모듈 경로에 추가하여 절대 경로 임포트 문제 방지
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_app import MetalJobLogApp

if __name__ == "__main__":
    app = MetalJobLogApp()
    app.mainloop()

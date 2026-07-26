import os
import sys
import shutil
import subprocess

def run_command(command, description):
    """지정한 셸 명령어를 실행하고 로그를 출력합니다."""
    print(f"[{description}] 실행 중: {command}")
    try:
        # Windows 환경에 맞게 shell=True로 실행
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"[{description}] 완료.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[{description}] 에러 발생! 반환 코드: {e.returncode}")
        print(f"표준 출력:\n{e.output}")
        print(f"표준 에러:\n{e.stderr}")
        return False

def main():
    print("=== 절곡 생산 작업일지 프로그램 EXE 빌드 프로세스 시작 ===")
    
    # 1. 필수 라이브러리 검사 및 설치
    run_command("pip install pyinstaller openpyxl", "필수 라이브러리 설치/업데이트")
    
    # 2. PyInstaller 빌드 실행
    # --onefile: 단일 파일 형태
    # --noconsole: GUI 전용으로 터미널 창 비활성화
    # --clean: 빌드 전 캐시 정리
    pyinstaller_cmd = 'pyinstaller --onefile --noconsole --clean --name="sheet_metal_job_log" src/main.py'
    build_success = run_command(pyinstaller_cmd, "PyInstaller 단일 파일 빌드")
    
    if not build_success:
        print("빌드에 실패하였습니다. 로그를 확인하세요.")
        sys.exit(1)
        
    # 3. 결과물 이동 (C:\\Users\\gamel\\.gemini\\Output\\sheet_metal_job_log)
    output_dir = r"C:\Users\gamel\.gemini\Output\sheet_metal_job_log"
    if not os.path.exists(output_dir):
        print(f"결과물 저장 폴더가 존재하지 않아 새로 생성합니다: {output_dir}")
        os.makedirs(output_dir)
        
    source_exe = os.path.join("dist", "sheet_metal_job_log.exe")
    target_exe = os.path.join(output_dir, "sheet_metal_job_log.exe")
    
    if os.path.exists(source_exe):
        try:
            # 타겟 경로에 이미 파일이 있다면 덮어쓰기 위해 사전 제거
            if os.path.exists(target_exe):
                os.remove(target_exe)
            shutil.copy2(source_exe, target_exe)
            print(f"\n[성공] 최종 실행 파일이 복사되었습니다.")
            print(f"이동 경로: {target_exe}")
            
            # 빌드 임시 폴더 및 파일 정리 (원하면 주석 해제)
            # shutil.rmtree("build")
            # shutil.rmtree("dist")
            # os.remove("sheet_metal_job_log.spec")
            
        except Exception as e:
            print(f"결과물 복사 중 에러 발생: {str(e)}")
            sys.exit(1)
    else:
        print("에러: 빌드 결과물인 exe 파일을 dist 폴더에서 찾을 수 없습니다.")
        sys.exit(1)

    print("\n=== 모든 빌드 및 파일 이동 프로세스가 성공적으로 끝났습니다! ===")

if __name__ == "__main__":
    main()

# Sheet Metal Job Log System (절곡 생산 작업일지 시스템)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)
![DB](https://img.shields.io/badge/Database-SQLite3-lightgrey)

생산 현장에서 수기로 관리되던 A4 규격의 절곡 생산 작업일지를 디지털화하고, 결재 양식에 맞춘 엑셀(Excel) 자동 변환을 지원하는 독립 실행형 데스크톱 애플리케이션입니다. 

기존 수기 작성 시 발생하던 시간 계산 오류를 방지하고 데이터 보관의 안정성을 높이기 위해 개발되었습니다. 별도의 서버나 복잡한 설치 과정 없이 단일 실행 파일(.exe)로 동작하며 데이터는 로컬에 안전하게 저장됩니다.

---

## ✨ 주요 기능 (Key Features)

- **작업 내역 관리 (CRUD)**: 날짜, 작업자, 시작/종료 시간, 품번, 공정, 수량 등 상세 작업 정보의 기록, 수정 및 삭제.
- **스마트 시간 연산 (Smart Time Calculation)**: 
  - `HH:MM` 포맷 입력 시 작업 소요 시간 자동 계산.
  - 야간 작업 시 자정을 넘기는 시간(예: 22:00 ~ 03:00) 자동 인식 및 24시간 가산 연산 처리.
  - 점심시간(12:30~13:30) 및 저녁시간(17:30~18:00) 자동 차감 알고리즘 적용.
- **날짜 기반 인덱싱**: 달력 데이터에 기반한 요일 자동 연산 및 선택한 날짜 기준 작업 내역 필터링 제공.
- **결재용 엑셀 출력 (Excel Export)**:
  - 사내 결재 양식을 엄격하게 준수하는 A4 가로 규격 프린트 옵션(Fit to Width) 최적화.
  - 상단 결재란 자동 생성 및 병합 적용.
- **직관적인 모던 GUI**: 윈도우 네이티브 테마(Vista) 및 가독성을 극대화한 Zebra 패턴 렌더링, 모달(Modal) 팝업 구조 적용.

---

## 🚀 시작하기 (Getting Started)

### 1. 일반 사용자 (배포용 실행 파일 사용 시)
- **요구 사항**: 없음 (Windows 10 / 11 환경이면 즉시 실행 가능)
- **실행 방법**:
  - 빌드된 단일 실행 파일(`sheet_metal_job_log.exe`)을 더블클릭하여 실행합니다.
  - **별도의 Python 설치나 라이브러리 설치가 전혀 필요 없습니다.**

### 2. 개발자 및 재빌드 환경 (소스 코드 수정/빌드 시)
소스 코드를 직접 실행하거나 새로운 EXE 파일로 재빌드하려는 경우에만 아래 요구 사항이 필요합니다.

- **필수 개발 환경**:
  - Python 3.8 이상
  - `openpyxl` (엑셀 파일 처리 라이브러리)
  - `pyinstaller` (실행 파일 빌드 도구)

#### 소스 코드 직접 실행
```bash
git clone <repository-url>
cd sheet_metal_job_log
pip install openpyxl
python src/main.py
```

#### 실행 파일(.exe) 빌드 방법
```bash
python build_exe.py
```
- 빌드가 완료되면 프로젝트 루트 경로에 `sheet_metal_job_log.exe` 파일이 생성됩니다.
- 생성된 실행 파일은 Python이 설치되지 않은 환경에서도 더블클릭만으로 즉시 실행 가능합니다.

---

## 📂 프로젝트 구조 (Project Structure)

```text
sheet_metal_job_log/
├── src/
│   ├── main.py              # 애플리케이션 진입점 (Entry Point)
│   ├── gui_app.py           # 메인 윈도우 및 Treeview 그리드 컨트롤러
│   ├── gui_dialog.py        # 데이터 CRUD 처리용 모달 다이얼로그
│   ├── gui_components.py    # 재사용 가능한 UI 팩토리 패턴 모듈
│   ├── database.py          # SQLite3 데이터베이스 인터페이스 
│   └── excel_exporter.py    # openpyxl 기반 결재 엑셀 포매터
├── build_exe.py             # PyInstaller 자동화 빌드 스크립트
├── sheet_metal_job_log.spec # PyInstaller 빌드 명세서
└── README.md                # 프로젝트 소개 문서
```

---

## ⚙️ 시스템 아키텍처 (Architecture)

- **UI Framework**: Python 표준 라이브러리인 `tkinter`와 `ttk`를 활용한 이벤트 드리븐(Event-driven) 아키텍처.
- **Database**: `sqlite3`를 사용하여 실행 파일과 동일한 경로에 `work_log.db`를 자동 생성 및 로컬 데이터 영구 보존.
- **Data Export**: `openpyxl` 모듈을 통한 무손실 셀 서식 지정 및 바이트 스트림 파일 저장.

---

## 📝 라이선스 (License)

## 👥 개발 및 기획 (Developer)

- **기획 및 개발자**: 지윤호 (Ji Yunho)
- **소속**: (주)제이오텍 생산1팀 (Production Team 1, J-Oh Tech)
- **역할**: 요구사항 정의, 데이터베이스 설계, GUI 인터페이스 개발, 엑셀 결재 포맷 자동화 스크립트 작성 및 독립 배포 패키지 구성 총괄.

---

## 📝 라이선스 (License)

이 프로젝트는 (주)제이오텍 사내 생산 관리 목적으로 개발되었습니다. 외부 배포 시 라이선스 정책을 참고해 주시기 바랍니다.
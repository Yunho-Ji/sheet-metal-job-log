# 📅 daily_log - 2026.07.27 (월요일)

생산1팀 절곡 작업일지 시스템 리팩토링, 2차 기능 보완(병행 작업 분할, 도움말, 시간 자동완성) 및 배포본 빌드 작업 완료 일지입니다.

---

## 🛠️ 오늘 수행한 작업 (Work Accomplished)

### 1. 코드 리팩토링 및 모듈화 (구조 개편)
- **목적**: 850줄에 달하던 거대한 `main.py` 파일을 기능별로 쪼개어 장기적인 유지보수성 및 코드 가독성을 대폭 향상.
- **수행 내용**:
  - `src/gui_components.py` (신설): 폰트, 패딩, 색상 등 중복 작성이 많았던 공통 UI 요소(버튼, 입력창 등)를 찍어내는 팩토리 모듈 작성.
  - `src/gui_dialog.py` (신설): 일지 추가/수정/삭제 작업을 처리하는 `JobLogDialog` 모달 클래스 분리.
  - `src/gui_app.py` (신설): 메인 화면 구성 및 리스트(Treeview) 조작, 엑셀 내보내기 등을 담당하는 `MetalJobLogApp` 클래스 분리.
  - `src/main.py` (수정): 코드 복잡도를 0에 가깝게 줄이고, 단순 진입점(Entry Point) 역할로 최소화.

### 2. 사용자 피드백 기반 UI/UX 디테일 개선
- **지브라(얼룩말) 패턴 가독성 보완**: 홀수 행의 연회색 채도(`Slate 300` 톤)를 올려 리스트 데이터 식별을 한층 더 수월하게 조치.
- **빈 공간 클릭 시 선택 해제**: 표 내부의 데이터가 없는 빈 공간을 클릭하면 선택(포커스) 띠가 깔끔하게 지워지도록 마우스 바인딩 추가.
- **노트북 화면 최적화**: 
  - 기본 실행 화면 크기를 `980x600`(최소 `920x480`)으로 축소하여 해상도가 작거나 배율이 확대된 노트북 화면에서도 위아래 잘림 없이 실행되도록 보완.
  - 가로 공간 확보를 위해 상단의 긴 더블클릭 힌트를 최하단 상태바(푸터)로 이관.
- **날짜 필터 레이블 명시**: 년, 월, 일 콤보박스 옆에 명확히 `년`, `월`, `일` 텍스트를 출력하여 시인성 제고.
- **소요 시간 표기 전환**: 메인 화면 테이블에서 "소요 (시간)" 컬럼 헤더를 마우스로 클릭하면 "2시간 10분" ↔ "130분"으로 표기 형식이 즉시 토글되는 기능 탑재.

### 3. 기여도 반영 및 공식 크레딧 추가
- **화면 푸터**: 메인 화면 최하단 상태바 오른쪽에 `제작자: (주)제이오텍 생산1팀 지윤호` 공식 표기 적용.
- **README.md 개편**: 대외 깃허브 공개 및 인사고과 증빙용으로 부족함이 없도록 소속, 이름, 개발 기여 영역(DB, GUI, 엑셀 필터 알고리즘 등)을 전문 용어로 작성 및 전면 교체.

### 4. 2차 기능 보강 및 5분 단위 병행 작업 분할기 추가
- **병행 작업 비례 시간 분할기 (`src/gui_split_dialog.py` 신설)**:
  - 130분 작업에 여러 제품을 병행 작업한 경우, 수량 비율에 따라 소요 시간을 자동으로 쪼개어 여러 개의 작업일지로 일괄 전환/등록하는 모달 구현.
  - **5분 단위 자동 보정 알고리즘**: 배분된 시간이 5분 단위의 깔끔한 숫자로 떨어지게 정규화하며, 단수 오차는 수량이 가장 큰 메인 작업에 가감 보정.
- **[ ? ] 도움말 버튼 추가**: 메인 화면 우측 상단에 헬프 아이콘 버튼을 신설하여 시간 자동 완성 팁, 더블클릭 수정 팁, 시간 분할기 기능 안내를 실시간 팝업으로 제공.
- **시간 자동 완성 예외처리**: 시간 입력 시 콜론(`:`)의 입력 유무에 구애받지 않고 무조건 `08:30` 또는 `15:00` 정규 포맷으로 보정하는 예외 처리 완성.

### 5. 2차 배포본 빌드 및 Git 기록 완료
- `build_exe.py` 스크립트를 재구동하여 위 개선 기능이 포함된 최신 `.exe` 실행 파일(Windows 단일 실행 무설치본)을 성공적으로 빌드.
- 불필요한 빌드 캐시 및 데이터베이스 파일이 추적되지 않도록 `.gitignore` 세팅 후 로컬 커밋 완료.

---

## 📂 변경된 파일 목록 (File Changes)

- `[NEW]` [src/gui_split_dialog.py](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/src/gui_split_dialog.py) - 수량 비례 5분 단위 시간 분할 모달 창 클래스
- `[MODIFY]` [src/gui_dialog.py](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/src/gui_dialog.py) - 시간 자동완성 예외처리 및 병행 작업 분할기 호출 연동
- `[MODIFY]` [src/gui_app.py](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/src/gui_app.py) - 메인 화면 도움말 버튼 UI 배치 및 가이드 메시지 작성
- `[NEW]` [src/gui_components.py](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/src/gui_components.py) - 공통 UI 생성 팩토리 함수
- `[NEW]` [src/gui_dialog.py](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/src/gui_dialog.py) - 입력/수정/삭제 모달 창 클래스
- `[NEW]` [src/gui_app.py](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/src/gui_app.py) - 메인 화면 및 엑셀 출력 기능
- `[MODIFY]` [src/main.py](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/src/main.py) - 엔트리 포인트 단일화
- `[MODIFY]` [README.md](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/README.md) - 사용자 요구사항 구별 및 지윤호 개발자 공헌 기술서 명시
- `[NEW]` [.gitignore](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/.gitignore) - 테스트 데이터베이스 및 빌드 캐시 예외 정의
- `[BUILD]` [sheet_metal_job_log.exe](file:///C:/Users/gamel/.gemini/Output/sheet_metal_job_log/sheet_metal_job_log.exe) - 최종 배포용 무설치 단일 파일

---

## 🔮 다음 작업 제안 (Next Steps)

1. **원격 깃허브 푸시**:
   - 로컬에 커밋된 최신 빌드 완료 버전을 원격 깃허브 저장소로 푸시(`git push origin main`)하여 백업 및 소스 관리 완료하기.
2. **현장 시범 배포 및 검증**:
   - `sheet_metal_job_log.exe` 파일을 실제 현장의 절곡기 옆 노트북에 옮겨두고 작업자에게 분할 입력 및 시간 자동 포맷 기능을 테스트하도록 요청하고 피드백 받기.
3. **타 부서(용접/기타 생산) 피드백 수집 및 확장 설계**:
   - 현장 시범 사용 중 발생하는 피드백을 반영하여 추후 타 공정 일지로의 범용화 설계 진행.

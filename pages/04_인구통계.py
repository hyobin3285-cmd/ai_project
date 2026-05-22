# 수정 전: df = pd.read_csv(uploaded_file)
    
    # 수정 후: 인코딩 예외 처리가 추가된 데이터 로드 코드
    try:
        # 일반적인 정부 공공데이터/엑셀용 한글 인코딩(cp949)으로 먼저 시도
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except UnicodeDecodeError:
        try:
            # 실패 시 일반적인 한글 인코딩(euc-kr)으로 시도
            df = pd.read_csv(uploaded_file, encoding='euc-kr')
        except UnicodeDecodeError:
            # 둘 다 실패 시 표준 UTF-8로 시도
            df = pd.read_csv(uploaded_file, encoding='utf-8')

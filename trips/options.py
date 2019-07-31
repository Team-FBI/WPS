#최소 나이에 관한 선택 값 - 인티저 초이스
MIN_AGE = [(x, x) for x in range(2, 30)]

#장애인의 이용 여부에 관한 선택 값 - 문자열 초이스
YES = "YES"
NO = "NO"
COMPATIBILITY = (
    (YES, "적합하지 않음"),
    (NO, "예"),
)

#트립의 강도에 관한 선택 값 - 문자열 초이스
LIGHT = "LIGHT"
NORMAL = "NORMAL"
VEHEMENCE = "VEHEMENCE"
EXTREME = "EXTREME"
STRENGTH = (
    (LIGHT, "가벼움"),
    (NORMAL, "보통"),
    (VEHEMENCE, "격렬함"),
    (EXTREME, "익스트림"),
)

#트립의 테크닉 요구 수준 - 문자열 초이스
BEGINNER = "BEGINNER"
INTERMEDIATE = "INTERMEDIATE"
MASTER = "MASTER"
TECHNIC = (
    (BEGINNER, "초급"),
    (INTERMEDIATE, "중급"),
    (MASTER, "고")
)

#최대 수용 게스트 - 인티저 초이스
MAX_GUEST = [(x, x) for x in range(1, 11)]
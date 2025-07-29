# 🗂️ Django 모델 명세서

## 📌 User 모델 (`users/models.py`)

| 필드명          | 타입                                | 설명                                  | 제약 조건                        |
|------------------|-------------------------------------|----------------------------------------|----------------------------------|
| email            | EmailField                          | 사용자 이메일                          | `unique=True`, 필수              |
| nickname         | CharField(max_length=30)            | 사용자 닉네임                          | `unique=True`, 필수              |
| profile_image    | ImageField(upload_to='profiles/')   | 프로필 이미지                          | `blank=True`, `null=True`        |
| is_active        | BooleanField                        | 계정 활성화 여부                       | 기본값: `True`                   |
| is_staff         | BooleanField                        | 관리자 권한 여부                       | 기본값: `False`                  |
| date_joined      | DateTimeField                       | 가입 일시                              | 기본값: `timezone.now`           |

- 인증 관련 설정:  
  - `USERNAME_FIELD = 'nickname'`  
  - `REQUIRED_FIELDS = ['email']`

- 매니저: `UserManager`  
  - `create_user()`, `create_superuser()` 메서드 포함

---

## 📌 TimeMarker 모델 (`posts/models.py`)

| 필드명          | 타입                    | 설명                                   | 제약 조건                  |
|------------------|-------------------------|----------------------------------------|----------------------------|
| user             | ForeignKey(User)        | 작성자 (사용자)                         | `on_delete=CASCADE`        |
| title            | CharField(max_length=100)| 제목                                   | 필수                        |
| description      | TextField               | 상세 설명                              | 필수                        |
| is_help_request  | BooleanField            | `True`: 도움요청, `False`: 시간 판매    | 기본값: `False`            |
| latitude         | FloatField              | 위도                                    | 필수                        |
| longitude        | FloatField              | 경도                                    | 필수                        |
| created_at       | DateTimeField           | 생성일시                                | `auto_now_add=True`         |
| is_active        | BooleanField            | 거래 활성 여부                          | 기본값: `True`             |

---

## 📌 TimePost 모델 (`posts/models.py`)

| 필드명          | 타입                      | 설명                                    | 제약 조건                   |
|------------------|---------------------------|------------------------------------------|-----------------------------|
| user             | ForeignKey(User)          | 작성자 (사용자)                           | `on_delete=CASCADE`         |
| title            | CharField(max_length=100) | 게시글 제목                              | 필수                         |
| description      | TextField                 | 게시글 설명                              | 필수                         |
| type             | CharField                 | `sale` (시간 판매) / `request` (구인)     | 필수 (`choices` 지정)       |
| latitude         | FloatField                | 위치 위도                                | `null=True`, `blank=True`   |
| longitude        | FloatField                | 위치 경도                                | `null=True`, `blank=True`   |
| created_at       | DateTimeField             | 작성일시                                 | `auto_now_add=True`          |
| price            | IntegerField              | 거래 시간 가격                           | 기본값: `0`                 |

---

## 📌 Wallet 모델 (`wallet/models.py`)

| 필드명          | 타입                          | 설명                                 | 제약 조건                   |
|------------------|-------------------------------|--------------------------------------|-----------------------------|
| user             | OneToOneField(User)           | 지갑 소유 사용자                      | `on_delete=CASCADE`, 고유   |
| balance          | DecimalField(max_digits=10, decimal_places=2) | 잔액 (시간 단위)      | 기본값: `0.00`              |

---

## 📌 Transaction 모델 (`wallet/models.py`)

| 필드명           | 타입                          | 설명                                 | 제약 조건                     |
|------------------|-------------------------------|--------------------------------------|-------------------------------|
| wallet           | ForeignKey(Wallet)            | 연결된 지갑                          | `on_delete=CASCADE`           |
| transaction_type | CharField                     | 거래 유형: 입금, 출금, 이체          | `choices=TRANSACTION_TYPES`   |
| amount           | DecimalField(max_digits=10, decimal_places=2) | 거래량 (시간)         | 필수                           |
| timestamp        | DateTimeField                 | 거래 일시                            | 기본값: `timezone.now`        |
| note             | CharField(max_length=255)     | 비고 메모                            | `blank=True`, `null=True`     |

---

## 🔗 모델 관계 요약

- **User ↔ Wallet**: 1:1 관계
- **User ↔ TimeMarker**: 1:N 관계
- **User ↔ TimePost**: 1:N 관계
- **Wallet ↔ Transaction**: 1:N 관계

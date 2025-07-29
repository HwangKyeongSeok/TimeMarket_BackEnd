# 📄 API 명세서 - TimeMarket

> 이 문서는 TimeMarket\_BackEnd 프로젝트의 전체 API 명세를 설명합니다.

---

## 🔧 기본 전제

* **인증 방식**: JWT (로그인 시 액세스 토큰 발급)
* **Base URL**: `/api/`
* 모든 엔드포인트는 `/api/`로 시작합니다.

---

## 📍 사용자 관련 (Users)

| 메서드   | 엔드포인트               | 설명           |
| ----- | ------------------- | ------------ |
| POST  | /auth/signup/       | 회원가입         |
| POST  | /auth/login/        | 로그인 (JWT 발급) |
| GET   | /users/me/          | 내 정보 가져오기    |
| PATCH | /users/me/          | 내 정보 수정      |
| GET   | /users/\<user\_id>/ | 다른 사용자 정보 보기 |

/auth/signup/ 에는 'nickname', 'email', 'password' 가 unique 하게 들어와야함.

---

## 🕒 시간 판매 / 구인 관련 (Time Posts)

| 메서드    | 엔드포인트                    | 설명                                                   |
| ------ | ------------------------ | ---------------------------------------------------- |
| GET    | /time-posts/             | 주변 시간 판매/구인 목록 (쿼리: `?lat=37.5&lng=127.0&type=sale`) |
| POST   | /time-posts/             | 시간 판매 or 구인 글 등록                                     |
| GET    | /time-posts/\<post\_id>/ | 개별 글 상세 보기                                           |
| PATCH  | /time-posts/\<post\_id>/ | 글 수정                                                 |
| DELETE | /time-posts/\<post\_id>/ | 글 삭제                                                 |
| GET    | /time-posts/board/       | GPS 없이 게시판형 조회                                       |

---

## 📬 채팅 / 거래 연결 (Matching & Chat)

> 초기에는 REST 방식, 추후 WebSocket `/ws/chat/<room_id>/`으로 전환 가능

| 메서드  | 엔드포인트                             | 설명                   |
| ---- | --------------------------------- | -------------------- |
| POST | /match/request/                   | 특정 글에 매칭 요청 (채팅방 생성) |
| GET  | /match/my-chats/                  | 내가 참여 중인 채팅방 목록      |
| GET  | /match/chat/\<room\_id>/          | 채팅방 상세 정보 조회         |
| POST | /match/chat/\<room\_id>/messages/ | 메시지 전송               |
| GET  | /match/chat/\<room\_id>/messages/ | 메시지 불러오기             |

---

## 📅 거래 관리 (Deal)

| 메서드  | 엔드포인트                       | 설명                      |
| ---- | --------------------------- | ----------------------- |
| POST | /deal/\<room\_id>/schedule/ | 약속 시간 잡기                |
| POST | /deal/\<room\_id>/confirm/  | 거래 성사 버튼 (약속 시간 이후만 가능) |
| GET  | /deal/history/              | 거래 완료 내역 조회             |

---

## 🌟 평가 시스템 (Review)

| 메서드  | 엔드포인트                 | 설명               |
| ---- | --------------------- | ---------------- |
| POST | /reviews/\<user\_id>/ | 해당 사용자에 대한 평가 등록 |
| GET  | /reviews/\<user\_id>/ | 특정 사용자 리뷰 목록 조회  |

---

## 🗺️ GPS 기반 마커 데이터

| 메서드 | 엔드포인트         | 설명                                     |
| --- | ------------- | -------------------------------------- |
| GET | /map/markers/ | 현재 위치 기준 마커 목록 조회 (`?lat=...&lng=...`) |
| GET | /map/cluster/ | 클러스터링된 마커 정보 (선택)                      |

---

## 💰 지갑 기능 (Wallet)

| 메서드  | 엔드포인트                 | 설명                |
| ---- | --------------------- | ----------------- |
| GET  | /wallet/balance/      | 내 시간 잔액 조회        |
| POST | /wallet/deposit/      | 시간 충전 (관리자 승인 가능) |
| POST | /wallet/withdraw/     | 시간 출금 요청          |
| POST | /wallet/transfer/     | 사용자 간 시간 전송       |
| GET  | /wallet/transactions/ | 시간 거래 내역 조회       |

---

추가적인 API 스펙, 응답/요청 스키마, 상태 코드 등은 추후 문서화 예정입니다.

📌 You know what I'm saying
-
- Text to image 
- 텍스를 입력하면 그림을 그려주는 AI
- DallE-2를 모티브로 프로젝트 진행

📌 Introduction
-    
- 프로젝트명: 유남생
- 기간: 2022.06.28 ~ 2022.07.05   
   
📌 핵심기능
-   
### 1. 로그인/회원가입      
> - 유효성 검사, 아이디 중복 검사, JWT Token사용   

### 2. 메인 페이지
> - Diffusion Model을 이용하여 Text-to-image 기능 구현
> - 댓글 CRUD
> - 평점 CRUD

### 3. 마이페이지
> - 자신이 작성한 댓글, 아티클 필터링하여 조회

### 4. Nginx / Gunicorn
> - Nginx : Proxy 역할
> - Gunicorn : Django 배포용 WSGI서버 http protocol 요청 처리

📌 핵심 트러블 슈팅  
-   
1) EC2 프리티어의 한계..
> - 에러: EC2 환경에서 서버를 돌리면 처음 Run Server를 할때 모델을 load해 오는데 이 과정에서 서버가 Kill 되는 현상
> - 문제점: EC2 프리티어의 사용가능한 메모리는 1GB인데 이 모델을 돌리기엔 부족했다.
> - 해결: 이 문제의 해결방법은 Cuda를 지원해주는 AI 전용 서버를 사야하는 것인데... 학생입장에서 부담스러운 금액이여서 팀원들과 합의하에 AI모델을 빼고 배포 하기로 결정하였다.


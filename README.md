# keyfa
keyfa(**k**o**e**un**y**eon **f**ast **a**pi)는 [FastAPI](https://fastapi.tiangolo.com/ko/) 기반 프로젝트 템플릿입니다.  
FastAPI로 프로젝트를 구성할 때마다 매 번 똑같은 작업을 해야 하는 것이 지겨워서 템플릿화한 후 공개합니다.
원래는 [devmini](https://github.com/koeunyeon/devmini) 프로젝트의 일부였으나, 현재는 독립적으로 관리됩니다.

# 포함된 기능
- FastAPI + SQLAlchemy 연동 + 로거 + 어드바이스 미들웨어 
- MySQL(MariaDB) 데이터베이스 및 테이블 생성 쿼리 작성
- 배포 스크립트 템플릿
- 환경 설정 템플릿
- 라우터 자동 등록
- 날짜, jwt, 로그, 예외, RDB 관련 유틸리티 포함.

# 설치 및 실행
## 다운로드
깃헙 프로젝트 페이지에서 최신 버전 [릴리즈](https://github.com/koeunyeon/keyfa/releases)를 다운로드하세요.

## 의존성 설치
가상환경을 만들고, 의존성을 설치해 주세요.
### windows
```
python -m virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt
```

### linux
```
python -m virtualenv venv
venv/bin/activate
pip install -r requirements.txt
```

## 실행
```
cd server
python app.py
```

http://localhost:5000/docs#/ 에 접속했을 때 `/keyfa/health`, `/keyfa/openapi.yaml` 두개의 엔드포인트가 보이면 성공입니다.


# 데이터베이스 설정
## MySQL 데이터베이스 생성
```
cd gen
python mysql.py db keyfa_db
```
`keyfa_db`는 원하시는 데이터베이스 이름으로 변경하세요.

터미널 출력에 DML 쿼리가 보여집니다. 또한 `gen/mysql.gen.log` 파일에도 기록이 쌓입니다.
```
db keyfa_db
-------------------------
create database `keyfa_db` /*!40100 COLLATE 'utf8mb4_general_ci' */;
```

해당 쿼리를 복사해서 DBMS 툴에 붙여넣고 실행하세요.

## MySQL 테이블 생성
```
python mysql.py table product: name, category_id, price.type=int.default=0
```

`mysql.gen.log`
```
table product: name, category_id, price.type=int.default=0
-------------------------

CREATE TABLE `product` 
( 
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;    
    ALTER TABLE `product` ADD `name` VARCHAR(255) NULL  ;
ALTER TABLE `product` ADD `category_id` INT UNSIGNED NULL  ;
ALTER TABLE `product` ADD `price` INT NULL DEFAULT '0' ;
ALTER TABLE `product` ADD `created_at` datetime NOT NULL  DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE `product` ADD `updated_at` datetime NULL  on update CURRENT_TIMESTAMP;
ALTER TABLE `product` ADD `use_yn` CHAR(1) NOT NULL DEFAULT 'Y' ;
```

해당 쿼리를 복사해서 DBMS 툴에 붙여넣고 실행하세요.

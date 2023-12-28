- 사용자 이름은 **keyfa_user**로 가정.
- 서비스 이름은 **keyfa**로 가정.

# 서비스 등록
deploy/service/keyfa.service 파일을 `/home/keyfa_user/.config/systemd/user/keyfa.service` 에 등록


# 서비스 시작
## 시스템 스크립트 내용 변경시
```sh
sudo systemctl daemon-reload
```
시스템 스크립트 변경시 1회 실행

## 서비스 활성화
```sh
systemctl --user enable keyfa
```
최초 등록. 1회성.

## 서비스 상태 확인
```sh
systemctl --user status keyfa
```

## 서비스 시작
```sh
systemctl --user start keyfa
```

## 서비스 정지
```sh
systemctl --user stop keyfa
```

## 서비스 재시작
```sh
systemctl --user restart keyfa
```

# Linger
## 개요
ssh 접속 끊어졌을 때도 서비스가 실행되게 하기 위한 서비스 

## Linger 등록
```sh
sudo loginctl enable-linger $USER
```

## Linger 확인
```sh
sudo loginctl show-user $USER --property Linger
ls /var/lib/systemd/linger
```
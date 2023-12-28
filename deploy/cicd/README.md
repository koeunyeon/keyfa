- 사용자 이름은 **keyfa_user**로 가정.

# 초기 디렉토리 생성
```sh
mkdir ~/project/cicd
mkdir ~/project/cicd/backup
mkdir ~/project/cicd/latest
mkdir ~/project/cicd/temp
```

리눅스의 ~/project 디렉토리 아래에 deploy/cicd/cicd 디렉토리를 업로드.

# 경로
- ~/project/cicd/backup : 젠킨스에서 전달된 zip 파일을 백업하는 디렉토리
- ~/project/cicd/latest : 젠킨스에서 서버로 파일을 전달하는 경로. 전체 경로는 ~/project/cicd/latest/keyfa_service_api.zip
- ~/project/cicd/temp : ~/project/cicd/latest/keyfa_service_api.zip 파일의 임시 압축 해제 경로


# 배포 스크립트
```sh
chmod 755 deploy.sh
chmod 755 rollback.sh
```

---------------------------------------------
CICD 용 배포 세팅.
# authorized_keys 등록
## 젠킨스쪽 작업.
### ssh key 생성
```
ssh-keygen
```
`id_rsa`,  `id_rsa.pub` 생성됨.

## 서버측 작업
젠킨스에서 생성된 `id_rsa.pub` 파일 내용을 ~/.ssh/authorized_key 에 복사

## 젠킨스로 돌아와서 
### 접속 테스트
ssh server_user@1.2.3.4


# 참고. 젠킨스에서 서버로 푸시할 때
## rsync
```
rsync -avh ./keyfa_service_api.zip keyfa_user@192.168.0.1:/home/keyfa/project/cicd/latest/keyfa_service_api.zip
```

## 커맨드 실행
```
sh -o 'StrictHostKeyChecking no' keyfa_user@192.168.0.1 /home/keyfa/project/cicd/deploy.sh
```
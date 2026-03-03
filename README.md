
# jdk-manager

open-jdk 의 배포판을 다운로드 및 설치하고 관리 하는 CLI 프로그램

앞으로 나오는 jdk 는 실행 파일명 => 개발중엔 `uv run main.py` 로 대체


## 자바 패키지 데이터베이스
```
resp = requests.get("https://mise-java.jdx.dev/jvm/ga/macosx/aarch64.json")
resp.raise_for_status()

data = resp.json()
df = pd.DataFrame(data)
이 df 를 사용한다.
```



## 사용법

```
jdk

아래 메시지 출력
usage: jdk [command] [jdk-package]
```


```
jdk download zulu-11

df 에서 vendor 가 zulu 이고, 버전이 11 인 최신 배포판을 다운로드 한다 - 현재디렉토리의 /temp 디렉토리에

```



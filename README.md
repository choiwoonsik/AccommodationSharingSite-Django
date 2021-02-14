# Accommodation Sharing Site

### [DESCRIPTION]

- WebPage of sharing accommodation by any people
- 숙박 공유 사이트 제작 개인 프로젝트

---

### [사용한 언어 및 기술]

- Python, Django, HTML, CSS
- back-end : Django
- front-end : Django 템플릿 시스템으로 구성
  - React를 사용하지 않은 이유
    - 상호작용이 많은 경우가 아니면 굳이 사용할 필요가없다
    - 콘텐츠 위주의 사이트 이므로 React를 굳이 선택할 필요가 없다
    - Django 템플릿으로도 반응형 웹사이트를 충분히 만들수 있다
- 모든 작업은 pipenv 가상환경위에서 진행되었다 (Pipenv shell)

---

### [기초 설정]

1. Pipenv 가상환경을 위해서 `pipevn --three` (파이썬3 환경)을 입력해서 파이썬3를 위한 가상환경을 생성 후 `Pipenv shell`을 입력해서 가상환경으로 들어간다
2. `Pipenv install Django=2.2.5` (버전이름 생략시 최신버전 설치)를 통해 장고를 설치
3. `django-admin startprject <project_name>` 명령어를 통해 장고 프로젝트 생성
   - 여기서 project_name을 config로 하는 방법을 추천한다. 이후 생성된 config 폴더 안에 있는 config폴더를 프로젝트 root로 꺼내주고 빈 config 폴더는 지워준다
4. 생성된 mange.py 파일을 통해 기초적인 설정을 해준다
   - python 버전 맞추기
   - flake8 적용
     - runtime언어인 python을 위해 실행 전 코드의 에러 부분을 감지해주기 위해 미리 컴파일 해주고 python pep(파이썬 문법)을 지킬수 있도록 해주는 Linter
   - black 적용
     - 코드를 파이썬에 맞는 Formmat을 자동으로 적용시켜서 변경해주는 formmater
5. settings.py 파일을 수정해서 프로젝트에 맞는 설정을 진행
   - TIME_ZONE 등등..
   - 여기서 passeord validation 등의 기본 설정을 해준다
6. `python manage.py runserver` 장고 서버를 실행

   - 이때 먼저 admin계정을 활성화해준다
     - `python manage.py migrate`를 통해 활성화하고 `python manage.py createsuperuser` 를 통해 관리자 계정을 생성
   - ~ipAddress~/admin 을 통해 관리자 계정으로 접근 가능

   > ### migrate란?
   >
   > migrate를 하기전에는 장고에서 admin 계정에 접근해도 django_session테이블이 존재하지 않는다고 에러가 발생한다, 이는 db와 장고가 연동이 되어있지 않다는 것으로 프로젝트와 DB간에 admin, auth, contenttypes, sessions에 대해서 연동이 필요하다는 것을 의미한다
   >
   > 데이터베이스의 경우에서 마이그레이션은 하나의 상태에서 다른 상태로, 다른 데이터 유형으로 바꾸는 것으로 이런 데이터 유형이 변경 될때 마다 migration이 필요하다

   **`python manage.py migrate` 명령어의 일련의 과정**

   - models에 뭔가를 변경하면 → 일부 데이터의 유형을 변경하게 되고 → migration을 생성하고 → 이를 Django에서 해당 migration을 적용해서 (데이터를)migrate한다 → 이로인해 DataBase가 변경된 Data가 Update가 되고 → 결과적으로 Django - DB가 동기화된다
   - 처음에는 장고에 기본적으로 admin, auth, contenttypes, sessions의 데이터 유형이 존재하므로 해당 내용을 비어있는 DB에 업데이트 해주는 것이다
   - 후에는 데이터를 변경한 후에 python manage.py makemigrations를 통해 migrations 폴더를 만들고 migrate를 진행

7. 프로젝트 시작전에 설계하기
   - 프로젝트는 애플리케이션의 집합이고 애플리케이션은 Group of function이다
   - 모든 애플리케이션을 Divide and Conquer 방식으로 독립적으로 구성해야한다. Room, User, Reservation, Review 등등 모든 애플리케이션을 따로 찢고 해당 애플리케이션의 함수를 생성하도록하자. room의 경우 room 검색, room 생성, room 삭제, room 업데이트, room 보기 등 기본적으로 CRUD를 기반으로 생각하고 추가적인 function을 갖도록 하자
   - **애플리케이션을 생성할지 말지에 대한 선택이 중요**하고, **애플리케이션은 한 문장으로 표현할 수 있어야한다**
     - 예를 들어 User Application에서의 기능은 ? → 유저 로그인, 로그아웃, 회원가입, 비번변경 ~~**AND 메시지 보내기**~~ 여기서 AND로 이어지지 않고 유저의 OO 기능으로 끝나야한다
     - AND로 이어진다면 이는 새로운 애플리케이션을 생성해야한다 → 메시지 보내기, 지우기, 보여주기, 전부 보여주기
8. 프로젝트 시작

---

장고에 기본적으로 django-admin startapp OOO을 입력하면 기본양식으로 애플리케이션을 생성해준다. 앞으로 필요한 모든 애플리케이션은 해당 명령어를 통해서 생성해준다

> 장고 프레임워크에 맞춰서 설계하는 것이므로 주어진 양식에 따라서 작성해줘야 한다. 따라서 파일을 변경하거나 지우면 안된다. (라이브러리는 내 코드가 해당 함수를 호출 - 도구 vs 프레임워크는 프로그램에서 내 코드를 호출 - 제공되는 틀)

### [USERS APPLICATION]

**models.OOField**

- 해당 필드값을 통해서 원하는 값을 받을 수 있다
- ImageField, CharField, TextField, BooleanField, DateField ...
- ImageFiled를 사용하기 위해서는 Pilow를 설치해줘야 한다 `pipenv install pillow`
- models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True) 등으로 설정을 해줄수 있다
  - null은 데이터베이스 상 null로 채우는 것이며 장고에서는 blank로 해줘야하므로 두개를 같이 해줘야한다 (null, blank)
  - CharFiled는 **Choices**를 가질수 있다 → GENDER_CHOICES ( (key, "value"), (key, "value"), .. )
- 참고 : [https://docs.djangoproject.com/en/2.2/ref/forms/fields/](https://docs.djangoproject.com/en/2.2/ref/forms/fields/)

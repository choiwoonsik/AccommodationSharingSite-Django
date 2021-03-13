# Accommodation Sharing Web App

# **Accommodation Sharing Site**

### **[DESCRIPTION]**

- WebPage of sharing accommodation by any people
- 숙박 공유 사이트 제작 개인 프로젝트

---

### **[사용한 언어 및 기술]**

- Python, Django, HTML, CSS
- back-end : Django
- front-end : Django 템플릿 시스템으로 구성
  - React를 사용하지 않은 이유
    - 상호작용이 많은 경우가 아니면 굳이 사용할 필요가없다
    - 콘텐츠 위주의 사이트 이므로 React를 굳이 선택할 필요가 없다
    - Django 템플릿으로도 반응형 웹사이트를 충분히 만들수 있다
- 모든 작업은 Pipenv 가상환경위에서 진행되었다 (Pipenv shell)

---

### **[기초 설정]**

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
   - ipAddress/admin 을 통해 관리자 계정으로 접근 가능

   > migrate란?

   migrate를 하기전에는 장고에서 admin 계정에 접근해도 django_session테이블이 존재하지 않는다고 에러가 발생한다, 이는 db와 장고가 연동이 되어있지 않다는 것으로 프로젝트와 DB간에 admin, auth, contenttypes, sessions에 대해서 연동이 필요하다는 것을 의미한다

   데이터베이스의 경우에서 마이그레이션은 하나의 상태에서 다른 상태로, 다른 데이터 유형으로 바꾸는 것으로 이런 데이터 유형이 변경 될때 마다 migration이 필요하다

   `**python manage.py migrate` 명령어의 일련의 과정\*\*

   - models에 뭔가를 변경하면 → 일부 데이터의 유형을 변경하게 되고 → migration을 생성하고 → 이를 Django에서 해당 migration을 적용해서 (데이터를)migrate한다 → 이로인해 DataBase가 변경된 Data가 Update가 되고 → 결과적으로 Django - DB가 동기화된다
   - 처음에는 장고에 기본적으로 admin, auth, contenttypes, sessions의 데이터 유형이 존재하므로 해당 내용을 비어있는 DB에 업데이트 해주는 것이다
   - 후에는 데이터를 변경한 후에 python manage.py makemigrations를 통해 migrations 폴더를 만들고 migrate를 진행

7. 프로젝트 시작전에 설계하기
   - 프로젝트는 애플리케이션의 집합이고 애플리케이션은 Group of function이다
   - 모든 애플리케이션을 Divide and Conquer 방식으로 독립적으로 구성해야한다. Room, User, Reservation, Review 등등 모든 애플리케이션을 따로 찢고 해당 애플리케이션의 함수를 생성하도록하자. room의 경우 room 검색, room 생성, room 삭제, room 업데이트, room 보기 등 기본적으로 CRUD를 기반으로 생각하고 추가적인 function을 갖도록 하자
   - **애플리케이션을 생성할지 말지에 대한 선택이 중요**하고, **애플리케이션은 한 문장으로 표현할 수 있어야한다**
     - 예를 들어 User Application에서의 기능은 ? → 유저 로그인, 로그아웃, 회원가입, 비번변경 **AND 메시지 보내기** 여기서 AND로 이어지지 않고 유저의 OO 기능으로 끝나야한다
     - AND로 이어진다면 이는 새로운 애플리케이션을 생성해야한다 → 메시지 보내기, 지우기, 보여주기, 전부 보여주기
8. 프로젝트 시작

# [완성된 사이트 모습]

- ...

# [사이트 구현 내용]

장고에 기본적으로 django-admin startapp OOO을 입력하면 기본양식으로 애플리케이션을 생성해준다. 앞으로 필요한 모든 애플리케이션은 해당 명령어를 통해서 생성해준다

> 장고 프레임워크에 맞춰서 설계하는 것이므로 주어진 양식에 따라서 작성해줘야 한다. 따라서 파일을 변경하거나 지우면 안된다. (라이브러리는 내 코드가 해당 함수를 호출 - 도구 vs 프레임워크는 프로그램에서 내 코드를 호출 - 제공되는 틀)

## [USERS APPLICATION]

유저(고객) 객체를 관리

### **Models.py**

**models.OOField**

- 해당 필드값을 통해서 원하는 값을 받을 수 있다
- ImageField, CharField, TextField, BooleanField, DateField, EmailField ...
- ImageFiled를 사용하기 위해서는 Pilow를 설치해줘야 한다 `pipenv install pillow`
- models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True) 등으로 설정을 해줄수 있다
  - null은 데이터베이스 상 null로 채우는 것이며 장고에서는 blank로 해줘야하므로 두개를 같이 해줘야한다 (null, blank)
  - CharFiled는 **Choices**를 가질수 있다 → GENDER_CHOICES ( (key, "value"), (key, "value"), .. )
- model에 작성한 값들을 장고가 알아서 ORM(Object Relation Mapping)을 통해 데이터베이스에 연동시켜 준다
- 참고 : [https://docs.djangoproject.com/en/2.2/ref/forms/fields/](https://docs.djangoproject.com/en/2.2/ref/forms/fields/)

### **Admin.py**

**@admin.register(models.User)**

- == admin.site.register(models.User, _CustomerUserAdmin_) , 여기서 *CustomerUserAdmin*은 @admin 바로 아래에 붙은 클래스 명
- admin패널을 컨트롤하는 곳이 Admin.py이다, 선언한 model을 사용하기 위해서는 Admin에 register 필요 (클래스에 register, 등록할 클래스 위에 decorator 선언)

**list_display**

- User의 리스트의 보여주는 형태를 변경하기 위해 사용
- 리스트에서 보여줄 특성값들을 고른다

  ```python
  list_display = ("username", ... )
  ```

**list_filter**

- 객체(유저)리스트에 대해서 특성값에 대해 filter를 적용하여 볼수 있다

  ```python
  list_filter = ('preference', ... )
  ```

**search_fields**

- 특성값에 대한 검색을 가능하게 한다
- 특정 class인스턴스의 프로퍼티로 접근하기 위해서는 `__`로 이어가면 접근할수 있다

  ```python
  search_fields = ["city", "host__username"]
  // User객체인 host의 프로퍼티임 username에 접근
  ```

**fieldsets**

- 리스트 내의 유저 내부의 값을 보여줄때 사용
- fieldsets를 이용해서 admin에서 보여주고자 하는 값을 조절할 수 있다
- UserAdmin.fieldsets은 장고에 내장되어있는 UserAdmin의 필드값들을 갖고있으므로 [UserAdmin.fieldsets + models]를 통해 생성한 필드값들을 추가함으로서 기존 값 + 새로운 값을 갖는 admin창을 만들 수 있다

  ```python
  from django.contrib.auth.admin import UserAdmin

  fieldsets = UserAdmin.fieldsets + (
          (
              "custom profile",
              {
                  # 간략히 보여주기가 가능해진다**
                  "classes": ("collapse",),
                  "fields": (
                      "avatar",
                      "gender",
                      "currency",
  											...
                  )
              },
          ),
      )
  ```

**ordering = ("price",)**

- list_display 항목중 골라서 기본세팅으로 정렬값을 줄 수 있다

**filter_horizontal**

- ManyToManyField()의 값을 갖는 값에 대해서 여러개를 가지게 되면 보기 힘드므로 보기 쉽게 만들어주는 형식

  ```java
  filter_horizontal = (
          "amenities",
          "facilities",
          "house_rules",
      )
  ```

## [ROOMS APPLICATION]

방 객체를 관리

### **core - models.py**

- 방의 생성 및 업데이트를 확인하기 위한 애플리케이션을 따로 생성 → django startapp "core"
- DB에 연동시키지 않기 위해서는 class Meta를 선언 후 abstract = True 설정을 넣어줘야한다

  ```python
  class Meta:
          abstract = True
  ```

- DateField(auto_now=False, auto_now_add=False)
  - auto_now : save 할때마다 date와 time을 저장
  - auto_now_add : create할 때마다 date와 time을 저장

### **models.py**

- host = models.ForeignKey(**"user_models.User"**, on_delete=models.CASCADE)
  - ForeinKey()를 이용해서 현재 model에 다른 애플리케이션의 model을 가져올 수 있다 → User 모델 취함
  - 일대다 관계, 하나의 유저 - 복수의 Room
  - on_delete
    - CASCADE: 종속, User가 삭제되면 같이 삭제된다 (폭포수 효과)
    - PROTECTED : 보호, Room을 갖는 유저가 존재한다면 해당 User는 지워질수 없다
- room_type = models.ManyToManyField(**"RoomType"**, blank=True)
  - 다대다 관계일 경우 ManyToMantyField()를 사용
  - AbstractItem을 갖는 RoomType, room_type은 복수의 RoomType값을 가질수 있다
  - 키값으로 삼을 타 클래스를 찾을 때 클래스 명을 String으로 하면 선언 위치에 상관없이 부를수 있다. 그렇지 않으면 호출이 선언 다음에 와야만 가능하다

### **Meta class**

- Meta class를 선언해서 사용
- verbose_name_plural("<name>") : 장고에서 자동으로 s를 붙여주는데 ies를 확인해주지 못하므로 원하는 단어로 설정
- verbose_name("<name>") : s는 그대로 붙이는데 설정한 이름을 갖게한뒤 붙임

[REVIEWS, RESERVATION, LIST, CONVERSATION APPLICATION]

생략

---

## [QuerySet]

**ForeignKey**

- User의 모델에는 Room객체를 따로 설정해주지 않았지만 python으로 db를 확인해보면 user객체는 room객체를 갖고있는것을 알수 있다. 이는 Room객체의 host변수에서 ForeignKey로 User를 갖기 때문이다.

  즉 Room은 하나의 유저를, 유저는 여러개의 방을 갖는 다대일 구조를 갖게된다

- A 객체가 B 객체를 ForeignKey로 갖게되면 B 객체의 개체(element) 또한 **???\_set**의 구조로 그 객체를 갖게 된다, 그러면 B객체의 element는 모든 A객체의 element에 접근할수 있다

  ```python
  #python manage.py sehll
  >>> user_obj = User.objects.get(username="woonsik")
  >>> print(user_obj)
  woonsik
  >>> user_obj.**room_set**
  <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x7fd419077100>
  >>> user_obj.room_set.all()
  <QuerySet [<Room: woonsikRoom>]>
  >>> dnstlr.review_set.all()
  <QuerySet [<Review: 뿌뿌이롱 - woonsikRoom>]>
  ```

- 여기서 set은 장고가 대신 만들어준것이다

**related_name**

- 어떤 값에 대해 ForeignKey를 설정할 때, 외부키로 설정된 객체가 외부키를 갖는 객체에 접근하는 이름을 변경할 수 있다 (default값은 **OOO_set**)

  ```python
  host = models.ForeignKey("users.User", **related_name="rooms"**, on_delete=models.CASCADE)
  ```

  ```python
  >>> dnstlr.rooms.all()
  <QuerySet [<Room: woonsikRoom>]>

  #room_set이아닌 rooms로 접근하는 모습
  ```

- related_name은 대상을 위한 이름으로 설정한다. host.rooms.all()을 통해 host의 모든 방을 보게 되는 방식

**ManyToManyField()**

- QuerySet으로 값을 갖는다

  ```python
  amenities = models.**ManyToManyField**("Amenity", blank=True)
  # Room 객체가 복수의 Amenity 객체를 가질수있게 된다
  ```

  ```python
  >>> room.review_set.all() # Room객체가 다대다 구조로 갖는 review 클래스, Amenity 클래스
  <QuerySet [<Review: 뿌뿌이롱 - woonsikRoom>]>
  >>> room.amenities.all()
  <QuerySet [<Amenity: 소파>, <Amenity: 침대>]>
  >>> room.amenities.count()
  2
  ```

> QuerySet은 리스트이고 object는 ManyToMany, ForeignKey를 갖는다

---

### [MODELS, ADMIN FUNCTION]

Admin패널 뿐만 아니라 Models.py에도 function을 넣을수 있다. 이는 보통 다른 models에서도 재사용하고자 하는 함수는 models에 작성하며, 특정 앱의 admin에서만 사용하고자하는 함수의 경우 admin패널에 작성하게 된다

**admin.py**

- admin패널에 함수를 작성하게 되는 경우

```python
# self = RoomAdmin, obj = row
    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "function"

    def count_photos(self, obj):
        return obj.photos.count()
```

위와 같은 경우에는 함수의 self로는 admin 자체가 들어가고, obj로는 admin의 row가 들어가게 된다. 따라서 row를 이루는 개체 (여기서는 room)의 amenities의 count()를 반환하게 된다

- FUNC_NAME.short_description을 통해 admin패널에 나오는 함수의 이름을 변경할수 있다
- list_display에 함수명을 추가해서 함수의 반환값을 출력하도록 할수 있다

**models.py**

- models.py에 함수를 작성하게 되는 경우

```python
# room Ojbect
def total_rating(self):
  all_reviews = self.reviews.all()
  all_rating = 0
  length = 1
  for review in all_reviews:
      all_rating += **review.rating_average()**
  if all_rating is 0:
      return 0
  else:
      length = len(all_reviews)
      return round(all_rating / length, 2)
```

매개변수로 self하나만 들어오며, self는 앱의 모델객체 자체이다. 현재 room객체이므로 room객체의 모든 reviews를 가져와서 **각 review들의 review_average()함수를 통해 리뷰의 평점**을 가져오고, 해당 평점들을 모두 더해서 방의 리뷰 평점 평균을 구하게 된다. 즉 models.py에 담긴 함수는 외부 앱에서도 접근이 가능하다

- admin 함수와 마찬가지로 list_display에 함수명을 추가하면 admin패널의 상태를 추가할수 있다

---

## **[photos]**

config의 settings.py에 다음을 추가

```python
~
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
# 위 내용을 추가함으로서 local폴더명은 uploads지만 이를 media라는 이름으로 접근하게 된다

MEDIA_URL = "/media/"
# '/'를 앞에 추가함으로서 root에서 바로 media로 접근하게 된다
# -> http://127.0.0.1:8000/media/room_photos/???.jpg
```

결과적으로 장고에게 파일이 저장되는 폴더명을 MEDIA_ROOT를 통해 알려주고, MEDIA_URL을 통해 접근할 수 있도록한다

Room의 models.py에 Photo클래스

```python
file = models.ImageField(upload_to="room_photos")
```

위 코드를 통해 들어오는 file을 room_photos폴더에 넣게되는데, 해당 디렉토리는 media/room_photos가 되고 media는 root디렉토리 바로 다음에 연결되도록 했으므로 root/media/room_photos에 해당 파일이 저장되게 된다

이후 config.urls 작성 - static을 이용하여 디렉토리와 url연결

```python
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    # static을 이용해서 settgins.MEDIA_URL과 실제 사진이 저장된 폴더를 연결시켜 주었다
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

DEBUG모드시에만 media폴더 디렉토리와 url을 연결시켜줌으로서 root/media/room_photos에 접근하면 MEDIA_ROOT인 `절대경로 BASE_DIR + "/uploads"`로 접근하게 해준다

DEBUG모드시에만 접근하도록 하는 이유는 배포시에는 아마존 s3등을 이용해서 DB를 사용하는데 이때 운용되는 서버마다 사진을 보관하게 하면 너무많은 용량을 차지하게 되므로 이때는 다른 방법을 사용한다. 현재 개발모드중에만 테스트를 위해 로컬에 보관하는 방식으로 진행한다

### [PhotoAdmin]

models를 통해 받은 사진을 admin패널에 표시해보자

file은 많은 값을 갖고있는데 이 중에서 obj.file.url을 통해 해당 파일의 url에 접근할 수 있다. 따라서 html 코드를 통해 해당 이미지를 출력하면된다

이때, 장고는 보안상의 이유로 html을 바로 받아서 열지 않고 문자열로 처리해버리는데 이를 위해 장고에게 mark_safe 표시를 해줘야 html링크가 자동으로 열리게 된다

```python
return **mark_safe**(f"<img width=40px src = {obj.file.url}/>")
```

---

### [InlineModelAdmin]

admin안에 admin을 넣는 방법

- admin.TabularInline
- admin.StackedInline

두가지가 존재하며 보여주는 방식에서 차이가 있다

특정 클래스의 admin이 이미 존재할 때, 해당 admin을 다른 클래스의 admin에 넣고 싶을 때 사용할수 있다

```python
class PhotoInline(admin.TabularInline):

    model = models.Photo

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = (PhotoInline,) # RoomAdmin에 photoAdmin을 인라인으로 넣은 것

		~
```

---

### [save() method]

models의 save()메소드를 오버라이딩을 통해 원하는 이벤트를 추가할수 있다

```python
def save(self, *args, **kwargs):
        do_something()
				# Call the "real" save() method.
				self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)
				do_something_else()
```

save()를 호출하게 되면 먼저 self.city의 첫글자만 대문자로 변경하고 나머지를 소문자로 한뒤 super()의 save()를 다시 호출해서 real save()를 진행해준다

단, 위의 save()의 경우 models.py에 작성되며 admin, view등 모든 저장에서 불려지게 된다. 따라서 admin에서의 저장이 발생했을 때만 save()를 변경해서 적용하고자 하면 따로 해야한다

**admin에서의 save()**

```python
def save_model(self, request, obj, form, change):
	print(obj, request, obj, change)
	super().save_model(request, obj, form, change)
```

admin에서의 save가 일어나면 save_model이 불리고 원하는 작업을 실행하고 이후 super().save_model이 실행되는데 이때, 위의 models의 save()가 불려지게 된다

---

## [Django-seed]

서버 테스트를 위한 fake-data 생성

- User, Room, Facility, Amenity, City, 등등 모든 개체에 대한 데이터를 생성해서 넣어주자

**세팅**

원하는 애플리케이션에 가서 management 폴더 생성 → [init.py](http://init.py) 생성 후 coomands 폴더 생성 → commands 폴더에도 init.py 생성 후 작업을 위한 파일 생성 (seed_amenities.py)

**BaseCommand**

반복적인 작업을 위한 BaseCommand를 사용

- 예시

  ```python
  class Command(BaseCommand):
      help = "this command tells me how can use this"

      def add_arguments(self, parser):
          parser.add_argument(
              "--times",
              help=("Input the count of repeatedly do handle"),
          )

      def handle(self, *args, **options):
          """
          The actual logic of the command. Subclasses must implement
          this method.
          """
          times = options.get("times")
          for t in range(0, int(times)):
  						## 아래 내용을 통해 초록색 or 빨간색 or 주황색등으로 출력할수 있다
              **self.stdout.write(self.style.SUCCESS("I love you"))**
  ```

  ```python
  python manage.py <"seed파일명"> --help
  >
  usage: manage.py loveyou [-h] [--times TIMES] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--force-color]

  this command tells me hello love me

  optional arguments:
    -h, --help            show this help message and exit
    --times TIMES         Input the count of repeatedly do handle
  	~
  ```

Room의 Amenity를 만들기 위해 활용 - handle함수 수정

```python
def handle(self, *args, **options):
	amenities = [내용물 ...]
	for amenity in amenities:
	            room_models.Amenity.objects.create(name=amenity)
	        self.stdout.write(self.style.SUCCESS("Amenities Created !"))
```

django-seed를 설치해서 User 객체 생성

```python
from django_seed import Seed

def add_arguments(self, parser):

  parser.add_argument(
      "--number", default=1, help="how many users do you want to create?"
  )

def handle(self, *args, **options):

  number = options.get("number")
  **seeder = Seed.seeder()**
  **seeder.add_entity(
      user_models.User, int(number), {"is_staff": False, "is_superuser": False}
  )**
  **seeder.execute()**
  self.stdout.write(self.style.SUCCESS(f"user {number} is Created !"))
```

→ `python manage.py seed_users --number 50`

위 명령을 통해 50개의 유저를 생성할 수 있다. 알아서 OOOField()에 적합한 데이터가 생성되어서 들어간다

foreignKey를 랜덤으로 넣어서 생성하는 경우

```python
def handle(self, *args, **options):

        number = options.get("number")
        seeder = Seed.seeder()

        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()

        seeder.add_entity(
            room_models.Room,
            int(number),
            {
                "city": lambda x: seeder.faker.city(),
                "address": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(0, 1000),
                "guests": lambda x: random.randint(1, 5),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()
```

random의 choice를 이용해서 객체중에서 하나를 고르게한다. 단 실제 배포모드에서는 all()로 모든 객체를 부르지않고 개수를 제한해서 불러야한다. (왜? 만약 수천개의 user가 있다면 너무 많으므로)

---

## [VIEWS]

사용자는 url을 요청하고 그에 맞는 응답으로 view를 제공한다. room의 사진들을 요청했다면 room의 사진들을 view를 통해 제공한다. 이때, view를 함수로 제공한다

필요한 url이 요청될 때마다 그에 맞는 view를 제공해야하므로 url을 그에 맞는 애플리케이션끼리 나눠서 갖게해준다. room에 관련된 url의 경우 rooms의 url.py에 작성하게 된다

→ url에 대한 요청으로 http응답메시지를 보내야한다. 이때 응답메시지에는 내용으로 HTML이 포함될수 있다. 이를 이용해서 요청 url에 맞는 화면을 보여준다

**template & render**

또한, 모든 요청에 대해 http메시지를 보내지 않기위해 template를 사용한다. Django는 **render()**를 이용해서 요청에 대해 작성한 html과 미리 설정한 context변수를 확인해서 HTTP메시지로 보내게 된다

render() : Return a HttpResponse whose content is filled with the result of calling django.template.loader.render_to_string() with the passed arguments.

```python
def all_rooms(request):
  now = datetime.now()
  hungry = True
  return **render**(request, "all_rooms.html", context={"now": now, "hungry": hungry})
```

**html 파일**

request의 응답으로 render를 이용해서 특정 html파일을 보내게된다. 이때 html파일에서는 render에서 선언한 변수(context)를 사용할수 있다

사용방법으로는 `{{ 변수 }}`와 파이썬 코드를 위한 `{% code %}`가 있다

```java
**all_rooms.html 예시**

<h1>Hello! nice to meet you</h1>

<h4>The time right now is : {{now}}</h4>

<h5>{% if hungry %} I'm hungry {% else %} I'm okay {% endif %}</h5>
```

### [PAGE]

Room 페이지별로 특정 개수의 방만 보여주고 특정 페이지로 갈수 있도록 구현

**3가지 방법이 존재**

- Django를 사용하지 않고 **순수 파이썬을 이용**해서 구현하는 경우
- Django의 **Pagination**을 이용해서 구현하는 경우
- **list view** (class based view)를 이용해서 구현하는 경우

1. Rooms views.py - 파이썬을 이용해서 구현하는 경우

```java
def all_rooms(request):
		//request -> ip~/?page=1 에서 page는 key, 1은 value
    page = request.GET.get("page", 1) //key값으로 page를 넣고 반환값을 받는다
		page = int(page or 1) // page값이 있으면 int로 받고 없으면 1
		page_size = 10
    limit = page * page_size
    offset = limit - page_size
    page_count = ceil(models.Room.objects.count() / page_size)
    all_rooms = models.Room.objects.all()[offset:limit]
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count + 1),
        },
    )
```

- home.html - 수동적으로 파이썬으로 만드는 경우

```html
<h5>
    {% if page is not 1 %}
    <a href="?page={{page|add:-1}}">Previous</a>
    {% endif %}
    Page {{page}} of {{page_count}}
    {% if page is not page_count %}
    <a href="?page={{page|add:1}}">Next</a>
    {% endif %}
  </h5>
```

2. Room views.py - Django를 사용하여 만드는 경우, **Paginator 사용**

```python
def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, **orphans=5**) 
    rooms = paginator.get_page(page)  # querySet을 반환, rooms는 object_list를 갖고있다
    return render(request, "rooms/home.html", {"rooms": rooms})

# **orphans**가 5이하라면 마지막 이전 페이지에 합쳐서 보여주게된다
```

- home.html - Paginator를 이용해서 구현한 경우

```python
{% block content %} 

  {% for room in rooms.object_list %}
    <h3>{{room.name}} </h3>
    <h4>주소 : {{room.address}}, 가격 : {{room.price}}</h4>
  {% endfor %} 

<h5>
    {% if page.has_previous %}
    <a href="?page={{page.previous_page_number}}">Previous</a>
    {% endif %}
    
    Page {{page.number}} of {{page.paginator.num_pages}}

    {% if page.has_next %}
    <a href="?page={{page.next_page_number}}">Next</a>
    {% endif %}
  </h5>

{% endblock content %}
```

3. Rooms views.py - list view(**class based view**)를 사용하여 구현하는 경우

listview의 메소드 및 Attributes 참고 사이트
[https://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/)

Homeview는 클래스로 ListView를 상속받는다. ListView의 활용은 위의 사이트를 통해 참고하도록하자. 지금까지는 function based view로 함수를 이용하여 구현하였지만 listview는 class based view이다.

```python
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    ordering = "name"
    paginate_orphans = 5
    page_kwarg = "page"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context
```

- room_list.html

```python
# listview를 사용하게 됨으로서 html의 이름 또한 view의 규칙을 따른다. 
# 사용하는 models의 클래스 명_list.html 의 파일을 가져야한다
# 나머지 내용은 이전 파일 그대로 사용하면 된다3
# (obj_list는 page_obj로 받아야한다, 현재는 rooms로 이름을 변경)
```

---

### [애플리케이션 VIEW page 구성]

각 애플리케이션 폴더에서 urls.py파일과 views.py파일을 이용하여 서비스별 페이지를 로드하도록 할수 있다.

예) rooms에서 방 리스트를 보여주고, 각 방을 클릭하면 그 방의 페이지를 로드하는 방식 등

config폴더에서 애플리케이션 urls로 보내주고, 각 앱의 urls.py에서 더 자세하게 들어갈 수 있도록 처리한다. 이때, 앱의 views.py에서 보여줄 화면을 구성하고 html파일들은 templates폴더에서 모두 관리하도록 한다

- config - urls.py

```python
urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    # static을 이용해서 settgins.MEDIA_URL과 실제 사진이 저장된 폴더를 연결시켜 주었다
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- rooms - urls.py

```python
from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]
```

- rooms - views.py

```python
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    ordering = "name"
    paginate_orphans = 5
    page_kwarg = "page"
    context_object_name = "rooms"

def room_detail(request, pk):

    print(pk)

    return render(request, "rooms/detail.html")
```

위에서 아래로 점점 파고드는 구조로 되어있다. 구조를 잘 이해하도록 하자. 다른 앱들도 이런 형태로 짜게 된다

### [애플리케이션 DetailView]

함수형 detail_view 구성

```python
//views.py
def room_detail(request, pk):

    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
```

- 잘못된 접근은 Http404()메서드를 사용해서 처리해야한다
- render로 변수값을 전달해줘야 html에서 값을 사용할 수 있다

클래스view 구성

```python
//views.py
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room
```

- 잘못된 접근도 404로 알아서 처리해준다
- model로 객체를 주면 알아서 소문자로 처리하여서 html 값으로 전달해준다
- DetailView는 자동으로 개체의 `pk`값을 기준으로 객체를 탐색해준다. 그러고 그 값을 url요청때 전달한다

```python
// urls.py 
urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]
```

### [애플리케이션 form]

search 기능구현을 위해 form을 사용해본다

- views.py

```python
def search(requset):
    city = requset.GET.get("city")
    print(str.capitalize(city))
    return render(requset, "rooms/search.html", context={"city": city})
```

- header.html - 헤더에 입력을위한 form생성, 입력값은 city명으로 받음

```java
<form method="get" action="{% url "rooms:search" %}">
    <input name="**city**" placeholder="Search by City"/>
</form>
```

- search.html

```html
{%  extends "base.html" %}

{% block page_title %}
    Search
{% endblock %}

{% block content %}
    <h2>Search!</h2>

    <h4>Searching by {{ **city** }}</h4>
{% endblock %}
```

- views.py - filter부분

```java

filter_args = {}

if city != "Anywhere":
    filter_args["city__startswith"] = city

filter_args["country"] = country

if room_type != 0:
    filter_args["room_type__pk"] = room_type

if price != 0:
    filter_args["price__lte"] = price

if len(s_amenities) > 0:
      for s_amenity in s_amenities:
          filter_args["amenities__pk"] = int(s_amenity)

if len(s_facilities) > 0:
    for s_facility in s_facilities:
        filter_args["facilities__pk"] = int(s_facility)

rooms = models.Room.objects.filter(**filter_args)

return render(request, "rooms/search.html", context={
    **form, **choices, "rooms": rooms,
})
```

위와 같이 filter를 설정할 수 있다

### Django를 이용하여 Form API 사용하기

search.html

```java
% block content %}
    <h2>Search!</h2>
    <form method="get" action="{% url "rooms:search" %}">
        **{{ form.as_p }}**
        <button>Search</button>
    </form>

    <h3>Results</h3>

    {% for room in rooms %}
        <h3>{{ room.name }}</h3>
    {% endfor %}

{% endblock %}
```

views.py

```java
def search(request):

    form = forms.SearchForm(request.GET)

    return render(request, "rooms/search.html", {"form": form})
```

- request.GET을 forms.SearchForm의 매개변수로 넣게 되면 골랐던, 입력했던 모든 값들을 기억해서 유지시켜준다

forms.py ← 새로 생성한 파일, Form API를 사용하기위해 생성

```java
class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
```
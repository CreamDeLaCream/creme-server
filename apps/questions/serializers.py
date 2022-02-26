from rest_framework import serializers

from .models import Question, QuestionChoice

"""
NOTE:

- 질문 리스트와 선택지를 같이 보여줌
ex:)
{
    id: "질문 번호",
    question: "질문 내용",
    choices: [
        {
            choice_index: 1,
            content: "선택지 1",
        },
        .......
        {
            choice_index: 4,
            content: "선택지 4",
        }
    ]
}

POST api/analysis/pet
# 참고: https://www.django-rest-framework.org/api-guide/parsers/#multipartparser

multipart-
{
    dog_name: "지노",
    dog_age: 7,
    image: binary,
}
이 시점에서 내부에서 이미지를 분석한 뒤 필드에 값을 채워 준다.
response: slug or analysis id

POST api/analysis/person
{
    slug: <slug>
    answer:[
        {
            question_id: <질문 ID>
            choice_index: <선택지 ID>
        },
        ........
        {
            question_id: <질문 ID>
            choice_index: <선택지 ID>
        }
    ]
}
response: success or failed

GET api/analysis/<slug>

"""


class QuestionChoiceSerializer(serializers.ModelSerializer):
    """질문 선택지"""

    class Meta:
        Model = QuestionChoice
        fields = (
            "choice_index",
            "content",
        )


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True)

    class Meta:
        Model = Question
        fields = (
            "question",
            "choices",
        )


# 질문갯수를 가변으로 처리하기 위해 ?
# 고정된 갯수가 아닌 4개 필드를 n개 생성 해줘야하니까 many to many 를 쓴 거 같다.. ! 아마도


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        Model = None

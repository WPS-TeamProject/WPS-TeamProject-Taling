from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Tutor
from regiclass.models import Lecture
from regiclass.serializers import LectureListSerializer, LectureMakeSerializer

MyUser = get_user_model()

__all__ = (
    'LectureMake',
    'LectureList',
    'LectureDetail',
    'LikeLecture',
)


class LectureMake(APIView):
    serializer_class = LectureMakeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        user = MyUser.objects.get(pk=request.user.id)
        if serializer.is_valid():
            try:
                tutor = get_object_or_404(Tutor, author=user)
            except Tutor.DoesNotExist:
                return Response({'result': '튜터가 아닌 사용자는 강의를 개설할 수 없습니다'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer.save(tutor=tutor)
            return Response({'result': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        return Response({'result': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class LectureList(APIView):
    serializer_class = LectureListSerializer

    def post(self, request):
        search_text = request.POST.get('search_text', '')
        order_by = request.POST.get('ordering', '-modify_date')
        category = request.POST.get('category', '')
        state = request.POST.get('state', Lecture.STATE_ACTIVITY)
        lecture_list = Lecture.objects.filter(
            (Q(title__contains=search_text) | Q(tutor__author__nickname__contains=search_text))
            | (Q(category__contains=category))
            & (Q(state=state))
        ).order_by(order_by)
        serializer = self.serializer_class(lecture_list, context={'user':request.user}, many=True)
        return Response(serializer.data)


class LectureDetail(APIView):
    serializer_class = LectureListSerializer

    def post(self, request):
        lecture_id = request.POST.get('lecture_id')
        try:
            lecture = get_object_or_404(Lecture, pk=lecture_id)
        except Lecture.DoesNotExist:
            return Response({'result': '해당하는 강의 정보가 없습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.serializer_class(lecture, context={'user':request.user})
        return Response(serializer.data)

    def patch(self, request):
        lecture_id = request.data['lecture_id']
        try:
            lecture = get_object_or_404(Lecture, pk=lecture_id)
        except Lecture.DoesNotExist:
            return Response({'result': '해당하는 강의 정보가 없습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.serializer_class(lecture, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class LikeLecture(APIView):
    def post(self, request):
        lecture_id = request.POST.get('lecture_id')
        lecture = get_object_or_404(Lecture, pk=lecture_id)
        like_lecture, like_created = lecture.likelecture_set.get_or_create(
            user=request.user
        )
        if not like_created:
            like_lecture.delete()
        return Response({'created': like_created}, status=status.HTTP_201_CREATED)

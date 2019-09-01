from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from quiz.models import MainUser, UserQuiz, Quiz, SubUser


def start(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        code = request.POST.get('code', '')
        url = "랜덤 생성"
        mainuser = MainUser.objects.create(username=username, code=code, url=url)
        return redirect('quiz:mainstart', mainuser.id)

    else :
        return render(request, 'quiz/start.html')
    return HttpResponse("start")

def mainstart(request, main_id):
    #퀴즈 생성중... 이런 화면 띄우기
    mainuser = MainUser.objects.get(id=main_id)
    #퀴즈 개수 이하에서 10개의 번호 랜덤 선택 -> 리스트:numlist
    numlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    quiz_num = 0
    for num in numlist:
        quiz_num += 1
        quiz = Quiz.objects.get(id=num)
        UserQuiz.objects.create(mainuser=mainuser, quiz=quiz, quiz_num=quiz_num)
    return redirect('quiz:mainquiz', main_id, 1)

def mainquiz(request, main_id, quiz_id):
    mainuser = MainUser.objects.get(id=main_id)
    mainquiz = UserQuiz.objects.get(quiz_num=quiz_id)

    if request.method == 'POST':
        if request.POST['answer'] == '1':
            mainquiz.answer = 1
            mainquiz.save()
        elif request.POST['answer'] == '2':
            mainquiz.answer = 2
            mainquiz.save()

        return redirect('quiz:mainquiz', main_id, quiz_id + 1)

    else :
        if quiz_id == 10 :
            return redirect('quiz:mainend', main_id)
        else :
            ctx = {'mainuser':mainuser, 'mainquiz':mainquiz}
            return render(request, 'quiz/mainquiz.html', ctx)

    return HttpResponse("mainquiz")

def mainend(request, main_id):
    mainuser = MainUser.objects.get(id=main_id)
    return render(request, 'quiz/mainend.html', {'mainuser':mainuser})

def substart(request, main_id):
    mainuser = MainUser.objects.get(id=main_id)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        subuser = SubUser.objects.create(mainuser=mainuser, username=username)
        return redirect('quiz:subquiz', main_id, subuser.id, 1)
    else :
        return render(request, 'quiz/substart.html', {'mainuser':mainuser})
    return HttpResponse("mainstart")

def subquiz(request, main_id, sub_id, quiz_id):
    mainuser = MainUser.objects.get(id=main_id)
    subuser = SubUser.objects.get(id=sub_id)
    mainquiz = UserQuiz.objects.get(quiz_num=quiz_id)

    if request.method == 'POST':
        if request['answer'] == mainquiz.answer :
            subuser.score += 1
            subuser.save()
            #잠깐동안 "맞았습니다" 표시 후 redirect 넘어감
        else :
            pass
            #잠깐동안 "틀렸습니다" 표시
        return redirect('quiz:subquiz', main_id, sub_id, quiz_id+1 )

    else :
        if quiz_id == 10 :
            return redirect('quiz:subend', main_id, sub_id)
        else :
            ctx = {'mainuser':mainuser, 'subuser':subuser, 'mainquiz':mainquiz}
            return render(request, 'quiz/subquiz.html', ctx)
    return HttpResponse("mainstart")

def subend(request, main_id, sub_id):
    mainuser = MainUser.objects.get(id=main_id)
    subuser = SubUser.objects.get(id=sub_id)
    subusers = SubUser.objects.filter(mainuser=mainuser).order_by('score')
    ctx = {'mainuser':mainuser, 'subuser':subuser, 'subusers':subusers}
    return render(request, 'quiz/subend.html', ctx)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse, Http404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from .forms import CustomUserCreationForm, ConversationForm, MentorConversationForm
from django.contrib.auth.models import Group
from .models import CustomUser, Conversation
from django.views.generic import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from .serializer import ConversationSerializer, MentorReplySerializer


def loginpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        obj = authenticate(request, username=email, password=password)
        if obj:
            login(request, obj)
            return redirect('home')
        else:
            return HttpResponse('Wrong credentials.....')
    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Adding Users to user role
            grp = Group.objects.get(name='UserRole')
            grp.user_set.add(user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    user = request.user
    userob = CustomUser.objects.get(email=user)
    data = Conversation.objects.filter(Q(sender=user) | Q(receipient=user)).order_by('-sent_at')
    if userob.is_mentor:
        return render(request, 'mentorhomepage.html', {'mentor': 'Mentor', 'data': data, 'token': userob.tokens()})
    return render(request, 'homepage.html', {'User': 'User', 'data': data, 'token': userob.tokens()})


class ConversationDetail(DetailView):
    model = Conversation
    template_name = 'conversation_detail.html'
    context_object_name = 'conversation'


class ConversationView(CreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Conversation.objects.all()

    def get(self, request):
        print(self.request.user)
        serializer = self.serializer_class(email=self.request.user.email, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return redirect('home')


class MentorReply(UpdateAPIView):
    serializer_class = MentorReplySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Conversation.objects.get(pk=pk)
        except Exception:
            raise Http404

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return redirect('home')

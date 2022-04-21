from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin


# def test(request):
# 	objects = [
# 		'john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6',
# 		'george7', 'ringo8', 'john9', 'paul10', 'george11', 'ringo12',
# 		'george13', 'ringo14', 'john15', 'paul16', 'george17', 'ringo18'
# 	]
# 	paginator = Paginator(objects, 5)
# 	page_num = request.GET.get('page', 1)
# 	page_objects = paginator.get_page(page_num)
# 	return render(request=request, template_name='news/contact.html', context={'page_obj': page_objects})


def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'musya.arina@yandex.ru', ['axmerov331@gmail.com'], fail_silently=True)
			if mail:
				messages.success(request, 'Письмо отправлено!')
				return redirect('contact')
			else:
				messages.error(request, 'Ошибка отправки сообщения')
		else:
			messages.error(request, 'Ошибка валидации')
	else:
		form = ContactForm()
	return render(request=request, template_name='news/contact.html', context={'form': form})


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Вы успешно зарегистрировались')
			return redirect('home')
		else:
			messages.error(request, 'Ошибка регистрации')
	else:
		form = UserRegisterForm()
	return render(request=request, template_name='news/register.html', context={'form': form})


def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)

			return redirect('home')
	else:
		form = UserLoginForm()
	return render(request=request, template_name='news/user_login.html', context={'form': form})


def user_logout(request):
	logout(request)
	return redirect('user_login')


class HomeNews(MyMixin, ListView):
	model = News
	template_name = 'news/home_news_list.html'
	context_object_name = 'news'
	mixin_prop = ''
	paginate_by = 3
	# extra_context = {'title': 'Главная'}

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.get_upper('Главная страница')
		context['mixin_prop'] = self.get_prop()
		return context

	def get_queryset(self):
		return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
	model = News
	template_name = 'news/home_news_list.html'
	context_object_name = 'news'
	allow_empty = False
	paginate_by = 3

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
		return context

	def get_queryset(self):
		return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
	model = News
	context_object_name = 'news_item'
	# template_name = 'news/news_detail.html'


class CreateNews(LoginRequiredMixin, CreateView):
	form_class = NewsForm
	template_name = 'news/add_news.html'
	# success_url = reverse_lazy('home')
	login_url = '/admin/'
	# raise_exception = True

# def index(request):
# 	news = News.objects.all()
#
# 	return render(
# 		request=request,
# 		template_name='news/index.html',
# 		context={
# 			'news': news,
# 			'title': 'Список новостей',
# 		}
# 	)


# def get_category(request, category_id):
# 	news = News.objects.filter(category_id=category_id)
# 	category = Category.objects.get(pk=category_id)
#
# 	return render(
# 		request=request,
# 		template_name='news/category.html',
# 		context={
# 			'news': news,
# 			'category': category
# 		}
# 	)
#
#
# def view_news(request, news_id):
# 	# news_item = News.objects.get(pk=news_id)
# 	news_item = get_object_or_404(News, pk=news_id)
# 	return render(
# 		request=request,
# 		template_name='news/view_news.html',
# 		context={
# 			'news_item': news_item
# 		}
# 	)


# def add_news(request):
# 	if request.method == 'POST':
# 		# связана с данными
# 		form = NewsForm(request.POST)
# 		if form.is_valid():
# 			# news = News.objects.create(**form.cleaned_data)
# 			news = form.save()
# 			return redirect(news)
# 	else:
# 		# не связана с данными
# 		form = NewsForm()
#
# 	return render(
# 		request=request,
# 		template_name='news/add_news.html',
# 		context={
# 			'form': form
# 		}
# 	)

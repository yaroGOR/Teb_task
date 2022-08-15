from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
	def create_user(self, tgname,tgid=None, username =None, password=None):
		if not tgname:
			raise ValueError('Users must have telegram name')
		
		user = self.model(
			tgname=tgname,
			tgid=tgid,
			username=username
		)

		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self, tgname,password):
		user = self.create_user(
			password=password,
			tgname=tgname,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	tgname = models.CharField(verbose_name="telegram name", max_length=60, unique=True)
	tgid=models.CharField(max_length=40, null=True, blank=True)
	username = models.CharField(max_length=30, null=True, blank=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)


	USERNAME_FIELD = 'tgname'
	#REQUIRED_FIELDS = []

	objects = MyAccountManager()

	def __str__(self):
		return self.tgname

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
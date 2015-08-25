# coding: utf-8
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group

from utils.tests.common_test_case import CommonTestCase

from sharing.models import Profile, Lending, Queue
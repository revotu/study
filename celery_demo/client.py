# -*- coding: utf-8 -*-

from celery_app import task1
from celery_app import task2

task1.add.delay(2, 8)		# 也可用 task1.add.apply_async(2, 8)
task2.multiply.delay(2, 8)	# 也可用 task2.multiply.apply_async(2, 8)

print 'hello world'

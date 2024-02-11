"""_summary_
初始化网站
    """

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Initializes the site with default data'

    def handle(self, *args, **options):
        # 创建一个超级用户
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', '123456ABCDEf')
            
        administrator, created  = Group.objects.get_or_create(name='administrator')
        teacher, created = Group.objects.get_or_create(name='teacher')
        student, created = Group.objects.get_or_create(name='student')

        user = User.objects.create_user(username='2022141520159', password='123456', email='3177267975@qq.com')
        user.first_name = '张三'
        user.save()
        administrator.user_set.add(user)
        
        user = User.objects.create_user(username='2022141520158', password='123456', email='3177267975@qq.com')
        user.first_name = '李四'
        user.save()
        teacher.user_set.add(user)
        
        user = User.objects.create_user(username='2022141520157', password='123456', email='3177267975@qq.com')
        user.first_name = '王五'
        user.save()
        student.user_set.add(user)
                
        self.stdout.write(self.style.SUCCESS('Successfully initialized the site'))

const routes = {
  routes: [
    {
      id: 16,
      parentId: 0,
      children: [
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_course',
          path: '/home/course',
          component: 'view.home_course',
          meta: {
            icon: 'carbon:course',
            order: 1,
            hideInMenu: false,
            roles: ['administrator', 'teacher', 'student'],
            title: 'My Courses'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_account',
          path: '/home/account',
          component: 'view.home_account',
          meta: {
            icon: 'carbon:course',
            order: 1,
            hideInMenu: false,
            roles: ['administrator'],
            title: 'Account'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_records',
          path: '/home/records',
          component: 'view.home_records',
          meta: {
            icon: 'carbon:course',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher'],
            title: 'Course Records'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_homework-records',
          path: '/home/homework-records',
          component: 'view.home_homework-records',
          meta: {
            icon: 'carbon:course',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher'],
            title: 'Homework Records'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_homework-records-detail',
          path: '/home/homework-records-detail',
          component: 'view.home_homework-records-detail',
          meta: {
            icon: 'carbon:course',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher'],
            title: 'Homework RecordDetail'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_homework',
          path: '/home/homework',
          component: 'view.home_homework',
          meta: {
            icon: 'material-symbols:home-work-outline',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher', 'student'],
            title: 'Homework List'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_problem-list',
          path: '/home/problem-list',
          component: 'view.home_problem-list',
          meta: {
            icon: 'material-symbols:home-work-outline',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher', 'student'],
            title: 'Problem List'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_problem-detail',
          path: '/home/problem-detail',
          component: 'view.home_problem-detail',
          meta: {
            icon: 'material-symbols:home-work-outline',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher', 'student'],
            title: 'Problem Detail'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_submission-detail',
          path: '/home/submission-detail',
          component: 'view.home_submission-detail',
          meta: {
            icon: 'material-symbols:home-work-outline',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher', 'student'],
            title: 'Submission Detail'
          }
        },
        {
          id: 17,
          parentId: 16,
          children: null,
          name: 'home_settings',
          path: '/home/settings',
          component: 'view.home_settings',
          meta: {
            title: "Settings",
            icon: 'ant-design:setting-outlined',
            order: 1,
            hideInMenu: true,
            roles: ['administrator', 'teacher', 'student']
          }
        }
      ],
      name: 'home',
      path: '/home',
      component: 'layout.base',
      meta: {
        icon: 'carbon:cloud-service-management',
        order: 5,
        hideInMenu: false,
        roles: ['administrator', 'teacher', 'student'],
        title: 'Home'
      }
    }
  ],
  home: '/wechat/home'
};

export default routes;

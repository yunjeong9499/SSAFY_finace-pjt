import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import SignUpView from '@/views/AccountView/SignUpView.vue'
import LogInView from '@/views/AccountView/LogInView.vue'
import UserProfileView from '@/views/AccountView/UserProfileView.vue'
import PasswordChangeView from '@/views/AccountView/PasswordChangeView.vue'
import EditProfileView from '@/views/AccountView/EditProfileView.vue'
import DepositListView from '@/views/ProductView/DepositListView.vue'
import SavingListView from '@/views/ProductView/SavingListView.vue'
import DepositDetailView from '@/views/ProductView/DepositDetailView.vue'
import SavingDetailView from '@/views/ProductView/SavingDetailView.vue'
import BranchesView from '@/views/support/BranchesView.vue'
import StocksView from '@/views/StocksView.vue'
// import StockChart from '@/components/StockChart.vue'
import CommunityListView from '@/views/CommunityView/CommunityListView.vue'
import CommunityCreateView from '@/views/CommunityView/CommunityCreateView.vue'
import CommunityDetailView from '@/views/CommunityView/CommunityDetailView.vue'
import CommunityEditView from '@/views/CommunityView/CommunityEditView.vue'
import Chatbot from '@/components/Chatbot.vue'
import ArticleListView from '@/views/ArticleView/ArticleListView.vue'
import ArticleDetailView from '@/views/ArticleView/ArticleDetailView.vue'
// import ArticleCreateView from '@/views/ArticleView/ArticleCreateView.vue'
// import ArticleEditView from '@/views/ArticleView/ArticleEditView.vue'
import ArticleEditorView from '../views/ArticleView/ArticleEditorView.vue'

import { useAccountStore } from '@/stores/accounts'
import ServiceDescripView from '@/views/support/ServiceDescripView.vue'
import ProductListView from '@/views/ProductView/ProductListView.vue'
// import StocksCalculatorView from '@/views/StocksCalculatorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: UserProfileView,
    },
    {
      path: '/change-password',
      name: 'changepassword',
      component: PasswordChangeView,
    },
    {
      path: '/profile/edit',
      name: 'profileEdit',
      component: EditProfileView,
    },
    {
      path: '/product',
      name: 'product-list',
      component: ProductListView,
    },
    {
      path: '/product/deposit',
      name: 'products_deposit',
      component: DepositListView,
    },
    {
      path: '/product/saving',
      name: 'products_saving',
      component: SavingListView,
    },
    {
      path: '/deposits/:id',
      name: 'deposit-detail',
      component: DepositDetailView,
      props: true,
    },
    {
      path: '/savings/:id',
      name: 'saving-detail',
      component: SavingDetailView,
      props: true,
    },
    {
      path: '/stocks',
      name: 'stocks',
      component: StocksView,
      // children: [{ path: ':name', name: 'stockChart', component: StockChart }],
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityListView,
    },
    {
      path: '/community/create',
      name: 'community-create',
      component: CommunityCreateView,
      meta: { requiresAuth: true },
    },
    {
      path: '/community/:id',
      name: 'community-detail',
      component: CommunityDetailView,
      props: true
    },
    {
      path: '/community/:id/edit',
      name: 'community-edit',
      component: CommunityEditView,
      props: true,
      meta: { requiresAuth: true },
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticleListView
    },
    {
      path: '/articles/create',
      name: 'articles-create',
      component: ArticleEditorView,
      meta: { requiresAuth: true },
    },
    {
      path: '/articles/:id',
      name: 'article-detail',
      component: ArticleDetailView,
      props: true,
    },
    {
      path: '/support/description',
      name: 'service-description',
      component: ServiceDescripView,
    },
    {
      path: '/support/branches',
      name: 'branches',
      component: BranchesView,
    },
    {
      path: '/chat-bot',
      name: 'chat-bot',
      component: Chatbot
    }
  ],
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !isLoggedIn) {
    alert('로그인이 필요한 기능입니다.')
    next({ name: 'LogInView' })
  } else {
    next()
  }
})

router.beforeEach((to, from, next) => {
  const accountStore = useAccountStore()
  const user = accountStore.profile  // ✅ 로그인 사용자 정보

  if (to.meta.requiresAdmin && !user?.is_superuser) {
    alert('관리자만 접근할 수 있습니다.')
    return next({ name: 'home' })
  }

  next()
})

export default router

// vue-web\src\router\index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue'
import ClerkPage from '../views/ClerkPage.vue'
import UserRegister from '../views/UserRegister.vue'  
import UserLogin from '../views/UserLogin.vue'  
import UserhardDel from '../views/UserhardDel.vue'  
import UsersoftDel from '../views/UsersoftDel.vue'  
import UserProfile from '../views/UserProfile.vue'
import UpdateProfile from '../views/UpdateProfile.vue'
import GenerateUnpaidBill from '../views/GenerateUnpaidBill.vue';
import QueryUnpaidBills from '../views/QueryUnpaidBills';
import MakePayment from '../views/MakePayment.vue';
import GetClerkUnpaidBills from '../views/GetClerkUnpaidBills.vue';
import ClerkCharge from '../views/ClerkCharge.vue';


// rest of your router configurations ...

const routes = [
  {
    path: '/',
    component: HomePage
  },  
  {
    path: '/c',
    component:ClerkPage 
  },

  {
    path: '/login',
    component: UserLogin
  },  
  {
    path: '/users/register',
    component: UserRegister
  },
  {
    path: '/users/soft_delete',
    component: UsersoftDel
  }, {
    path: '/users/hard_delete',
    component: UserhardDel
  },
  {
    path: '/profile',
    component: UserProfile,
  },
  {
    path: '/profile/update',
    component: UpdateProfile
  },
  {
    path: '/bills/generate',
    component: GenerateUnpaidBill
  },
  {
    path: '/bills',
    component: QueryUnpaidBills
  },
  {
    name: 'pay',
    path: '/payments',
    component: MakePayment
  },
  {
    path: '/clerk/unpaid_bills',
    component: GetClerkUnpaidBills
  },
  {
    name: 'charge',
    path: '/clerk/charge',
    component: ClerkCharge
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
}); 

export default router;

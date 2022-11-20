import Vue from "vue";
import VueRouter from "vue-router";
import Cards from '../components/CardsList.vue'

Vue.use(VueRouter);

const routes = [
 {
   path : '/cards',
   name : 'Cards',
   component : Cards,
 }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
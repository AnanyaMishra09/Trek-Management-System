import { createRouter, createWebHistory } from "vue-router";
import { auth } from "./stores/auth";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import AdminDashboard from "./components/admin/Dashboard.vue";
import AdminTreks from "./components/admin/Treks.vue";
import AdminStaff from "./components/admin/Staff.vue";
import AdminUsers from "./components/admin/Users.vue";
import AdminBookings from "./components/admin/Bookings.vue";
import StaffDashboard from "./components/staff/Dashboard.vue";
import StaffTrekManage from "./components/staff/TrekManage.vue";
import UserDashboard from "./components/user/Dashboard.vue";
import UserTrekList from "./components/user/TrekList.vue";
import UserProfile from "./components/user/Profile.vue";
import UserHistory from "./components/user/History.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/admin",
    component: AdminDashboard,
    meta: { role: "admin" },
    children: [
      { path: "treks", component: AdminTreks },
      { path: "staff", component: AdminStaff },
      { path: "users", component: AdminUsers },
      { path: "bookings", component: AdminBookings },
    ],
  },
  {
    path: "/staff",
    component: StaffDashboard,
    meta: { role: "staff" },
    children: [{ path: "treks/:id", component: StaffTrekManage }],
  },
  {
    path: "/user",
    component: UserDashboard,
    meta: { role: "trekker" },
    children: [
      { path: "", component: UserTrekList },
      { path: "history", component: UserHistory },
      { path: "profile", component: UserProfile },
    ],
  },
];

export const roleHome = { admin: "/admin", staff: "/staff", trekker: "/user" };

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  if (to.meta.role && !auth.token) return "/login";
  if (to.meta.role && auth.role !== to.meta.role) return roleHome[auth.role];
});

export default router;

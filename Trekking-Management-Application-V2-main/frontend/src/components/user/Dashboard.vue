<script setup>
import { useRouter } from "vue-router";
import { auth, clearAuth } from "../../stores/auth";

const router = useRouter();

function logout() {
  clearAuth();
  router.push("/login");
}
</script>

<template>
  <nav class="navbar navbar-expand navbar-dark bg-dark px-3">
    <span class="navbar-brand">⛰️ Trekking - {{ auth.name }}</span>
    <div class="navbar-nav me-auto">
      <router-link class="nav-link" to="/user">Explore Treks</router-link>
      <router-link class="nav-link" to="/user/history">My History</router-link>
      <router-link class="nav-link" to="/user/profile">Profile</router-link>
    </div>
    <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
  </nav>

  <div class="container my-4">
    <router-view />
  </div>
</template>

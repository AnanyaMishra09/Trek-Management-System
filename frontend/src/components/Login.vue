<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { roleHome } from "../router.js";
import { setAuth } from "../stores/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const validated = ref(false);
const router = useRouter();

async function onSubmit(e) {
  validated.value = true;
  if (!e.target.checkValidity()) return;
  await submit();
}

async function submit() {
  error.value = "";
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email.value, password: password.value }),
  });
  const data = await res.json();
  if (!res.ok) {
    error.value = data.error || "Login failed";
    return;
  }
  setAuth(data);
  router.push(roleHome[data.role]);
}
</script>

<template>
  <div class="auth-shell d-flex justify-content-center align-items-center vh-100">
    <form
      novalidate
      :class="{ 'was-validated': validated }"
      class="auth-card card p-4 p-md-5 shadow-lg"
      style="width: 24rem"
      @submit.prevent="onSubmit"
    >
      <div class="text-center mb-4">
        <div class="auth-mark">⛰️</div>
        <h1 class="h4 mt-2 mb-0">Welcome back</h1>
        <p class="text-muted small mb-0">Log in to Trekking Management</p>
      </div>
      <div class="mb-3">
        <label class="form-label small text-muted">Email</label>
        <input class="form-control" v-model="email" type="email" placeholder="you@example.com" required />
        <div class="invalid-feedback">Enter a valid email.</div>
      </div>
      <div class="mb-3">
        <label class="form-label small text-muted">Password</label>
        <input class="form-control" v-model="password" type="password" placeholder="••••••••" required />
        <div class="invalid-feedback">Password is required.</div>
      </div>
      <button class="btn btn-primary w-100" type="submit">Login</button>
      <p v-if="error" class="text-danger mt-2 mb-0 small">{{ error }}</p>
      <router-link class="d-block text-center mt-4 small" to="/register">Need an account? Register</router-link>
    </form>
  </div>
</template>

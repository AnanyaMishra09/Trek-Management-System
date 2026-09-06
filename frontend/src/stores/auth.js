import { reactive } from "vue";

const stored = JSON.parse(localStorage.getItem("auth") || "null");

export const auth = reactive({
  token: stored?.token || null,
  role: stored?.role || null,
  name: stored?.name || null,
});

export function setAuth({ token, role, name }) {
  auth.token = token;
  auth.role = role;
  auth.name = name;
  localStorage.setItem("auth", JSON.stringify({ token, role, name }));
}

export function clearAuth() {
  auth.token = null;
  auth.role = null;
  auth.name = null;
  localStorage.removeItem("auth");
}

/**
 * Feature F18 - Client-side token lifecycle guard.
 * Design intent: keep route protection and token invalidation deterministic before any
 * business page starts issuing privileged requests.
 */
import axios from "axios";
import { service } from "@/service";

export const checkToken = () => {
  const token = localStorage.getItem("token");
  if (token === null) {
    return false;
  }

  axios.defaults.headers.common.Authorization = `Bearer ${token}`;
  return true;
};

export const validateToken = async () => {
  if (!checkToken()) {
    return false;
  }

  try {
    await service.user.check();
    return true;
  } catch (err) {
    if (err?.response?.status === 401) {
      delete axios.defaults.headers.common.Authorization;
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("email");
      localStorage.removeItem("userID");
      localStorage.removeItem("userType");
    }
    return false;
  }
};

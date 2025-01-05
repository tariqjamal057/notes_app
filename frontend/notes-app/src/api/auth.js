import axios from "axios";

class AuthAPI {
  static #API_URL = "http://localhost:8000";

  static #axiosInstance = axios.create({
    baseURL: this.#API_URL,
    timeout: 5000,
    headers: {
      "Content-Type": "application/json",
    },
  });

  static {
    this.#axiosInstance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
  }

  static #handleError(error) {
    if (error.response) {
      console.error("Auth Error:", error.response.data);
      throw error.response.data;
    } else if (error.request) {
      console.error("Network Error:", error.request);
      throw new Error("Network error. Please check your connection.");
    } else {
      console.error("Request Error:", error.message);
      throw error;
    }
  }

  static async login(credentials) {
    try {
      const response = await this.#axiosInstance.post(
        "/auth/login",
        credentials
      );
      return response.data;
    } catch (error) {
      this.#handleError(error);
    }
  }

  static async register(userData) {
    try {
      const response = await this.#axiosInstance.post(
        "/auth/register",
        userData
      );
      return response.data;
    } catch (error) {
      this.#handleError(error);
    }
  }

  static async refreshToken() {
    try {
      const refresh_token = localStorage.getItem("refresh_token");
      const response = await this.#axiosInstance.post(
        "/auth/refresh",
        {},
        {
          headers: { Authorization: `Bearer ${refresh_token}` },
        }
      );

      const { access_token } = response.data;
      localStorage.setItem("access_token", access_token);
      return response.data;
    } catch (error) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
      throw error;
    }
  }
}

export default AuthAPI;

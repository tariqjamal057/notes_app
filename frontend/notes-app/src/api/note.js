import axios from "axios";
import AuthAPI from "./auth";

class NotesAPI {
  static #API_URL = "http://localhost:8000";

  static #axiosInstance = axios.create({
    baseURL: this.#API_URL,
    timeout: 5000,
  });

  // Add interceptors for token handling and error management
  static {
    this.#axiosInstance.interceptors.request.use((config) => {
      const token = localStorage.getItem("access_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    this.#axiosInstance.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        // If unauthorized and not a refresh token request, try to refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            await AuthAPI.refreshToken();
            return this.#axiosInstance(originalRequest);
          } catch (refreshError) {
            window.location.href = "/login";
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  // Centralized error handling
  static #handleError(error) {
    console.error("API Error:", error);
    throw error;
  }

  // Generic method for GET requests
  static async #get(endpoint) {
    try {
      const response = await this.#axiosInstance.get(endpoint);
      return response.data;
    } catch (error) {
      this.#handleError(error);
    }
  }

  // Generic method for POST requests
  static async #post(endpoint, data) {
    try {
      const response = await this.#axiosInstance.post(endpoint, data);
      return response.data;
    } catch (error) {
      this.#handleError(error);
    }
  }

  // Generic method for PUT requests
  static async #put(endpoint, data) {
    try {
      const response = await this.#axiosInstance.put(endpoint, data);
      return response.data;
    } catch (error) {
      this.#handleError(error);
    }
  }

  // Generic method for DELETE requests
  static async #delete(endpoint) {
    try {
      const response = await this.#axiosInstance.delete(endpoint);
      return response.data;
    } catch (error) {
      this.#handleError(error);
    }
  }

  static async getAllNotes() {
    return this.#get("/notes");
  }

  static async createNote(noteData) {
    return this.#post("/notes", {
      title: noteData.title,
      content: noteData.content,
    });
  }

  static async updateNote(noteId, noteData) {
    return this.#put(`/notes/${noteId}`, {
      title: noteData.title,
      content: noteData.content,
    });
  }

  static async deleteNote(noteId) {
    return this.#delete(`/notes/${noteId}`);
  }
}

export default NotesAPI;

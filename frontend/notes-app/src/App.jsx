import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import SignUp from "./pages/Signup";

const PrivateRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkTokenValidity = () => {
      const token = localStorage.getItem("access_token");
      const tokenExpiry = localStorage.getItem("token_expiry");

      if (token && tokenExpiry) {
        const currentTime = new Date();
        const expiryTime = new Date(tokenExpiry);

        if (currentTime < expiryTime) {
          setIsAuthenticated(true);
        } else {
          // Token has expired
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          localStorage.removeItem("token_expiry");
          setIsAuthenticated(false);
        }
      } else {
        // No token or expiry found
        setIsAuthenticated(false);
      }
    };

    checkTokenValidity();
  }, []);

  return children;
};

function App() {
  return (
    <BrowserRouter>
      <div className="bg-gray-100 min-h-screen">
        <Navbar />
        <div className="container p-6">
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<SignUp />} />

            {/* Protected Routes */}
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Home />
                </PrivateRoute>
              }
            />

            {/* Redirect to login for any undefined routes */}
            <Route path="*" element={<Navigate to="/login" />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;

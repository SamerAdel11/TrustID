import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode'; // Corrected import for jwtDecode
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const storedAuthTokens = localStorage.getItem('authTokens');
  const initialUser = storedAuthTokens ? jwtDecode(storedAuthTokens) : null;
  const [user, setUser] = useState(initialUser);
  const initialAuthTokens = storedAuthTokens ? JSON.parse(storedAuthTokens) : null;
  const [authTokens, setAuthTokens] = useState(initialAuthTokens);
  const [loading, setLoading] = useState(true);
  const host = import.meta.env.VITE_API_HOST;
  const navigate = useNavigate();

  const fetchUser = async () => {
    if (authTokens) {
      try {
        const response = await fetch(`${host}/verified/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${authTokens.access}`,
          },
        });
        const data = await response.json();
        setUser({ ...jwtDecode(authTokens.access), verified: data.verified });
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  };


  const loginUser = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${host}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email.value, password: password.value }),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error(data.detail[0] || "Login Failed -- NO json response");
        return null;
      }

      localStorage.setItem('authTokens', JSON.stringify(data));
      console.log('Login Successful');
      const loggedUser = jwtDecode(data.access_token);
      setUser(loggedUser);
      console.log(loggedUser);
      navigate('/home');
      return data;
    } catch (error) {
      console.error('Error during login:', error.message);
      return null;
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    navigate('/');
  };

  const updateToken = async () => {
    console.log('Tokens have been updated');
    if (authTokens) {
      try {
        const response = await fetch(`${host}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authTokens?.refresh_token}` },
          // body: JSON.stringify({ refresh: authTokens.refresh_token }),
        });
        const tokens = await response.json();
        if (response.status === 200) {
          setAuthTokens(tokens);
          setUser(jwtDecode(tokens.access));
          localStorage.setItem('authTokens', JSON.stringify(tokens));
        } else {
          // logoutUser();
        }
      } catch (error) {
        console.error('Error updating token:', error);
        // logoutUser();
      }
    } else {
      setLoading(false);
    }
  };

  // Ensure the interval only runs if authTokens are present
  useEffect(() => {
    if (authTokens) {
      const interval = setInterval(() => {
        console.log("Should be refreshed")
        updateToken();
      }, 1000 * 60*1); // 1 Minute

      return () => clearInterval(interval);
    }
  }, [authTokens]); // This will run when authTokens changes

  const contextData = {
    user,
    authTokens,
    login: loginUser,
    logout: logoutUser,
    loading,
    // googleLogin,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;

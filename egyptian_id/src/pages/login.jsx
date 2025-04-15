import React, { useState, useContext } from "react";
import '../css/login.css'
import Navbar from "../components/navbar";
import { useNavigate } from 'react-router-dom'
import AuthContext from "../context/Authcontext";

const Login = () => {
  const {login}=useContext(AuthContext);
  const [passwordVisible, setPasswordVisible] = useState(false);
  const navigate = useNavigate()
  // const host = import.meta.env.VITE_API_HOST;

  const togglePasswordVisibility = () => {
    setPasswordVisible(!passwordVisible);
  };


  return (
    <>
    <Navbar/>
        <section className="service_section layout_padding">
          <div className="service_container">
            <div className="container">
              <div className="heading_container heading_center">
                <div className="login-container">
                  <h2>Login</h2>
                  <form onSubmit={login}>
                    <div className="input-group">
                      <i className="fas fa-user"></i>
                      <input
                        type="text"
                        id="email" 
                        placeholder="Email"  
                        required
                      />
                    </div>
                    <div style={{ position: "relative" }} className="input-group">
                      <i className="fas fa-lock"></i>
                      <input
                        type="password"
                        id="password"
                        placeholder="Password"
                        required 
                      />

                      <i
                        className={passwordVisible ? "fas fa-eye-slash" : "fas fa-eye"}
                        id="togglePassword"
                        onClick={togglePasswordVisibility}
                        style={{ cursor: "pointer"}}
                      ></i>
                    </div>
                    <button type="submit" onSubmit={login} className="login-btn" id="login-btn">
                      Login
                    </button>
                    <div className="extra-links">
                      <a href="#">Forgot Password?</a>
                      <a href="#">Sign Up</a>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </section>
        </>
  );
};
export default Login;

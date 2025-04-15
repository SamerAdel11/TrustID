import React from "react";

const Register = () => {

    return <>
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
    </>
}
export default Register
import {React, useContext} from "react";
import AuthContext from "../context/Authcontext";
const Welcome = () => {
  const { user } = useContext(AuthContext);
  
  return (
    <div className="container mt-4 pr-0 pl-0 ">
      <div className="welcome-section bg-white p-4 rounded-3 shadow-sm">
        <h4 className="fw-bold">Welcome, {user?.first_name}!</h4>
        <p className="mb-1">
          Use our OCR system to extract text from ID cards quickly and efficiently.
          Upload an image, and we'll do the rest!
        </p>
      </div>
    </div>
  );
};

export default Welcome;

import { useState } from 'react';
import reactLogo from './assets/react.svg';
// import './App.css'
import DashBoard from './pages/dashboard';
import Navbar from './components/navbar';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './css/bootstrap.css';
// import './css/font-awesome.min.css';
import './css/style.css';
import './css/responsive.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Login from './pages/login';
import { AuthProvider } from './context/Authcontext';

function App() {
  // const [count, setCount] = useState(0)

  return (
    <Router>
      {/* <Navbar/> */}
      <AuthProvider>
        <Routes>
          <Route path='/' element={<Navbar/>}/>
          <Route path='/login' element={<Login/>}/>
          <Route path='/home' element={<DashBoard/>}/>
        </Routes>
      {/* </Navbar> */}
      </AuthProvider>

    </Router>

  )
}

export default App

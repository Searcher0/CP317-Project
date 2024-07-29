// src/components/Header.jsx
import { Link } from 'react-router-dom';
import '../styles/Header.css';
import logo from "../assets/logo.png";

const Header = () => (
  <nav className="nav">
    <Link to="/">
      <img src={logo} alt="Grocery Guru Logo" className="logo" />
    </Link>
    <div className="nav-links">
      <Link to="/" className="nav-link">Home</Link>
      <Link to="/about" className="nav-link">About us</Link>
      <Link to="/create-list" className="nav-link">Create a list</Link>
    </div>
  </nav>
);

export default Header;
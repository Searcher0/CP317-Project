// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import AboutUs from './pages/AboutUs';
import CreateList from './pages/CreateList';
import Footer from './components/Footer';
import './styles/App.css'; // Import global styles

const App = () => (
  <Router>
    <Header />
    <main>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/create-list" element={<CreateList />} />
      </Routes>
    </main>
    <Footer />
  </Router>
);

export default App;
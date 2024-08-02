import React, { useEffect } from 'react';
import '../styles/AboutUs.css';
import Adnan from "../assets/Adnan.jpeg";
import Waleed from "../assets/waleed.jpeg";
import George from "../assets/George.jpg";
import Muneeb from "../assets/Muneeb.jpeg";

const teamMembers = [
  { name: 'George Salib', role: 'Lead Developer', image: George, description: 'George is the front and backend developer for this project.' },
  { name: 'Muneeb Zaidi', role: 'Backend Developer', image: Muneeb, description: 'Muneeb is the backend developer that developed the webscraper.' },
  { name: 'Yousif Salman', role: 'Customer Support', image: 'https://via.placeholder.com/50', description: 'Yousif is the backend developer that developed the webscraper.' },
  { name: 'Adnan Awad', role: 'UI Designer', image: Adnan, description: 'Adnan designed the front-end interface and handled the documentation of our project' },
  { name: 'Waleed Asif', role: 'UI Designer', image: Waleed, description: 'Waleed designed the front-end interface and handled the documentation of our project' },
];

const AboutUs = () => {
  useEffect(() => {
    const handleVisibility = () => {
      const elements = document.querySelectorAll('.fade-in-section');
      elements.forEach((element) => {
        const rect = element.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom >= 0;
        if (isVisible) {
          element.classList.add('fade-in');
        } else {
          element.classList.remove('fade-in');
        }
      });
    };

    handleVisibility(); // Check visibility on initial load
    window.addEventListener('scroll', handleVisibility);
    return () => {
      window.removeEventListener('scroll', handleVisibility);
    };
  }, []);

  return (
    <div className="aboutus-container">
      <section className="aboutus-section fade-in-section section-1">
        <h1 className="aboutus-title">About Us</h1>
        <p className="aboutus-description">
          At Grocery Guru, we are committed to making grocery shopping as convenient and affordable as possible. Our mission is to help you save both time and money by providing a seamless and efficient way to find the best deals on your grocery list.
        </p>
        <h2 className="aboutus-subtitle">How It Works</h2>
        <p className="aboutus-description">
          Using our advanced internal web scraper, we have developed a sophisticated algorithm capable of sorting grocery items from most expensive to cheapest. By analyzing the shopping lists provided by our clients, our system ensures that you receive the most cost-effective options available in your area.
        </p>
      </section>
      <section className="aboutus-section fade-in-section section-2">
        <h2 className="aboutus-subtitle">Commitment to Quality</h2>
        <p className="aboutus-description">
          We are committed to providing a high-quality service that you can rely on. Our team regularly tests and updates our system to ensure accuracy and efficiency. We value your feedback and are always looking for ways to enhance your experience with Grocery Guru.
        </p>
      </section>
      <section className="aboutus-section fade-in-section section-3">
        <h2 className="aboutus-subtitle">Get Started Today</h2>
        <p className="aboutus-description">
          Join the many satisfied customers who have discovered the benefits of using Grocery Guru. Start saving money on your groceries today by creating your shopping list and letting us find the best deals for you. We are here to make your grocery shopping experience stress-free and affordable.
        </p>
      </section>
      <section className="team-section fade-in-section section-9">
        <h2 className="aboutus-subtitle">Meet the Team</h2>
        <div className="team-container">
          {teamMembers.map((member, index) => (
            <div className="team-member" key={index}>
              <img src={member.image} alt={member.name} className="team-member-image" />
              <div className="team-member-info">
                <h3 className="team-member-name">{member.name}</h3>
                <p className="team-member-role">{member.role}</p>
                <p className="team-member-description">{member.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default AboutUs;
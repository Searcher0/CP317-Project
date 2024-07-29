import React, { useEffect } from 'react';
import '../styles/AboutUs.css';

const teamMembers = [
  { name: 'Alice', role: 'Developer', image: 'https://via.placeholder.com/50', description: 'Alice is a highly skilled developer with over 10 years of experience.' },
  { name: 'Cornelius', role: 'Data Analyst', image: 'https://via.placeholder.com/50', description: 'Cornelius is a data analyst who ensures our database is always up to date.' },
  { name: 'Charlie', role: 'Customer Support', image: 'https://via.placeholder.com/50', description: 'Charlie leads our customer support team, helping users with any issues.' },
  { name: 'Dave', role: 'Project Manager', image: 'https://via.placeholder.com/50', description: 'Dave oversees all projects, ensuring everything runs smoothly.' },
  { name: 'Eve', role: 'Marketing Specialist', image: 'https://via.placeholder.com/50', description: 'Eve handles marketing and ensures our platform reaches more users.' },
];

const AboutUs = () => {
  useEffect(() => {
    const handleScroll = () => {
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

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
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
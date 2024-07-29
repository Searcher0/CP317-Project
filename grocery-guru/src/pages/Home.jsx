import React, { useState, useEffect } from 'react';
import Map from '../components/Map';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../styles/Home.css';
import image from "../assets/home.jpg";

const defaultLocation = { lat: 43.4723, lng: -80.5449 };

const Home = () => {
  const [location, setLocation] = useState(defaultLocation);
  const [stores, setStores] = useState([]);
  const [popupContent, setPopupContent] = useState(null);

  useEffect(() => {
    const sections = document.querySelectorAll('.intro-section, .how-it-works-section, .testimonials-section');
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate');
          }
        });
      },
      { threshold: 0.1 }
    );

    sections.forEach(section => {
      observer.observe(section);
    });

    return () => {
      sections.forEach(section => {
        observer.unobserve(section);
      });
    };
  }, []);

  const handleStoreClick = (index) => {
    const store = stores[index];
    setPopupContent(store);
  };

  const closePopup = () => {
    setPopupContent(null);
  };

  const testimonials = [
    {
      text: "This website has saved me so much time and money. I always find the cheapest products in my area. Thank you Grocery Guru!",
      name: "Alice",
      image: "https://via.placeholder.com/50"
    },
    {
      text: "Grocery Guru is fantastic! I can always find the best deals on groceries.",
      name: "Bob",
      image: "https://via.placeholder.com/50"
    },
    {
      text: "The best grocery shopping helper ever! Highly recommend Grocery Guru to everyone.",
      name: "Charlie",
      image: "https://via.placeholder.com/50"
    },
    {
      text: "I was able to cut down my grocery bill significantly thanks to Grocery Guru.",
      name: "Dave",
      image: "https://via.placeholder.com/50"
    },
    {
      text: "Fantastic app! Makes grocery shopping so much easier and cheaper.",
      name: "Eve",
      image: "https://via.placeholder.com/50"
    }
  ];

  const settings = {
    dots: true,
    infinite: true,
    speed: 2000,
    slidesToShow: 2,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 5000,
    pauseOnHover: true,
    arrows: true,
    adaptiveHeight: true,
    centerMode: false,
  };

  const renderTestimonials = () => {
    return testimonials.map((testimonial, index) => (
      <div className="testimonial-slide" key={index}>
        <div className="testimonial">
          <img src={testimonial.image} alt={testimonial.name} className="testimonial-image" />
          <div>
            <div className="testimonial-name">{testimonial.name}</div>
            <p>{testimonial.text}</p>
          </div>
        </div>
      </div>
    ));
  };

  return (
    <div className="home-container">
      <section className="intro-section">
        <div className="image-placeholder">
          <img src={image} alt="Grocery Guru" className="home-image" />
        </div>
        <div className="intro-text">
          <h1 className="home-title">Grocery Guru</h1>
          <p className="home-description">
            Shopping during these financially difficult times can be hard on many people, that's why here at Grocery Guru we make it simple. Let us know the products you need and we will find you the cheapest places to get them.
          </p>
        </div>
      </section>
      <section className="how-it-works-section">
        <h2 className="how-it-works-title">How It Works</h2>
        <div className="how-it-works-content">
          <div className="step">
            <div className="step-number">1</div>
            <div className="step-text">Tell us what products you need.</div>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <div className="step-text">We search for the best prices.</div>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <div className="step-text">Get a list of the cheapest stores.</div>
          </div>
        </div>
      </section>
      <section className="testimonials-section">
        <h2 className="testimonials-title">Read what our customers say:</h2>
        <Slider {...settings}>
          {renderTestimonials()}
        </Slider>
      </section>
      <section className="stores-section">
        <Map location={location} setLocation={setLocation} stores={stores} setStores={setStores} />
        <div className="stores-list">
          <h3 className="stores-list-title">List of stores - 10km radius</h3>
          <div className="stores-list-scroll">
            <ul>
              {stores.map((store, index) => (
                <li key={index} title={`Address: ${store.address}`} onClick={() => handleStoreClick(index)}>
                  {store.name}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>
      {popupContent && (
        <div className="modal-overlay" onClick={closePopup}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-button" onClick={closePopup}>X</button>
            <h4>{popupContent.name}</h4>
            <p>{popupContent.address}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
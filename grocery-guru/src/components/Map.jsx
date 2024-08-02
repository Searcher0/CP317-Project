import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import locationIcon from '../assets/location.png';
import PropTypes from 'prop-types';

const defaultLocation = { lat: 43.4723, lng: -80.5449 };

const Map = ({ location, setLocation, stores, setStores }) => {
  const mapRef = useRef(null);
  const userMarkerRef = useRef(null);
  const markersRef = useRef([]);
  const mapInstanceRef = useRef(null);

  useEffect(() => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove();
    }

    const initializeMap = () => {
      const map = L.map(mapRef.current).setView([location.lat, location.lng], 13);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);

      const redIcon = new L.Icon({
        iconUrl: locationIcon,
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34]
      });

      userMarkerRef.current = L.marker([location.lat, location.lng], { icon: redIcon }).addTo(map)
        .bindPopup('You are here')
        .openPopup();

      map.on('click', (e) => {
        const { lat, lng } = e.latlng;
        fetchAddress(lat, lng, map);
      });

      mapInstanceRef.current = map;

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { latitude, longitude } = position.coords;
            setLocation({ lat: latitude, lng: longitude });
            map.setView([latitude, longitude], 13);
            userMarkerRef.current.setLatLng([latitude, longitude]);
            fetchNearbyStores(latitude, longitude, map);
          },
          () => {
            fetchNearbyStores(location.lat, location.lng, map);
          }
        );
      } else {
        fetchNearbyStores(location.lat, location.lng, map);
      }
    };

    initializeMap();

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  const fetchNearbyStores = async (lat, lng, map) => {
    const overpassUrl = `https://overpass-api.de/api/interpreter?data=[out:json][timeout:25];nwr["shop"="supermarket"](around:5000,${lat},${lng});out geom;`;

    try {
      const response = await axios.get(overpassUrl);
      const elements = response.data.elements;

      const allStores = elements.map(store => {
        const storeLat = store.lat || (store.center && store.center.lat) || (store.geometry && store.geometry[0] && store.geometry[0].lat);
        const storeLng = store.lon || (store.center && store.center.lon) || (store.geometry && store.geometry[0] && store.geometry[0].lon);
        return {
          name: store.tags.name || 'Unknown Store',
          lat: storeLat,
          lng: storeLng,
          address: `${store.tags["addr:street"] || ''}, ${store.tags["addr:city"] || ''}`,
          shop: store.tags.shop
        };
      }).filter(store => store.lat && store.lng); // filter out stores with no lat/lng

      console.log('Fetched stores:', allStores);

      // Filter stores based on specific names
      const filteredStores = allStores.filter(store => 
        // store.name.toLowerCase().includes('metro') || 
        // store.name.toLowerCase().includes('superstore') || 
        store.name.toLowerCase().includes('walmart') || 
        store.name.toLowerCase().includes('loblaws') ||
        store.name.toLowerCase().includes('no frills')
      );

      console.log('Filtered stores:', filteredStores);

      setStores(filteredStores);

      markersRef.current.forEach(marker => marker.remove());
      markersRef.current = [];

      filteredStores.forEach((store, index) => {
        const marker = L.marker([store.lat, store.lng]).addTo(map)
          .bindPopup(`${store.name}<br>${store.address}`);
        markersRef.current[index] = marker;
      });
    } catch (error) {
      console.error('Error fetching stores:', error);
    }
  };

  const fetchAddress = async (lat, lng, map) => {
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`);
      const data = await response.json();
      L.popup()
        .setLatLng([lat, lng])
        .setContent(data.display_name)
        .openOn(map);
    } catch (error) {
      console.error('Error fetching address:', error);
    }
  };

  return <div id="map" ref={mapRef} className="map-placeholder"></div>;
};

Map.propTypes = {
  location: PropTypes.object.isRequired,
  setLocation: PropTypes.func.isRequired,
  stores: PropTypes.array.isRequired,
  setStores: PropTypes.func.isRequired,
};

export default Map;
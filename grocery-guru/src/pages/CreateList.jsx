import React, { useState, useEffect } from "react";
import "../styles/CreateList.css";
import logo from "../assets/logo.png"; // Make sure the path to your logo is correct

const CreateList = () => {
  const [items, setItems] = useState([]);
  const [input, setInput] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [allItems, setAllItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [results, setResults] = useState(null);
  const [ignoreMissing, setIgnoreMissing] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [showContent, setShowContent] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5001/getall");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        data.sort((a, b) => a.localeCompare(b)); // Sort items alphabetically
        setAllItems(data);
        console.log("Fetched items:", data); // Debugging line
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
        setTimeout(() => {
          setShowContent(true);
        }, 3000); // Ensure loading screen stays for 3 seconds
      }
    };

    fetchData();
  }, []);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInput(value);

    if (value.trim()) {
      const filteredSuggestions = allItems.filter((item) =>
        item.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filteredSuggestions);
    } else {
      setSuggestions(allItems); // Show all items if input is empty
    }
  };

  const handleInputFocus = () => {
    setSuggestions(allItems); // Show all items when the input is focused
  };

  const addItem = (item) => {
    if (item.trim()) {
      setItems([...items, item.trim()]);
      setInput("");
      const newAllItems = allItems.filter((i) => i !== item.trim());
      setAllItems(newAllItems);
      setSuggestions([]);
    }
  };

  const removeItem = (index) => {
    const removedItem = items[index];
    setItems(items.filter((_, i) => i !== index));
    const newAllItems = [...allItems, removedItem].sort((a, b) =>
      a.localeCompare(b)
    );
    setAllItems(newAllItems);
    setSuggestions(newAllItems);
  };

  const searchCheapestStore = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5001/cheapest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ items }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
    setLoading(false);
    setShowPopup(true);
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  const handleBackgroundClick = (e) => {
    if (e.target.classList.contains("popup")) {
      closePopup();
    }
  };

  useEffect(() => {
    if (results) {
      const sortedStores = [...results.sorted_stores];
      sortedStores.sort(([storeA, totalA], [storeB, totalB]) => {
        const missingA = results.missing_items[storeA].length;
        const missingB = results.missing_items[storeB].length;
        return ignoreMissing
          ? totalA - totalB
          : missingA - missingB || totalA - totalB;
      });
      setResults((prevResults) => ({
        ...prevResults,
        sorted_stores: sortedStores,
      }));
    }
  }, [ignoreMissing, results]);

  if (loading || !showContent) {
    return (
      <div className="loading-screen">
        <img src={logo} alt="Loading..." className="loading-logo" />
        <p className="loading-text">Loading...</p>
      </div>
    );
  }

  return (
    <div className="create-container">
      <h1 className="create-title">Create a List</h1>
      <div className="input-button-container">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          placeholder="Search item"
          className="create-input"
        />
        <button onClick={searchCheapestStore} className="create-button">
          Search Cheapest Store
        </button>
      </div>
      {suggestions.length > 0 && (
        <div className="suggestions">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="suggestion-item"
              onClick={() => addItem(suggestion)}
            >
              {suggestion}
            </div>
          ))}
        </div>
      )}
      <div className="list-divider"></div>
      <div className="list-container notepad">
        {items.length === 0 && <p>No items in the list</p>}
        {items.map((item, index) => (
          <div key={index} className="list-item">
            <span>
              {index + 1} - {item}
            </span>
            <button onClick={() => removeItem(index)} className="remove-button">
              Remove
            </button>
          </div>
        ))}
      </div>
      {loading && <div className="loading">Loading...</div>}
      {showPopup && results && (
        <div className="popup" onClick={handleBackgroundClick}>
          <div className="popup-content" onClick={(e) => e.stopPropagation()}>
            <h2>Cheapest Stores</h2>
            <button
              onClick={() => setIgnoreMissing(!ignoreMissing)}
              className="popup-button"
            >
              {ignoreMissing
                ? "Consider Missing Items"
                : "Ignore Missing Items"}
            </button>
            {results.sorted_stores.map(([store, total], index) => (
              <div
                key={index}
                className="store"
                onClick={() =>
                  document.getElementById(store).classList.toggle("hidden")
                }
              >
                <div className="store-header">
                  <h3>{store}</h3>
                  <span>
                    ${total.toFixed(2)}{" "}
                    {results.missing_items[store].length > 0 && (
                      <span className="missing-items">(Missing items)</span>
                    )}
                  </span>
                </div>
                <div id={store} className="store-details hidden">
                  {Object.entries(results.store_data[store]).map(
                    ([item, details], idx) => (
                      <div key={idx}>
                        <span>{item}</span>
                        <span>
                          $
                          {typeof details.price === "number"
                            ? details.price.toFixed(2)
                            : details.price}
                        </span>
                      </div>
                    )
                  )}
                  {results.missing_items[store].length > 0 && (
                    <div className="missing-items">
                      {results.missing_items[store].map((missing, idx) => (
                        <div key={idx}>
                          <span>{missing}</span>
                          <span>Missing</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            <button onClick={closePopup} className="popup-button">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default CreateList;

// src/pages/CreateList.jsx
import React, { useState } from 'react';
import '../styles/CreateList.css';

const CreateList = () => {
  const [items, setItems] = useState([]);
  const [input, setInput] = useState('');

  const addItem = () => {
    if (input.trim()) {
      setItems([...items, input.trim()]);
      setInput('');
    }
  };

  const removeItem = (index) => {
    setItems(items.filter((_, i) => i !== index));
  };

  return (
    <div className="create-container">
      <h1 className="create-title">Create a List</h1>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Search item"
        className="create-input"
      />
      <button onClick={addItem} className="create-button">Add Item</button>
      {items.map((item, index) => (
        <div key={index} className="list-item">
          <span>{index + 1} - {item}</span>
          <button onClick={() => removeItem(index)}>Remove</button>
        </div>
      ))}
      {/* Additional content here */}
    </div>
  );
};

export default CreateList;
// src/components/UserInput.jsx
import React, { useState } from 'react';

export const UserInput = ({ onSend }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', padding: '10px' }}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ flex: 1, padding: '10px', marginRight: '10px' }}
        placeholder="Type your message..."
      />
      <button type="submit" style={{ padding: '10px' }}>Send</button>
    </form>
  );
};
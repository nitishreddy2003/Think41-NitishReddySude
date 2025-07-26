// src/components/Message.jsx
import React from 'react';

export const Message = ({ message }) => {
  const isUser = message.sender === 'user';
  const messageStyle = {
    padding: '10px',
    margin: '5px',
    borderRadius: '10px',
    maxWidth: '70%',
    alignSelf: isUser ? 'flex-end' : 'flex-start',
    backgroundColor: isUser ? '#dcf8c6' : '#fff',
    border: '1px solid #ddd',
  };

  return <div style={messageStyle}>{message.content}</div>;
};
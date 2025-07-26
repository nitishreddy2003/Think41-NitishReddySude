// src/components/MessageList.jsx
import React from 'react';
import { Message } from './Message.jsx';

export const MessageList = ({ messages }) => {
  return (
    <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', padding: '10px' }}>
      {messages.map((msg, index) => (
        <Message key={index} message={msg} />
      ))}
    </div>
  );
};
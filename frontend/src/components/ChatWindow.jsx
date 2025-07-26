// src/components/ChatWindow.jsx
import React from 'react';
import { MessageList } from './MessageList';
import { UserInput } from './UserInput';

export const ChatWindow = ({ messages, onSend }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', border: '1px solid #ccc' }}>
      <MessageList messages={messages} />
      <UserInput onSend={onSend} />
    </div>
  );
};
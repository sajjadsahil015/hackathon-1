import React from 'react';
import ChatBot from '../components/ChatBot';

// This component wraps the entire Docusaurus application
// The ChatBot will appear on every page
export default function Root({ children }) {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
}

"use client";
import React from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = () => {
  return (
    <div className="h-full">
      <Editor height="100%" language="javascript" theme="vs-dark" />
    </div>
  );
};

export default CodeEditor;
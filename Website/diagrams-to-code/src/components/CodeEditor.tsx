'use client';
import React from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = ({
  code,
  onCodeChange,
}: {
  code: string;
  onCodeChange: (newCode: string) => void;
}) => {
  return (
    <div className='h-full'>
      <Editor
        value={code}
        height='100%'
        language='yaml'
        theme='vs-dark'
        onChange={(newValue) => onCodeChange(newValue || '')}
      />
    </div>
  );
};

export default CodeEditor;

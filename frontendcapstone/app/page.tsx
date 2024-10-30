'use client';
import { useState } from 'react';
import FileUpload from './components/FileUpload';
import FileDisplay from './components/FileDisplay';

export default function Home() {
  const [files, setFiles] = useState([]);

  const handleFileUpload = (newFiles) => {
    setFiles(prev => [...prev, ...newFiles]);
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">File Upload Application</h1>
        <FileUpload onUpload={handleFileUpload} />
        <FileDisplay files={files} />
      </div>
    </main>
  );
}
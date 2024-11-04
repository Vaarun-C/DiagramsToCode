"use client";
import CodeEditor from '@components/CodeEditor';
import FileUploadWrapper from '@components/FileUploadWrapper';
import ParagraphComponent from '@components/ParagraphComponent';
import { useState } from 'react';

export default function Home() {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  const handleFilesUploaded = (files: File[]) => {
    setUploadedFiles(prevFiles => [...prevFiles, ...files]);
    console.log(files);
  };

  return (
    <FileUploadWrapper onFilesUploaded={handleFilesUploaded}>
      <div className="flex h-screen">
        <div className="w-1/2 p-4">
          <ParagraphComponent uploadedFiles={uploadedFiles} onFilesUploaded={handleFilesUploaded}/>
        </div>
        <div className="w-1/2 p-4">
          <CodeEditor />
        </div>
      </div>
    </FileUploadWrapper>
  );
}

'use client';
import CodeEditor from '@components/CodeEditor';
import FileUploadWrapper from '@components/FileUploadWrapper';
import ParagraphComponent from '@components/ParagraphComponent';

import { useState } from 'react';
import { sendDiagrams } from './api/handler';

export default function Home() {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  const handleFilesUploaded = (files: File[]) => {
    setUploadedFiles((prevFiles) => [...prevFiles, ...files]);
    console.log(files);
  };

  const handleDeleteFile = (fileToDelete: File) => {
    setUploadedFiles((prevFiles) =>
      prevFiles.filter((file) => file !== fileToDelete)
    );
  };

  const handleUpload = () => {
    if (uploadedFiles.length == 0)
      alert("No Architecture Diagrams have been uploaded")
    else sendDiagrams(uploadedFiles)
  }

  return (
    <FileUploadWrapper onFilesUploaded={handleFilesUploaded}>
      <div className='flex h-screen'>
        <div className='w-1/2 p-4'>
          <ParagraphComponent
            uploadedFiles={uploadedFiles}
            onFilesUploaded={handleFilesUploaded}
            handleDeleteFile={handleDeleteFile}
            handleUpload={handleUpload}
          />
        </div>
        <div className='w-1/2 p-4'>
          <CodeEditor />
        </div>
      </div>
    </FileUploadWrapper>
  );
}

'use client';
import React from 'react';
import Card from './Card';
import UploadButton from './UploadButton';

function Paragraph({
  uploadedFiles,
  onFilesUploaded,
}: {
  uploadedFiles: File[];
  onFilesUploaded: (files: File[]) => void;
}) {
  return (
    <div className='p-4'>
      <UploadButton onFilesUploaded={onFilesUploaded} />
      <p>Some random text goes here...</p>
      <h2 className='mt-4 font-bold'>Uploaded Images:</h2>
      <div className='grid grid-cols-1 gap-4 mt-2'>
        {uploadedFiles &&
          uploadedFiles.map((file, index) => <Card key={index} file={file} />)}
      </div>
    </div>
  );
}

export default Paragraph;

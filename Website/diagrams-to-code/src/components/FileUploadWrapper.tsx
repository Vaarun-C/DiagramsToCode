'use client';
import React, { useState } from 'react';

function FileUploadWrapper({
  children,
  onFilesUploaded,
}: {
  children: React.ReactNode;
  onFilesUploaded: (files: File[]) => void;
}) {
  const [showOverlay, setShowOverlay] = useState(false);

  const handleDragEnter = (event: React.DragEvent) => {
    event.preventDefault();
    setShowOverlay(true);
  };

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const handleDragLeave = () => {
    setShowOverlay(false);
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    setShowOverlay(false);

    const files = Array.from(event.dataTransfer.files);
    const imageFiles = files.filter((file) => file.type.startsWith('image/'));

    if (imageFiles.length > 0) {
      onFilesUploaded(imageFiles);
    }
  };

  return (
    <div
      onDragEnter={handleDragEnter}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      onDragLeave={handleDragLeave}
      className='relative h-full'
    >
      {showOverlay ? (
        <div className='fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-90 text-white text-xl z-50'>
          <p>Upload Image Here</p>
        </div>
      ) : (
        children
      )}
    </div>
  );
}

export default FileUploadWrapper;

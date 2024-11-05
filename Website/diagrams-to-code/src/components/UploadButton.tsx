'use client';

import React, { useRef } from 'react';
import { Button } from '@nextui-org/react';
import { MdFileUpload } from 'react-icons/md';

function UploadButton({
  onFilesUploaded,
}: {
  onFilesUploaded: (files: File[]) => void;
}) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const selectedFiles = Array.from(event.target.files); // Convert to array
      onFilesUploaded(selectedFiles); // Pass selected files to parent
    }
  };

  return (
    <>
      <Button
        onClick={handleButtonClick}
        endContent={<MdFileUpload />}
        className='flex border-2 items-center gap-2 px-4 py-1 rounded-md hover:bg-gray-700 hover:text-white transition-all duration-200'
      >
        Upload Image
      </Button>
      <input
        type='file'
        accept='image/*'
        ref={fileInputRef}
        className=' hidden'
        onChange={handleFileChange}
      />
    </>
  );
}

export default UploadButton;

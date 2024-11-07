'use client';
import React from 'react';
import Card from './Card';
import UploadButton from './UploadButton';
import GenerateButton from './GenerateButton';

function Paragraph({
  uploadedFiles,
  onFilesUploaded,
  handleDeleteFile,
  handleUpload,
  handleSelectedCard,
}: {
  uploadedFiles: { [key: string]: File };
  onFilesUploaded: (files: File[]) => void;
  handleDeleteFile: (uuid: string) => void;
  handleUpload: () => void;
  handleSelectedCard: (uuid: string) => void;
}) {
  return (
    <div className='p-4 bg-slate-200 h-full relative rounded-md'>
      <div className='flex justify-between'>
        <UploadButton onFilesUploaded={onFilesUploaded} />
        <GenerateButton handleUpload={handleUpload} />
      </div>
      {Object.keys(uploadedFiles).length === 0 ? (
        <div className='flex items-center justify-center h-full text-gray-500 text-lg'>
          No Architecture Diagrams uploaded
        </div>
      ) : (
        <div className='flex flex-wrap gap-3 gap-y-3 mt-2 max-h-[92%] overflow-y-scroll no-scrollbar'>
          {Object.entries(uploadedFiles).map(([uuid, file]) => (
            <Card
              key={uuid}
              file={file}
              uuid={uuid}
              onDelete={handleDeleteFile}
              handleSelect={handleSelectedCard}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default Paragraph;

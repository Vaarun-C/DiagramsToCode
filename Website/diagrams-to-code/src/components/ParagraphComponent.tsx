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
}: {
  uploadedFiles: File[];
  onFilesUploaded: (files: File[]) => void;
  handleDeleteFile: (files: File) => void;
  handleUpload: () => void;
}) {
  return (
    <div className='p-4 bg-slate-200 h-full relative'>
      <div className='flex justify-between'>
      <UploadButton onFilesUploaded={onFilesUploaded} />
      <GenerateButton handleUpload={handleUpload}/>
      </div>
      {uploadedFiles.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-500 text-lg">
          No Architecture Diagrams uploaded
        </div>
      ) : (
        <div className="flex flex-wrap gap-3 gap-y-3 mt-2 max-h-full overflow-y-scroll no-scrollbar">
          {uploadedFiles.map((file, index) => (
            <Card key={index} file={file} onDelete={handleDeleteFile} />
          ))}
        </div>
      )}
    </div>
  );
}

export default Paragraph;

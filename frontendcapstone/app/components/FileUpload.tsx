import { useState } from 'react';

export default function FileUpload({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleFiles = (uploadedFiles) => {
    const filesArray = Array.from(uploadedFiles).map(file => ({
      name: file.name,
      type: file.type,
      size: file.size,
      url: URL.createObjectURL(file)
    }));
    onUpload(filesArray);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  return (
    <div 
      className={`border-2 border-dashed rounded-lg p-8 mb-8 text-center transition-colors
        ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
    >
      <input
        type="file"
        multiple
        onChange={(e) => handleFiles(e.target.files)}
        className="hidden"
        id="fileInput"
      />
      <label
        htmlFor="fileInput"
        className="cursor-pointer block"
      >
        <div className="text-gray-600">
          <p className="mb-2">Drag and drop files here</p>
          <p>or click to select files</p>
        </div>
      </label>
    </div>
  );
}
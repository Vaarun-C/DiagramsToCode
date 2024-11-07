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

  const handleUpload = async () => {
    if (uploadedFiles.length == 0)
      alert("No Architecture Diagrams have been uploaded")
    else {
      // sendDiagrams(uploadedFiles)
      let icon_data = await recognizeIcons();
      // const mock_data = ['AWS::S3::Bucket', 'AWS::Lambda::Function']
      let llm_data = await getLLMsuggestions(icon_data.message);
      let template = await generateAWSTemplate([...icon_data.message, ...llm_data.message])
      console.log("GENERATED TEMPLATE: ")
      console.log(template)
    }
      
  }

  const recognizeIcons = async () => {
    if (uploadedFiles.length == 0)
      alert("No Architecture Diagrams have been uploaded")
    else {//sendDiagrams(uploadedFiles)
      const formData = new FormData();
      formData.append('architectureDiagram', uploadedFiles[0]);
      try {
        const response = await fetch('/api/iconsService', {
            method: 'POST',
            body: formData, // Attach FormData (multipart/form-data)
        });

        const data = await response.json();
        return data
      } catch (error) {
          console.error('Error uploading image:', error);
      }
    }
  }

  const getLLMsuggestions = async (diagram_services: string[]) => {
    try {
      const response = await fetch('/api/llmService', {
          method: 'POST',
          body: JSON.stringify(diagram_services), // Attach FormData (multipart/form-data)
      });

      const data = await response.json();
      return data
    } catch (error) {
        console.error('Error uploading image:', error);
    }
  }

  const generateAWSTemplate = async (all_services: string[]) => {
    try {
      const response = await fetch('/api/templateService', {
          method: 'POST',
          body: JSON.stringify(all_services), // Attach FormData (multipart/form-data)
      });

      const data = await response.json();
      return data
    } catch (error) {
        console.error('Error uploading image:', error);
    }
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

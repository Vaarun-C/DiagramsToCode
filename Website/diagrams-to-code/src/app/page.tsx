'use client';
import { v4 as uuidv4 } from 'uuid';
import CodeEditor from '@components/CodeEditor';
import FileUploadWrapper from '@components/FileUploadWrapper';
import ParagraphComponent from '@components/ParagraphComponent';

import { useState } from 'react';
import { sendDiagrams } from './api/handler';

export default function Home() {
  const [uploadedFiles, setUploadedFiles] = useState<{ [key: string]: File }>({});
  const [yamlCodes, setYamlCodes] = useState<{ [key: string]: string }>({'':"No template Code Generated"});
  const [selectedUUID, setSelectedUUID] = useState<string>('');

  const handleFilesUploaded = (files: File[]) => {
    const newFiles = Array.from(files).reduce((acc, file) => {
      const uuid = uuidv4();
      acc[uuid] = file;
      return acc;
    }, {} as { [key: string]: File });
    setUploadedFiles((prevFiles) => ({...prevFiles, ...newFiles}));
    console.log(files);
  };

  const handleDeleteFile = (fileUUIDToDelete: string) => {
    setUploadedFiles(prevFiles => {
      const updatedFiles = { ...prevFiles };
      delete updatedFiles[fileUUIDToDelete];
      return updatedFiles;
    });
    if (selectedUUID === fileUUIDToDelete){
      setSelectedUUID('')
    }
  };

  const handleSelectedCard = (newSelectedUUID: string) => {
    setSelectedUUID(newSelectedUUID);
  };

  const onCodeChange = (newCode:string) => {
    setYamlCodes((prevYamlCodes) => ({
      ...prevYamlCodes,
      [selectedUUID]: newCode,
    }));
  };

  const handleUpload = async () => {
    
    if (Object.keys(uploadedFiles).length === 0)
      alert("No Architecture Diagrams have been uploaded")
    else {
      Object.entries(uploadedFiles).forEach(([uuid, file]) => {
        const formData = new FormData();
        formData.append('ArchitectureDiagram', file);
        formData.append('UUID', uuid);

        console.log("BEFORE: ", formData)

        fetch('/api/templateService', {
          method: 'POST',
          body: formData, // Attach FormData (multipart/form-data)
        })
        .then(async (response) => {
          if (!response.ok) {
              throw new Error(`Failed to upload ${file.name}: ${response.statusText}`);
          }
          const data = await response.json();
          const uuid = data.responses[0].uuid
          const template = data.responses[0].template

          const formattedTemplate = Object.entries(template)
          .map(([key, value]) => `${key}: ${value}`)
          .join("");

          // console.log("SLEEP", formattedTemplate)

          setYamlCodes((prevYamlCodes) => ({
            ...prevYamlCodes,
            [uuid]: formattedTemplate,
          }));
          
          console.log(`Upload successful for ${file.name}:`, JSON.stringify(data.message));
          // Show or handle the result here, such as updating the UI
        })
        .catch((error) => {
          console.error(`Error uploading ${file.name}:`, error);
          // Handle the error as needed, e.g., show an alert or update the UI
        });
      });
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

  const generateAWSTemplate = async () => {//(all_services: string[]) => {
    // try {
    //   const response = await fetch('/api/templateService', {
    //       method: 'POST',
    //       body: JSON.stringify(all_services), // Attach FormData (multipart/form-data)
    //   });

    //   const data = await response.json();
    //   return data
    // } catch (error) {
    //     console.error('Error uploading image:', error);
    // }
    const uploadPromises = uploadedFiles.map(async (file) => {
      const formData = new FormData();
      formData.append('Diagram', file);

      try {
          const response = await fetch('/api/service1', {
              method: 'POST',
              body: formData, // Attach FormData (multipart/form-data)
          });
          
          // Ensure you check if the response is ok before parsing
          if (!response.ok) {
              throw new Error(`Failed to upload ${file.name}: ${response.statusText}`);
          }
          
          const data = await response.json();
          return data;
      } catch (error) {
          console.error(`Error uploading ${file.name}:`, error);
          return { error: `Error uploading ${file.name}` }; // Return error info to handle later
      }
    });

    // Wait for all promises to complete and return the results
    const results = await Promise.all(uploadPromises);
    return results;
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
            handleSelectedCard={handleSelectedCard}
          />
        </div>
        <div className='w-1/2 p-4'>
          <CodeEditor code={yamlCodes[selectedUUID] || ''} onCodeChange={onCodeChange}/>
        </div>
      </div>
    </FileUploadWrapper>
  );
}

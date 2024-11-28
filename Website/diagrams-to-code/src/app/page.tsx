'use client';
import { v4 as uuidv4 } from 'uuid';
import CodeEditor from '@components/CodeEditor';
import FileUploadWrapper from '@components/FileUploadWrapper';
import ParagraphComponent from '@components/ParagraphComponent';

import { useState } from 'react';

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

  const sendToCfnDiagService = (template: string) => {
    const formData = new FormData();
    formData.append('GeneratedTemplate', template);
    return fetch('/api/cfnDiag', {
      method: 'POST',
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((result) => {
        console.log('Response from second endpoint:', result);
        return result;
      });
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
          .join("\n");

          setYamlCodes((prevYamlCodes) => ({
            ...prevYamlCodes,
            [uuid]: formattedTemplate,
          }));

          return formattedTemplate
          // console.log(`Upload successful for ${file.name}:`, JSON.stringify(data.message));
          // // Show or handle the result here, such as updating the UI
        })
        .then((template) => {
          console.log(sendToCfnDiagService(template));
        })
        .catch((error) => {
          console.log(`Error uploading ${file.name}:`);
        });
      });
    }
      
  }

  return (
    <FileUploadWrapper onFilesUploaded={handleFilesUploaded}>
      <div className='flex h-screen'>
        {/* Left side of screen */}
        <div className='w-1/2 p-4'>
          {/* Image Input */}
          <div className='h-1/2'>
            <ParagraphComponent
              uploadedFiles={uploadedFiles}
              onFilesUploaded={handleFilesUploaded}
              handleDeleteFile={handleDeleteFile}
              handleUpload={handleUpload}
              handleSelectedCard={handleSelectedCard}
            />
          </div>
          {/* Cfn Graph Display */}
          <div className='h-1/2 bg-white rounded-md border border-gray-300 overflow-hidden'>
          {selectedUUID ? (
            <iframe
              title="Preview"
              src={`/graph/index.html`}
              className="w-full h-full"
            />
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              Select a file to preview
            </div>
          )}
          </div>
        </div>
        {/* Right side of Screen */}
        <div className='w-1/2 p-4'>
          <CodeEditor code={yamlCodes[selectedUUID] || ''} onCodeChange={onCodeChange}/>
        </div>
      </div>
    </FileUploadWrapper>
  );
}

// return (
//   <div className="h-screen grid grid-rows-1 grid-cols-2 gap-4 p-4">
//     {/* Left Panel */}
//     <div className="grid grid-rows-[2fr_1fr] gap-4">
//       {/* Top: Input Section */}
//       <div className="bg-slate-200 rounded-md p-4 overflow-auto">
//         <Paragraph
//           uploadedFiles={uploadedFiles}
//           onFilesUploaded={handleFilesUploaded}
//           handleDeleteFile={handleDeleteFile}
//           handleUpload={() => {
//             console.log('Handle Upload');
//           }}
//           handleSelectedCard={handleSelectedCard}
//           selectedUUID={selectedUUID}
//         />
//       </div>

//       {/* Bottom: Iframe Section */}
      
//     </div>

//     {/* Right Panel: Code Editor */}
//     <div className="bg-white rounded-md border border-gray-300 p-4">
//       <CodeEditor
//         code={yamlCodes[selectedUUID] || ''}
//         onCodeChange={onCodeChange}
//       />
//     </div>
//   </div>
// );
// }
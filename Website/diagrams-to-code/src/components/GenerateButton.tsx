'use client';

import React from 'react';
import { Button } from '@nextui-org/react';
import { VscRunAll } from 'react-icons/vsc';

interface GenerateButtonProps {
  handleUpload: () => void;
}

const GenerateButton: React.FC<GenerateButtonProps> = ({ handleUpload }) => {
  return (
    <Button
      onClick={handleUpload}
      endContent={<VscRunAll />}
      className='flex border-2 items-center gap-2 px-4 py-2 rounded-md transition-all duration-200
      bg-gray-700 text-white hover:bg-green-500 hover:text-black hover:border-gray-700 '
    >
      Generate Templates
    </Button>
  );
};

export default GenerateButton;

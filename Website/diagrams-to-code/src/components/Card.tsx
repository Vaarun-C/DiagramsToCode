'use client';

import React, { useEffect, useState } from 'react';
import Image from 'next/image';

interface CardProps {
  file: File;
}

const Card: React.FC<CardProps> = ({ file }) => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    // Create object URL after component mounts on the client side
    const objectUrl = URL.createObjectURL(file);
    setImageUrl(objectUrl);

    // Clean up the object URL when the component unmounts
    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [file]);

  return (
    <div className='relative w-48 h-48 overflow-hidden rounded-lg shadow-lg cursor-pointer group'>
      {imageUrl && (
        <Image
          src={imageUrl}
          alt={file.name}
          layout='fill'
          objectFit='cover'
          className='transition-transform duration-300 transform group-hover:scale-110'
        />
      )}

      <div className='absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 opacity-0 transition-opacity duration-300 group-hover:opacity-100'>
        <span className='text-white'>{file.name}</span>
      </div>
    </div>
  );
};

export default Card;

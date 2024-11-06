'use client';

import React, { useEffect, useRef, useState } from 'react';
import Image from 'next/image';
import { TiDeleteOutline } from 'react-icons/ti';

interface CardProps {
  file: File;
  onDelete: (file: File) => void;
}

const Card: React.FC<CardProps> = ({ file, onDelete }) => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  // const [hovered, setHovered] = useState(false);
  // const [cardWidth, setCardWidth] = useState<number>(192);
  // const [cardHeight, setCardHeight] = useState<number>(192);

  useEffect(() => {
    // Create object URL after component mounts on the client side
    const objectUrl = URL.createObjectURL(file);
    setImageUrl(objectUrl);

    // Clean up the object URL when the component unmounts
    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [file]);

  const handleImageLoad = (
    event: React.SyntheticEvent<HTMLImageElement, Event>
  ) => {
    const img = event.currentTarget;
    const baseLength = 200;
    // if (img.naturalWidth > img.naturalHeight) {
    //   setCardWidth((baseLength * img.naturalWidth) / img.naturalHeight);
    //   setCardHeight(baseLength);
    // } else {
    //   setCardHeight((baseLength * img.naturalHeight) / img.naturalWidth);
    //   setCardWidth(baseLength);
    // }
    if (containerRef.current) {
      containerRef.current.style.width = `${baseLength*img.naturalWidth / img.naturalHeight}px`;
      containerRef.current.style.height = `${baseLength}px`;
    }
  };

  return (
    <div
      ref={containerRef}
      className={`relative w-5 h-48 overflow-hidden rounded-lg shadow-xl cursor-pointer group `}
      style={{
      //   width: hovered ? cardWidth : '192px', // Initial width, expands on hover
      //   height: hovered ? cardHeight : '192px', // Initial width, expands on hover
        transition: 'width 0.3s ease', // Smooth transition effect
      }}
      // onMouseEnter={() => setHovered(true)}
      // onMouseLeave={() => setHovered(false)}
    >
      {imageUrl && (
        <Image
          src={imageUrl}
          alt={file.name}
          onLoad={handleImageLoad}
          layout='fill'
          objectFit='cover' //{hovered ? 'contain' : 'cover'}
          className='transition-transform duration-300 transform group-hover:scale-110'
        />
      )}

      {/* Overlay with filename on hover */}
      <div className='absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 opacity-0 transition-opacity duration-300 group-hover:opacity-100'>
        <span className='text-white break-words max-w-[90%]'>{file.name}</span>
      </div>

      {/* Delete button, visible on hover */}
      <button
        onClick={() => onDelete(file)}
        className='absolute top-2 left-2  bg-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300'
      >
        <TiDeleteOutline size={25} className='text-red-600' />
      </button>
    </div>
  );
};

export default Card;

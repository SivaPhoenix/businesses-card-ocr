import React from 'react';

const ImageDisplay = ({ src, alt, title }) => (
    <div className="m-4">
        <h2 className="text-xl font-bold mb-2">{title}</h2>
        <img src={src} alt={alt} className="max-w-full h-auto" />
    </div>
);

export default ImageDisplay;

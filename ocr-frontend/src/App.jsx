import React, { useState } from 'react';
import axios from 'axios';
import ImageDisplay from './components/ImageDisplay';
import OCRResultTable from './components/OCRResultTable';
import './index.css';

const App = () => {
    const [file, setFile] = useState(null);
    const [ocrResult, setOcrResult] = useState(null);
    const [originalImage, setOriginalImage] = useState(null);
    const [grayImage, setGrayImage] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append('image', file);

        setLoading(true);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData);
            setOcrResult(response.data.ocr_result);
            setOriginalImage(response.data.original_image_path);
            setGrayImage(response.data.grayscale_image_path);
        } catch (error) {
            console.error('Error uploading the file:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-center text-3xl font-bold mb-4">OCR Business Card Reader</h1>
            <form onSubmit={handleSubmit} className="mb-4">
                <input type="file" onChange={handleFileChange} className="mb-2" />
                <button type="submit" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    {loading ? 'Processing...' : 'Upload'}
                </button>
            </form>
            {originalImage && grayImage && (
                <div className="flex">
                    <ImageDisplay src={`http://localhost:5000${originalImage}`} alt="Original Image" title="Original Image" />
                    <ImageDisplay src={`http://localhost:5000${grayImage}`} alt="Gray Scale Image" title="Gray Scale Image" />
                </div>
            )}
            {ocrResult && <OCRResultTable result={ocrResult} />}
        </div>
    );
};

export default App;

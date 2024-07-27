const express = require('express');
const multer = require('multer');
const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });
//use
app.use(cors());
app.use('/images', express.static(path.join(__dirname, 'images'))); // Serve images statically

// app.post('/upload', upload.single('image'), (req, res) => {
//     const tempPath = path.join(__dirname, 'images', 'temp_image.png');
    
//     fs.writeFile(tempPath, req.file.buffer, (err) => {
//         if (err) {
//             console.error('Failed to save the image:', err);
//             return res.status(500).json({ error: 'Failed to save the image' });
//         }

//         execFile('python', ['ocr.py', tempPath], (error, stdout, stderr) => {
//             if (error) {
//                 console.error('Error executing Python script:', stderr);
//                 return res.status(500).json({ error: stderr });
//             }
//             try {
//                 const result = JSON.parse(stdout);
//                 result.original_image_path = `/images/${path.basename(result.original_image_path)}`;
//                 result.grayscale_image_path = `/images/${path.basename(result.grayscale_image_path)}`;
//                 res.json(result);
//             } catch (parseError) {
//                 console.error('Error parsing JSON output:', parseError);
//                 res.status(500).json({ error: 'Error parsing JSON output' });
//             }
//         });
//     });
// });
app.post('/upload', upload.single('image'), (req, res) => {
    const tempPath = path.join(__dirname, 'images', 'temp_image.png');
    
    fs.writeFile(tempPath, req.file.buffer, (err) => {
        if (err) {
            console.error('Failed to save the image:', err);
            return res.status(500).json({ error: 'Failed to save the image', details: err.message });
        }

        execFile('python', ['ocr.py', tempPath], (error, stdout, stderr) => {
            if (error) {
                console.error('Error executing Python script:', stderr);
                return res.status(500).json({ error: 'Error executing Python script', details: stderr });
            }
            try {
                const result = JSON.parse(stdout);
                result.original_image_path = `/images/${path.basename(result.original_image_path)}`;
                result.grayscale_image_path = `/images/${path.basename(result.grayscale_image_path)}`;
                res.json(result);
            } catch (parseError) {
                console.error('Error parsing JSON output:', parseError);
                res.status(500).json({ error: 'Error parsing JSON output', details: parseError.message });
            }
        });
    });
});



app.listen(5000, () => {
    console.log('Server is running on port 5000');
});

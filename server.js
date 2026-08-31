const express = require('express');
const multer = require('multer');
const cloudinary = require('cloudinary').v2;
const path = require('path');

const app = express();

// Memory Storage: Files direct memory me process hongi (Fast Processing)
const storage = multer.memoryStorage();
const upload = multer({ 
  storage: storage,
  limits: { fileSize: 100 * 1024 * 1024 } // 100MB per file limit
});

cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME || 'zowk74pz',
  api_key: process.env.CLOUDINARY_API_KEY || '684481677341335',
  api_secret: process.env.CLOUDINARY_API_SECRET
});

app.use(express.static(path.join(__dirname, 'public')));

// Memory Buffer se Direct Cloudinary Stream Upload Function
const streamUpload = (fileBuffer, isVideo) => {
  return new Promise((resolve, reject) => {
    const resourceType = isVideo ? 'video' : 'image';
    const stream = cloudinary.uploader.upload_stream(
      { resource_type: resourceType },
      (error, result) => {
        if (result) {
          resolve(result.secure_url);
        } else {
          reject(error);
        }
      }
    );
    stream.end(fileBuffer);
  });
};

// Multiple Files Upload Endpoint (`files` instead of `file`)
app.post('/api/upload', upload.array('files', 20), async (req, res) => {
  try {
    if (!req.files || req.files.length === 0) {
      return res.status(400).json({ error: 'Koi bhi file select nahi ki gayi.' });
    }

    // Promise.all ka use karke saari files EKSATH (Parallelly) upload hongi
    const uploadPromises = req.files.map(file => {
      const isVideo = file.mimetype.startsWith('video');
      return streamUpload(file.buffer, isVideo);
    });

    const urls = await Promise.all(uploadPromises);
    res.json({ urls });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Upload process fail ho gaya.' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server live on port ${PORT}`));

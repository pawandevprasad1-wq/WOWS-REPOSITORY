const express = require('express');
const multer = require('multer');
const cloudinary = require('cloudinary').v2;
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

// Cloudinary Configuration (Environment Variables se credentials uthayega)
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME || 'zowk74pz',
  api_key: process.env.CLOUDINARY_API_KEY || '684481677341335',
  api_secret: process.env.CLOUDINARY_API_SECRET
});

// Static Frontend files serving
app.use(express.static(path.join(__dirname, 'public')));

// Upload Endpoint
app.post('/api/upload', upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'Koi file select nahi ki gayi.' });
    }

    // Auto-detect photo or video
    const resourceType = req.file.mimetype.startsWith('video') ? 'video' : 'image';

    const result = await cloudinary.uploader.upload(req.file.path, {
      resource_type: resourceType
    });

    res.json({ url: result.secure_url });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Upload fail ho gaya.' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});


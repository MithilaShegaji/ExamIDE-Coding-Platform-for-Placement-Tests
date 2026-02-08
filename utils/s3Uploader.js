const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const fs = require('fs');
const path = require('path');

const s3 = new S3Client({
  region: 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
  }
});

async function uploadProfileImage(localFilePath, filename) {
  const fileStream = fs.createReadStream(localFilePath);

  const uploadParams = {
    Bucket: 'Exam-IDEtestbucket',
    Key: `profile/${filename}`,
    Body: fileStream,
    ContentType: 'image/jpeg' // or infer type dynamically
  };

  await s3.send(new PutObjectCommand(uploadParams));

  return `https://Exam-IDEtestbucket.s3.amazonaws.com/profile/${filename}`;
}

module.exports = { uploadProfileImage };

import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { v4 as uuidv4 } from 'uuid';

const accessKeyId = process.env.AWS_ACCESS_KEY_ID
const secretAccessKey = process.env.AWS_SECRET_ACCESS_KEY

const regionName = "eu-central-1"

const config = {
  region: regionName,
  credentials: {
    accessKeyId,
    secretAccessKey,
  },
};

const client = new S3Client(config);
const randomFolderKey = uuidv4();

const uploadFile = async (fileName, fileData) => {
    const bucketName = 'jambo-llama';
    const fileKey = `${randomFolderKey}/${fileName}`

    const input = {
        Bucket: bucketName,     
        Key: fileKey,          
        Body: fileData,     
    };

    const command = new PutObjectCommand(input);
    const response = await client.send(command);

    if(response['$metadata'].httpStatusCode !== 200) {
      return null;
    }
    
    const publicUrl = `https://${bucketName}.s3.${regionName}.amazonaws.com/${fileKey}`;
    return publicUrl;
};

const uploadMultipleFiles = async (files) => {
  const bucketName = 'jambo-llama';
  
  const uploadPromises = files.map(async (fileData) => {
    // Decode base64 JSON into binary data
    const buffer = Buffer.from(fileData, 'base64');
    const fileKey = `${randomFolderKey}/${uuidv4()}`; // Generate unique file name
    
    const input = {
      Bucket: bucketName,
      Key: fileKey,
      Body: buffer,
    };

    const command = new PutObjectCommand(input);
    const response = await client.send(command);

    if (response['$metadata'].httpStatusCode !== 200) {
      return null;
    }

    const publicUrl = `https://${bucketName}.s3.${regionName}.amazonaws.com/${fileKey}`;
    return publicUrl;
  });

  return Promise.all(uploadPromises);
};



export { uploadFile, uploadMultipleFiles };

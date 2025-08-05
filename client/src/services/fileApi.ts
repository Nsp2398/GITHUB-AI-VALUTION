import axios from 'axios';

export interface FileUploadResponse {
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  headers?: string[];
  rows?: any[][];
  paragraphs?: string[];
  tables?: any[][][];
  pages?: {
    page_number: number;
    text: string;
    images: number;
  }[];
  metadata?: Record<string, any>;
  format?: string;
  mode?: string;
  size?: [number, number];
  info?: Record<string, any>;
  error?: string;
}

export const uploadFile = async (file: File): Promise<FileUploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post('/api/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.error || 'Failed to upload file');
    }
    throw new Error('Failed to upload file');
  }
};

export const getFileData = async (filename: string): Promise<FileUploadResponse> => {
  try {
    const response = await axios.get(`/api/files/${filename}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.error || 'Failed to get file data');
    }
    throw new Error('Failed to get file data');
  }
};

import React, { useState, useCallback } from 'react';
import { CloudArrowUpIcon, DocumentIcon, PhotoIcon, XMarkIcon, SparklesIcon } from '@heroicons/react/24/outline';

interface FileUploadProps {
  onFileSelect: (files: File[]) => void;
  acceptedTypes?: string[];
  maxFiles?: number;
  maxSize?: number; // in bytes
  className?: string;
}

interface UploadedFile {
  file: File;
  id: string;
  preview?: string;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  acceptedTypes = [
    'text/plain',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ],
  maxFiles = 5,
  maxSize = 16 * 1024 * 1024, // 16MB
  className = ''
}) => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const [errors, setErrors] = useState<string[]>([]);

  const validateFile = (file: File): string | null => {
    if (!acceptedTypes.includes(file.type)) {
      return `File type ${file.type} is not supported`;
    }
    if (file.size > maxSize) {
      return `File size must be less than ${formatFileSize(maxSize)}`;
    }
    return null;
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (fileType: string) => {
    if (fileType.startsWith('image/')) {
      return <PhotoIcon className="h-8 w-8 text-blue-500" />;
    }
    return <DocumentIcon className="h-8 w-8 text-gray-500" />;
  };

  const getFileTypeLabel = (fileType: string): string => {
    const typeMap: { [key: string]: string } = {
      'text/plain': 'Text',
      'application/pdf': 'PDF',
      'application/msword': 'Word',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word',
      'image/jpeg': 'JPEG Image',
      'image/png': 'PNG Image',
      'image/gif': 'GIF Image',
      'image/webp': 'WebP Image',
      'application/vnd.ms-excel': 'Excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Excel'
    };
    return typeMap[fileType] || 'Unknown';
  };

  const processFiles = useCallback((files: FileList | File[]) => {
    const fileArray = Array.from(files);
    const newErrors: string[] = [];
    const validFiles: File[] = [];

    if (uploadedFiles.length + fileArray.length > maxFiles) {
      newErrors.push(`Maximum ${maxFiles} files allowed`);
      setErrors(newErrors);
      return;
    }

    fileArray.forEach((file) => {
      const error = validateFile(file);
      if (error) {
        newErrors.push(`${file.name}: ${error}`);
      } else {
        validFiles.push(file);
      }
    });

    if (newErrors.length > 0) {
      setErrors(newErrors);
    } else {
      setErrors([]);
    }

    if (validFiles.length > 0) {
      const newUploadedFiles: UploadedFile[] = validFiles.map((file) => ({
        file,
        id: Math.random().toString(36).substr(2, 9),
        preview: file.type.startsWith('image/') ? URL.createObjectURL(file) : undefined
      }));

      const updatedFiles = [...uploadedFiles, ...newUploadedFiles];
      setUploadedFiles(updatedFiles);
      onFileSelect(updatedFiles.map(f => f.file));
    }
  }, [uploadedFiles, maxFiles, onFileSelect, validateFile, formatFileSize]);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFiles(e.dataTransfer.files);
    }
  }, [processFiles]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFiles(e.target.files);
    }
  }, [processFiles]);

  const removeFile = (id: string) => {
    const updatedFiles = uploadedFiles.filter(f => f.id !== id);
    setUploadedFiles(updatedFiles);
    onFileSelect(updatedFiles.map(f => f.file));
    
    // Revoke object URLs to prevent memory leaks
    const fileToRemove = uploadedFiles.find(f => f.id === id);
    if (fileToRemove?.preview) {
      URL.revokeObjectURL(fileToRemove.preview);
    }
  };

  const clearAllFiles = () => {
    uploadedFiles.forEach(file => {
      if (file.preview) {
        URL.revokeObjectURL(file.preview);
      }
    });
    setUploadedFiles([]);
    onFileSelect([]);
    setErrors([]);
  };

  return (
    <div className={`w-full ${className}`}>
      <div
        className={`relative border-2 border-dashed rounded-3xl p-8 transition-all duration-300 backdrop-blur-sm ${
          dragActive
            ? 'border-blue-500 bg-blue-50/60 shadow-neon animate-pulse-neon'
            : 'border-gray-300 hover:border-blue-400 bg-white/50 hover:bg-white/70'
        } ${uploadedFiles.length > 0 ? 'bg-gradient-to-br from-green-50/50 to-blue-50/50' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          multiple
          accept={acceptedTypes.join(',')}
          onChange={handleChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        
        <div className="text-center space-y-4">
          <div className="mx-auto h-20 w-20 flex items-center justify-center rounded-3xl bg-gradient-to-br from-blue-600 to-purple-600 shadow-glow animate-float">
            <CloudArrowUpIcon className="h-10 w-10 text-white" />
          </div>
          
          <div>
            <p className="text-xl font-bold text-gray-900 mb-2">
              {dragActive ? '✨ Drop files here' : '📁 Upload Documents'}
            </p>
            <p className="text-sm text-gray-600 font-medium">
              {dragActive 
                ? 'Release to upload your files' 
                : 'Drag and drop files here, or click to browse'
              }
            </p>
            <p className="text-xs text-gray-500 mt-2">
              Max {maxFiles} files • {formatFileSize(maxSize)} each
            </p>
          </div>
          
          {/* Enhanced file type indicators */}
          <div className="flex justify-center space-x-6 text-xs text-gray-500">
            <div className="flex items-center space-x-2 bg-white/60 backdrop-blur-sm rounded-lg px-3 py-2">
              <DocumentIcon className="h-4 w-4 text-red-500" />
              <span>PDF, DOC</span>
            </div>
            <div className="flex items-center space-x-2 bg-white/60 backdrop-blur-sm rounded-lg px-3 py-2">
              <PhotoIcon className="h-4 w-4 text-green-500" />
              <span>Images</span>
            </div>
            <div className="flex items-center space-x-2 bg-white/60 backdrop-blur-sm rounded-lg px-3 py-2">
              <SparklesIcon className="h-4 w-4 text-blue-500" />
              <span>Excel, TXT</span>
            </div>
          </div>
        </div>
      </div>

      {/* Error Messages */}
      {errors.length > 0 && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <div className="text-sm text-red-600">
            {errors.map((error, index) => (
              <div key={index}>{error}</div>
            ))}
          </div>
        </div>
      )}

      {/* Enhanced Uploaded Files Display */}
      {uploadedFiles.length > 0 && (
        <div className="mt-8 animate-slide-up">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-lg font-bold text-gray-900 flex items-center">
              <SparklesIcon className="h-5 w-5 mr-2 text-green-500" />
              Uploaded Files ({uploadedFiles.length})
            </h4>
            <button
              onClick={clearAllFiles}
              className="text-sm font-medium text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 px-3 py-1 rounded-lg transition-colors"
            >
              Clear All
            </button>
          </div>
          
          <div className="grid gap-3">
            {uploadedFiles.map((uploadedFile, index) => (
              <div
                key={uploadedFile.id}
                className="flex items-center p-4 bg-white/70 backdrop-blur-sm rounded-2xl border border-white/30 shadow-lg hover:shadow-xl transition-all duration-200 animate-scale-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="flex-shrink-0 mr-4">
                  {uploadedFile.preview ? (
                    <img
                      src={uploadedFile.preview}
                      alt={uploadedFile.file.name}
                      className="h-12 w-12 object-cover rounded-xl shadow-md"
                    />
                  ) : (
                    <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-md">
                      {getFileIcon(uploadedFile.file.type)}
                    </div>
                  )}
                </div>
                <div className="ml-3 flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {uploadedFile.file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {getFileTypeLabel(uploadedFile.file.type)} • {formatFileSize(uploadedFile.file.size)}
                  </p>
                </div>
                
                <button
                  onClick={() => removeFile(uploadedFile.id)}
                  className="ml-3 text-gray-400 hover:text-gray-600"
                >
                  <XMarkIcon className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

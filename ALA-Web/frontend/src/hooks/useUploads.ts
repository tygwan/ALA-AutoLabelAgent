import { useState, useEffect } from 'react';
import axios from 'axios';

interface UploadedFile {
    file_id: string;
    filename: string;
    file_type: 'image' | 'video';
    size: number;
    uploaded_at: string;
}

const API_URL = 'http://localhost:8000';

export const useUploads = () => {
    const [files, setFiles] = useState<UploadedFile[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchFiles = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${API_URL}/api/upload/list`);
            setFiles(response.data.files);
            setError(null);
        } catch (err) {
            setError('Failed to fetch files');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const uploadFile = async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);

        try {
            await axios.post(`${API_URL}/api/upload/file`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            await fetchFiles(); // Refresh list
        } catch (err) {
            console.error('Upload failed:', err);
            throw err;
        }
    };

    const uploadBatch = async (files: FileList) => {
        const formData = new FormData();
        Array.from(files).forEach(file => {
            formData.append('files', file);
        });

        try {
            await axios.post(`${API_URL}/api/upload/batch`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            await fetchFiles(); // Refresh list
        } catch (err) {
            console.error('Batch upload failed:', err);
            throw err;
        }
    };

    const deleteFile = async (fileId: string) => {
        try {
            await axios.delete(`${API_URL}/api/upload/${fileId}`);
            await fetchFiles(); // Refresh list
        } catch (err) {
            console.error('Delete failed:', err);
            throw err;
        }
    };

    useEffect(() => {
        fetchFiles();
    }, []);

    return {
        files,
        loading,
        error,
        uploadFile,
        uploadBatch,
        deleteFile,
        refreshFiles: fetchFiles
    };
};

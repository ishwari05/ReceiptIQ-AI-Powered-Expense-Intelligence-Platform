import React, { useState } from 'react';
import { UploadCloud, FileText, Loader2, CheckCircle2, AlertCircle, ArrowLeft, ArrowRight } from 'lucide-react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function Upload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected && (selected.type.startsWith('image/') || selected.type === 'application/pdf')) {
      setFile(selected);
      setError('');
    } else {
      setError('Please select a valid image or PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/receipts/upload_receipt', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process receipt. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <button 
        onClick={() => navigate('/')}
        className="flex items-center gap-2 text-gray-500 hover:text-gray-900 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </button>

      <div>
        <h1 className="text-3xl font-bold text-gray-900">Upload Receipt</h1>
        <p className="text-gray-500 mt-1">Our AI will automatically extract the details</p>
      </div>

      <div className="space-y-6">
        {!result ? (
          <div className="card">
            <div 
              className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
                file ? 'border-primary-500 bg-primary-50' : 'border-gray-200 hover:border-primary-400'
              }`}
            >
              <input 
                type="file" 
                id="receipt-upload" 
                className="hidden" 
                accept="image/*,.pdf"
                onChange={handleFileChange}
              />
              <label htmlFor="receipt-upload" className="cursor-pointer">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-white shadow-sm rounded-full mb-4">
                  <UploadCloud className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {file ? file.name : 'Click to upload receipt'}
                </h3>
                <p className="text-gray-500 mt-1">Supports JPG, PNG, WEBP and PDF</p>
              </label>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-lg flex items-center gap-3 border border-red-100">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <p className="text-sm">{error}</p>
              </div>
            )}

            <button 
              onClick={handleUpload}
              disabled={!file || uploading}
              className="btn-primary w-full mt-6 h-12 flex items-center justify-center gap-2"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing with AI...
                </>
              ) : (
                'Extract Details'
              )}
            </button>
          </div>
        ) : (
          <div className="card animate-in fade-in duration-500">
            <div className="flex items-center justify-center w-16 h-16 bg-green-100 text-green-600 rounded-full mx-auto mb-6">
              <CheckCircle2 className="w-10 h-10" />
            </div>
            <h2 className="text-2xl font-bold text-center text-gray-900">Extraction Complete!</h2>
            <p className="text-gray-500 text-center mt-1">Review the details below</p>

            <div className="mt-8 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500 font-medium uppercase">Vendor</p>
                  <p className="text-lg font-bold text-gray-900">{result.vendor || 'Unknown'}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500 font-medium uppercase">Amount</p>
                  <p className="text-lg font-bold text-gray-900">${result.amount?.toFixed(2)}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500 font-medium uppercase">Date</p>
                  <p className="text-lg font-bold text-gray-900">
                    {result.date ? new Date(result.date).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500 font-medium uppercase">Status</p>
                  <p className="text-lg font-bold text-green-600 capitalize">{result.status}</p>
                </div>
              </div>
            </div>

            <div className="mt-8 flex gap-4">
              <button 
                onClick={() => setResult(null)}
                className="flex-1 px-4 py-3 border border-gray-200 rounded-lg font-medium hover:bg-gray-50 transition-all"
              >
                Upload Another
              </button>
              <button 
                onClick={() => navigate('/')}
                className="btn-primary flex-1 flex items-center justify-center gap-2"
              >
                Go to Dashboard
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

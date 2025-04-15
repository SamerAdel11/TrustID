import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { FaCloudUploadAlt } from "react-icons/fa"; // Download/Upload icon

const UploadSection = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    setUploading(true);

    const formData = new FormData();
    formData.append("file", selectedFiles[0]); // 'file' is the key to send in the request

    try {
      const response = await fetch("YOUR_API_ENDPOINT", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setUploadSuccess(true);
        console.log("File uploaded successfully!");
      } else {
        throw new Error("File upload failed");
      }
    } catch (err) {
      console.error("Error uploading file:", err);
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const onDrop = useCallback((acceptedFiles) => {
    console.log("Dropped files:", acceptedFiles);
    setSelectedFiles(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
  });

  return (
    <div className="upload-section container bg-white mt-4 rounded-3 p-4">
      <h5 className="fw-bold mb-3">Upload ID Card</h5>

      <div
        {...getRootProps()}
        className="upload-area border border-2 rounded-3 p-5 text-center text-muted"
        style={{ cursor: "pointer" }}
      >
        <input {...getInputProps()} />


        {isDragActive ? (
          <>
            <FaCloudUploadAlt size={60} className="text-secondary mb-3" />
            <p className="fw-bold text-primary">Drop the file here...</p>
          </>
        ) : selectedFiles.length > 0 ? (
          <p className="fw-bold text-primary">
             {selectedFiles[0].name}
          </p>
        ) : (
          <>
            <FaCloudUploadAlt size={60} className="text-secondary mb-3" />
            <p className="text-muted">
              <strong>Choose a file</strong> or drag it here
            </p>
          </>
        )}
      </div>

      <button className="extract-btn mt-3" type="submit">Extract Text</button>
      <p className="text-muted small mt-2">
        Supported formats: JPG, PNG, PDF. Please upload clear images for better accuracy.
      </p>
    </div>
  );
};

export default UploadSection;

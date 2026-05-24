import { useState } from "react"
import axios from "axios"

function ResumeUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState("")
  const [statusType, setStatusType] = useState("") // "success" | "error" | ""
  const [uploading, setUploading] = useState(false)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
    setStatus("")
    setStatusType("")
  }

  const handleUpload = async () => {
    if (!file) {
      setStatus("Please select a PDF first.")
      setStatusType("error")
      return
    }

    const formData = new FormData()
    formData.append("file", file)

    setUploading(true)
    setStatus("Uploading and indexing your resume...")
    setStatusType("")

    try {
      const res = await axios.post(
        `${import.meta.env.VITE_API_URL}/resume/upload`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      )
      setStatus(`✓ ${res.data.filename} uploaded successfully`)
      setStatusType("success")
      if (onUploadSuccess) onUploadSuccess()
    } catch (err) {
      setStatus(`Upload failed: ${err.message}`)
      setStatusType("error")
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-semibold">
          1
        </span>
        <h2 className="text-xl font-semibold text-slate-800">Upload Resume</h2>
      </div>

      <div className="flex flex-col sm:flex-row gap-3">
        <label className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 border-2 border-dashed border-slate-300 rounded-lg cursor-pointer hover:border-blue-400 hover:bg-blue-50 transition">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className="hidden"
          />
          <span className="text-slate-600">
            {file ? file.name : "Choose PDF file"}
          </span>
        </label>

        <button
          onClick={handleUpload}
          disabled={uploading || !file}
          className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-medium rounded-lg transition disabled:bg-slate-300 disabled:cursor-not-allowed"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </div>

      {status && (
        <p
          className={`mt-3 text-sm ${
            statusType === "success"
              ? "text-green-600"
              : statusType === "error"
              ? "text-red-600"
              : "text-slate-500"
          }`}
        >
          {status}
        </p>
      )}
    </div>
  )
}

export default ResumeUpload
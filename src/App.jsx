function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#0f172a",
        color: "white",
        fontFamily: "Arial",
      }}
    >
      <h1 style={{ fontSize: "48px", marginBottom: "10px" }}>
        InterviewIQ
      </h1>

      <p style={{ fontSize: "20px", marginBottom: "30px" }}>
        AI-powered interview preparation platform
      </p>

      <button
        style={{
          padding: "12px 24px",
          fontSize: "18px",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          backgroundColor: "#3b82f6",
          color: "white",
        }}
      >
        Upload Resume
      </button>
    </div>
  )
}

export default App
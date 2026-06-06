from app.services.rag_service import build_index_from_pdf

# Test with the exact filename that failed in the browser
filename = "uploads/Resume - D (1).pdf"
print(f"Testing with: {filename}")

try:
    result = build_index_from_pdf(filename)
    print(f"SUCCESS — chunks indexed: {result}")
except Exception as e:
    import traceback
    print("ERROR OCCURRED:")
    traceback.print_exc()
    
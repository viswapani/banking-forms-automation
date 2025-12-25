document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("file-input");
  const uploadStatus = document.getElementById("upload-status");
  const resultSection = document.getElementById("result-section");
  const ackIdSpan = document.getElementById("ack-id");
  const formTypeSpan = document.getElementById("form-type");
  const formStatusSpan = document.getElementById("form-status");
  const missingFieldsSpan = document.getElementById("missing-fields");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    if (!fileInput.files || fileInput.files.length === 0) {
      uploadStatus.textContent = "Please choose a file to upload.";
      uploadStatus.className = "status error";
      return;
    }

    const file = fileInput.files[0];
    uploadStatus.textContent = "Uploading and processing...";
    uploadStatus.className = "status info";
    resultSection.style.display = "none";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const detail = errorData.detail || `Error ${response.status}`;
        uploadStatus.textContent = `Upload failed: ${detail}`;
        uploadStatus.className = "status error";
        return;
      }

      const data = await response.json();

      uploadStatus.textContent = "Upload and processing completed.";
      uploadStatus.className = "status success";

      ackIdSpan.textContent = data.acknowledgment_id || "-";
      formTypeSpan.textContent = data.form_type || "-";
      formStatusSpan.textContent = data.status || "-";

      if (Array.isArray(data.missing_fields) && data.missing_fields.length > 0) {
        missingFieldsSpan.textContent = data.missing_fields.join(", ");
      } else {
        missingFieldsSpan.textContent = "None";
      }

      resultSection.style.display = "block";
    } catch (err) {
      console.error(err);
      uploadStatus.textContent = "Unexpected error during upload.";
      uploadStatus.className = "status error";
    }
  });
});
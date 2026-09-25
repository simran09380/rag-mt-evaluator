const API_BASE_URL = "http://127.0.0.1:8000";

export async function evaluateTranslation({
  source,
  hypothesis,
  reference,
  sourceLang,
  targetLang,
  domain,
}) {
  const formData = new FormData();

  formData.append("source", source);
  formData.append("hypothesis", hypothesis);

  if (reference) {
    formData.append("reference", reference);
  }

  if (sourceLang) {
    formData.append("source_lang", sourceLang);
  }

  if (targetLang) {
    formData.append("target_lang", targetLang);
  }

  if (domain) {
    formData.append("domain", domain);
  }

  const response = await fetch(`${API_BASE_URL}/evaluate/`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `Evaluation failed (${response.status}): ${errorText}`
    );
  }

  return await response.json();
}


export async function evaluateDataset({
  file,
  sourceLang = "en",
  targetLang = "hi",
  domain = "General",
}) {
  const formData = new FormData();

  formData.append("file", file);

  formData.append("source_lang", sourceLang);
  formData.append("target_lang", targetLang);
  formData.append("domain", domain);

  const response = await fetch(
    "http://127.0.0.1:8000/evaluate/",
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `Dataset evaluation failed (${response.status}): ${errorText}`
    );
  }

  return await response.json();
}
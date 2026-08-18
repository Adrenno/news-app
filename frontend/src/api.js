const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

export async function getLatestDigest() {
  const response = await fetch(
    `${API_BASE_URL}/api/digests/latest`
  );

  if (!response.ok) {
    throw new Error("Failed to load latest digest.");
  }

  return response.json();
}

export async function getWhyItMatters(articleId) {
  const response = await fetch(
    `${API_BASE_URL}/api/articles/${articleId}/why-it-matters`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Failed to generate explanation."
    );
  }

  return response.json();
}

export async function getDigests(limit = 20, offset = 0) {
  const response = await fetch(
    `${API_BASE_URL}/api/digests?limit=${limit}&offset=${offset}`
  );

  if (!response.ok) {
    throw new Error("Failed to load digests.");
  }

  return response.json();
}

export async function getArticles({
  limit = 20,
  offset = 0,
  category = "",
  source = "",
  search = "",
  is_read,
} = {}) {
  const params = new URLSearchParams();

  params.set("limit", limit);
  params.set("offset", offset);

  if (category) {
    params.set("category", category);
  }

  if (source) {
    params.set("source", source);
  }

  if (search) {
    params.set("search", search);
  }

  if (is_read !== undefined) {
    params.set("is_read", is_read);
  }

  const response = await fetch(
    `${API_BASE_URL}/api/articles?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch articles.");
  }

  return response.json();
}

export async function setArticleReadStatus(
  articleId,
  isRead
) {
  const response = await fetch(
    `${API_BASE_URL}/api/articles/${articleId}/read?is_read=${isRead}`,
    {
      method: "PATCH",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Could not update article read status."
    );
  }

  return response.json();
}
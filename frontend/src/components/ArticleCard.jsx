function ArticleCard({
  article,
  whyItMatters,
  loadingWhy,
  whyError,
  onWhyItMatters,
  onReadStatus
}) {
  const explanationShown = Boolean(
    whyItMatters[article.id]
  );

  const explanationLoading = Boolean(
    loadingWhy[article.id]
  );

  return (
    <article
      className={
        article.is_read
          ? "article-card read"
          : "article-card"
      }
    >
      <div className="article-meta">
        <span className="article-source">
          {article.source}
        </span>

        <span className="article-category">
          {article.category}
        </span>

        {article.published && (
          <span className="article-date">
            {new Date(
              article.published
            ).toLocaleDateString()}
          </span>
        )}
      </div>

      <h3>{article.title}</h3>

      <p className="article-summary">
        {article.summary}
      </p>

      <div className="article-actions">
        <button
          type="button"
          className="read-button"
          onClick={() =>
            onReadStatus(
              article.id,
              !Boolean(article.is_read)
            )
          }
        >
          {article.is_read
            ? "Mark as unread"
            : "Mark as read"}
        </button>
        
        <button
          type="button"
          className={
            explanationShown
              ? "why-button shown"
              : "why-button"
          }
          onClick={() =>
            onWhyItMatters(article.id)
          }
          disabled={
            explanationLoading ||
            explanationShown
          }
        >
          <span className="why-button-icon">
            ✦
          </span>

          {explanationLoading
            ? "Thinking..."
            : explanationShown
              ? "Explanation shown"
              : "Why does this matter?"}
        </button>

        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
        >
          Read article →
        </a>
      </div>

      {explanationShown && (
        <div className="why-it-matters">
          <strong>Why it matters</strong>

          <p>
            {whyItMatters[article.id]}
          </p>
        </div>
      )}

      {whyError[article.id] && (
        <p className="why-error">
          {whyError[article.id]}
        </p>
      )}
    </article>
  );
}

export default ArticleCard;
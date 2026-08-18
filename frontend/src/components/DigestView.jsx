import ArticleCard from "./ArticleCard";
import DigestHistory from "./DigestHistory";

function DigestView({
  isLatestDigest,
  digest,
  digests,
  loadingDigests,
  selectedDigestId,
  onSelectDigest,
  category,
  source,
  setCategory,
  setSource,
  categories,
  sources,
  whyItMatters,
  loadingWhy,
  whyError,
  onWhyItMatters,
  onReadStatus,
}) {
  const filteredArticles = digest
    ? digest.articles.filter((article) => {
        const matchesCategory =
          !category || article.category === category;

        const matchesSource =
          !source || article.source === source;

        return matchesCategory && matchesSource;
      })
    : [];

  return (
    <>
      <section className="digest-header">
        <div>
          <p className="eyebrow">
            {isLatestDigest
              ? "LATEST DIGEST"
              : "ARCHIVED DIGEST"}
          </p>

          <h2>
            {isLatestDigest
              ? "Today's News"
              : `Digest #${digest.id}`}
          </h2>
        </div>

        {digest && (
          <span className="digest-status">
            Created {digest.created_at}
          </span>
        )}
      </section>

      <div className="content-layout">
        <DigestHistory
          digests={digests}
          loading={loadingDigests}
          selectedDigestId={selectedDigestId}
          onSelectDigest={onSelectDigest}
        />

        <section className="article-content">
          <div className="article-filters">
            <div>
              <label htmlFor="category-filter">
                Category
              </label>

              <select
                id="category-filter"
                value={category}
                onChange={(event) =>
                  setCategory(event.target.value)
                }
              >
                <option value="">
                  All categories
                </option>

                {categories.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="source-filter">
                Source
              </label>

              <select
                id="source-filter"
                value={source}
                onChange={(event) =>
                  setSource(event.target.value)
                }
              >
                <option value="">
                  All sources
                </option>

                {sources.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </div>

            {(category || source) && (
              <button
                type="button"
                onClick={() => {
                  setCategory("");
                  setSource("");
                }}
              >
                Clear filters
              </button>
            )}
          </div>

          <section className="articles">
            {filteredArticles.map((article) => (
              <ArticleCard
                key={article.id}
                article={article}
                whyItMatters={whyItMatters}
                loadingWhy={loadingWhy}
                whyError={whyError}
                onWhyItMatters={onWhyItMatters}
                onReadStatus={onReadStatus}
              />
            ))}
          </section>
        </section>
      </div>
    </>
  );
}

export default DigestView;
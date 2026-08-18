import ArticleCard from "./ArticleCard";

function ExploreView({
  exploreCategory,
  exploreSource,
  setExploreCategory,
  setExploreSource,
  exploreCategories,
  exploreSources,
  activeSearch,
  articleSearch,
  setArticleSearch,
  setActiveSearch,
  setArticleOffset,
  loadingArticles,
  articlesError,
  allArticles,
  whyItMatters,
  loadingWhy,
  whyError,
  onWhyItMatters,
  articleOffset,
  articleLimit,
  hasMoreArticles,
  onReadStatus,
  exploreReadFilter,
  setExploreReadFilter,
}) {
  return (
    <section className="explore">
      <section className="digest-header">
        <div>
          <p className="eyebrow">EXPLORE</p>
          <h2>All Articles</h2>
        </div>
      </section>

      <div className="article-filters explore-filters">
        <div>
          <label htmlFor="explore-category-filter">
            Category
          </label>

          <select
            id="explore-category-filter"
            value={exploreCategory}
            onChange={(event) =>
              setExploreCategory(event.target.value)
            }
          >
            <option value="">
              All categories
            </option>

            {exploreCategories.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="explore-source-filter">
            Source
          </label>

          <select
            id="explore-source-filter"
            value={exploreSource}
            onChange={(event) =>
              setExploreSource(event.target.value)
            }
          >
            <option value="">
              All sources
            </option>

            {exploreSources.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>

        {(exploreCategory || exploreSource) && (
          <button
            type="button"
            onClick={() => {
              setExploreCategory("");
              setExploreSource("");
              setArticleOffset(0);
            }}
          >
            Clear filters
          </button>
        )}
      </div>

      <div className="read-filter">
        <span>Reading status</span>

        <div className="read-filter-buttons">
          <button
            type="button"
            className={
              exploreReadFilter === ""
                ? "active"
                : ""
            }
            onClick={() => {
              setExploreReadFilter("");
              setArticleOffset(0);
            }}
          >
            All
          </button>

          <button
            type="button"
            className={
              exploreReadFilter === "unread"
                ? "active"
                : ""
            }
            onClick={() => {
              setExploreReadFilter("unread");
              setArticleOffset(0);
            }}
          >
            Unread
          </button>

          <button
            type="button"
            className={
              exploreReadFilter === "read"
                ? "active"
                : ""
            }
            onClick={() => {
              setExploreReadFilter("read");
              setArticleOffset(0);
            }}
          >
            Read
          </button>
        </div>
      </div>

      <div className="explore-summary">
        {activeSearch ? (
          <p>
            Results for <strong>"{activeSearch}"</strong>
          </p>
        ) : (
          <p>All articles</p>
        )}

        {(exploreCategory || exploreSource) && (
          <div className="explore-active-filters">
            {exploreCategory && (
              <span>
                Category: {exploreCategory}
              </span>
            )}

            {exploreSource && (
              <span>
                Source: {exploreSource}
              </span>
            )}
          </div>
        )}
      </div>

      <div className="explore-search">
        <input
          type="text"
          value={articleSearch}
          onChange={(event) =>
            setArticleSearch(event.target.value)
          }
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              setArticleOffset(0);
              setActiveSearch(articleSearch);
            }
          }}
          placeholder="Search articles..."
        />

        <button
          type="button"
          onClick={() => {
            setArticleOffset(0);
            setActiveSearch(articleSearch);
          }}
        >
          Search
        </button>

        {activeSearch && (
          <button
            type="button"
            onClick={() => {
              setArticleSearch("");
              setArticleOffset(0);
              setActiveSearch("");
            }}
          >
            Clear
          </button>
        )}
      </div>

      {loadingArticles && (
        <p>Loading articles...</p>
      )}

      {articlesError && (
        <p>
          Could not load articles: {articlesError}
        </p>
      )}

      {!loadingArticles &&
        !articlesError &&
        allArticles.length === 0 && (
          <div className="empty-state">
            <h3>No articles found</h3>

            {activeSearch ? (
              <p>
                No articles matched "{activeSearch}".
                Try a different search term.
              </p>
            ) : (
              <p>
                There are no articles available right now.
              </p>
            )}
          </div>
        )}

      {!loadingArticles &&
        !articlesError &&
        allArticles.length > 0 && (
          <section className="articles">
            {allArticles.map((article) => (
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
        )}

      <div className="pagination">
        <button
          type="button"
          onClick={() => {
            setArticleOffset(
              Math.max(
                0,
                articleOffset - articleLimit
              )
            );
          }}
          disabled={
            articleOffset === 0 ||
            loadingArticles
          }
        >
          Previous
        </button>

        <span>
          Page{" "}
          {Math.floor(
            articleOffset / articleLimit
          ) + 1}
        </span>

        <button
          type="button"
          onClick={() => {
            setArticleOffset(
              articleOffset + articleLimit
            );
          }}
          disabled={
            !hasMoreArticles ||
            loadingArticles
          }
        >
          Next
        </button>
      </div>
    </section>
  );
}

export default ExploreView;
import { useEffect, useState } from "react";
import "./App.css";
import {
  getLatestDigest,
  getWhyItMatters,
  getDigests,
  getArticles,
  setArticleReadStatus,
} from "./api";
import DigestView from "./components/DigestView";
import ExploreView from "./components/ExploreView";

function App() {
  const [category, setCategory] = useState("");
  const [source, setSource] = useState("");

  const [digest, setDigest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [digests, setDigests] = useState([]);
  const [loadingDigests, setLoadingDigests] = useState(true);
  const [selectedDigestId, setSelectedDigestId] = useState(null);

  const [whyItMatters, setWhyItMatters] = useState({});
  const [loadingWhy, setLoadingWhy] = useState({});
  const [whyError, setWhyError] = useState({});

  const [view, setView] = useState("digest");

  const [allArticles, setAllArticles] = useState([]);
  const [loadingArticles, setLoadingArticles] = useState(false);
  const [articlesError, setArticlesError] = useState(null);

  const [exploreCategory, setExploreCategory] = useState("");
  const [exploreSource, setExploreSource] = useState("");
  const [exploreReadFilter, setExploreReadFilter] =
  useState("");

  const [articleSearch, setArticleSearch] = useState("");
  const [activeSearch, setActiveSearch] = useState("");

  const [articleOffset, setArticleOffset] = useState(0);
  const articleLimit = 20;
  const [hasMoreArticles, setHasMoreArticles] = useState(false);

  const [readStatus, setReadStatus] = useState({});

  const exploreCategories = [
    ...new Set(
      allArticles.map((article) => article.category)
    ),
  ].sort();

  const exploreSources = [
    ...new Set(
      allArticles.map((article) => article.source)
    ),
  ].sort();

  async function handleWhyItMatters(articleId) {
    if (whyItMatters[articleId]) {
      return;
    }
    setLoadingWhy((previous) => ({
      ...previous,
      [articleId]: true,
    }));

    setWhyError((previous) => ({
      ...previous,
      [articleId]: null,
    }));

    try {
      const data = await getWhyItMatters(articleId);

      setWhyItMatters((previous) => ({
        ...previous,
        [articleId]: data.why_it_matters,
      }));

      setTimeout(() => {
        setWhyItMatters((previous) => {
          const updated = { ...previous };

          delete updated[articleId];

          return updated;
        });
      }, 10000);
    } catch (error) {
      setWhyError((previous) => ({
        ...previous,
        [articleId]: error.message,
      }));
    } finally {
      setLoadingWhy((previous) => ({
        ...previous,
        [articleId]: false,
      }));
    }
  }

  async function handleReadStatus(
    articleId,
    isRead
  ) {
    try {
      await setArticleReadStatus(
        articleId,
        isRead
      );

      setDigest((previous) => {
        if (!previous) {
          return previous;
        }

        return {
          ...previous,
          articles: previous.articles.map(
            (article) =>
              article.id === articleId
                ? {
                    ...article,
                    is_read: isRead ? 1 : 0,
                  }
                : article
          ),
        };
      });

      setDigests((previous) =>
        previous.map((item) => ({
          ...item,
          articles: item.articles.map(
            (article) =>
              article.id === articleId
                ? {
                    ...article,
                    is_read: isRead ? 1 : 0,
                  }
                : article
          ),
        }))
      );

      setAllArticles((previous) =>
        previous.map((article) =>
          article.id === articleId
            ? {
                ...article,
                is_read: isRead ? 1 : 0,
              }
            : article
        )
      );
    } catch (error) {
      console.error(
        "Could not update article read status:",
        error
      );
    }
  }

  useEffect(() => {
    async function loadDigest() {
      try {
        const data = await getLatestDigest();

        setDigest(data.digest);

        if (data.digest) {
          setSelectedDigestId(data.digest.id);
        }
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    async function loadDigests() {
      try {
        const data = await getDigests();

        setDigests(data.digests);
      } catch (error) {
        console.error(
          "Could not load digest history:",
          error
        );
      } finally {
        setLoadingDigests(false);
      }
    }

    loadDigest();
    loadDigests();
  }, []);

  useEffect(() => {
    if (view !== "explore") {
      return;
    }

    async function loadArticles() {
      setLoadingArticles(true);
      setArticlesError(null);

      try {
        const data = await getArticles({
          category: exploreCategory,
          source: exploreSource,
          search: activeSearch,
          is_read:
            exploreReadFilter === ""
              ? undefined
              : exploreReadFilter === "read",
          limit: articleLimit,
          offset: articleOffset,
        });

        setAllArticles(data.articles);
        setHasMoreArticles(data.articles.length === articleLimit);
      } catch (error) {
        setArticlesError(error.message);
      } finally {
        setLoadingArticles(false);
      }
    }

    loadArticles();
  }, [
    view,
    exploreCategory,
    exploreSource,
    exploreReadFilter,
    activeSearch,
    articleOffset,
    articleLimit,
  ]);

  const isLatestDigest =
    digest && digests.length > 0
      ? digest.id === digests[0].id
      : false;
  const digestCategories = digest
    ? [
        ...new Set(
          digest.articles.map(
            (article) => article.category
          )
        ),
      ].sort()
    : [];

  const digestSources = digest
    ? [
        ...new Set(
          digest.articles.map(
            (article) => article.source
          )
        ),
      ].sort()
    : [];

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>News App</h1>
          <p>Your personal news digest</p>
        </div>

        <nav className="navigation">
          <button
            type="button"
            className={
              view === "digest"
                ? "navigation-button active"
                : "navigation-button"
            }
            onClick={() => setView("digest")}
          >
            Digest
          </button>

          <button
            type="button"
            className={
              view === "explore"
                ? "navigation-button active"
                : "navigation-button"
            }
            onClick={() => setView("explore")}
          >
            Explore
          </button>
        </nav>
      </header>

      <main className="main">
        {view === "digest" && (
          <>
            {loading && (
              <p>Loading latest digest...</p>
            )}

            {error && (
              <p>
                Could not load the latest digest:{" "}
                {error}
              </p>
            )}

            {!loading && !error && !digest && (
              <p>
                There is no news digest yet.
              </p>
            )}

            {!loading && !error && digest && (
              <DigestView
                isLatestDigest={isLatestDigest}
                digest={digest}
                digests={digests}
                loadingDigests={loadingDigests}
                selectedDigestId={selectedDigestId}
                onSelectDigest={(item) => {
                  setSelectedDigestId(item.id);
                  setDigest(item);

                  setWhyItMatters({});
                  setWhyError({});

                  setCategory("");
                  setSource("");
                }}
                category={category}
                source={source}
                setCategory={setCategory}
                setSource={setSource}
                categories={digestCategories}
                sources={digestSources}
                whyItMatters={whyItMatters}
                loadingWhy={loadingWhy}
                whyError={whyError}
                onWhyItMatters={handleWhyItMatters}
                readStatus={readStatus}
                onReadStatus={handleReadStatus}
              />
            )}
          </>
        )}
        {view === "explore" && (
          <ExploreView
            exploreCategory={exploreCategory}
            exploreSource={exploreSource}
            setExploreCategory={setExploreCategory}
            setExploreSource={setExploreSource}
            exploreCategories={exploreCategories}
            exploreSources={exploreSources}
            activeSearch={activeSearch}
            articleSearch={articleSearch}
            setArticleSearch={setArticleSearch}
            setActiveSearch={setActiveSearch}
            setArticleOffset={setArticleOffset}
            loadingArticles={loadingArticles}
            articlesError={articlesError}
            allArticles={allArticles}
            whyItMatters={whyItMatters}
            loadingWhy={loadingWhy}
            whyError={whyError}
            onWhyItMatters={handleWhyItMatters}
            articleOffset={articleOffset}
            articleLimit={articleLimit}
            hasMoreArticles={hasMoreArticles}
            readStatus={readStatus}
            onReadStatus={handleReadStatus}
            exploreReadFilter={exploreReadFilter}
            setExploreReadFilter={setExploreReadFilter}
          />
        )}
      </main>
    </div>
  );
}

export default App;
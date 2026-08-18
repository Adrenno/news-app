function DigestHistory({
  digests,
  loading,
  selectedDigestId,
  onSelectDigest,
}) {
  return (
    <aside className="digest-history">
      <h3>Digests</h3>

      {loading && (
        <p>Loading...</p>
      )}

      {!loading && digests.length === 0 && (
        <p>No digests.</p>
      )}

      {!loading && digests.length > 0 && (
        <div className="digest-list">
          {digests.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => onSelectDigest(item)}
              className={
                item.id === selectedDigestId
                  ? "digest-history-item active"
                  : "digest-history-item"
              }
            >
              <span>
                Digest #{item.id}
              </span>

              <span>
                {item.created_at}
              </span>
            </button>
          ))}
        </div>
      )}
    </aside>
  );
}

export default DigestHistory;
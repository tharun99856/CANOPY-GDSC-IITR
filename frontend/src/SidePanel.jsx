import { useState, useEffect, useRef } from "react";
import { fetchSummary } from "./api";

const TYPE_LABELS = {
  py: "Python",
  js: "JavaScript",
  ts: "TypeScript",
  jsx: "JSX",
  tsx: "TSX",
  other: "File",
};

export default function SidePanel({ node, g_data }) {
  const [summary, setSummary] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const debounceRef = useRef(null);

  const content = g_data._content?.[node.data.fullPath] || "";
  const typeLabel = TYPE_LABELS[node.data.type] || "File";

  useEffect(() => {
    setSummary("");
    setIsLoading(false);
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (!content) {
      setSummary("No content available for this file.");
      return;
    }

    debounceRef.current = setTimeout(async () => {
      setIsLoading(true);
      try {
        const result = await fetchSummary(node.data.fullPath, content);
        setSummary(result);
      } catch (e) {
        setSummary("Summary unavailable. Try again in a moment.");
      }
      setIsLoading(false);
    }, 400);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [node.id, content, node.data.fullPath]);

  return (
    <div>
      <div className="side-panel-header">{node.data.label}</div>

      <div className="meta-row">
        <span>Path</span>
        <span style={{ textAlign: "right", maxWidth: "60%", overflow: "hidden", textOverflow: "ellipsis" }}>
          {node.data.fullPath}
        </span>
      </div>

      <div className="meta-row">
        <span>Lines of code</span>
        <span>{node.data.loc}</span>
      </div>

      <div className="meta-row">
        <span>Type</span>
        <span className="type-badge">{typeLabel}</span>
      </div>

      <div style={{ marginTop: 16 }}>
        <div className="meta-row" style={{ fontWeight: 600, color: "var(--text-primary)", marginBottom: 8 }}>
          AI Summary
        </div>
        {isLoading ? (
          <div className="summary-loading">
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div className="loading-spinner" />
              <span>Analysing file...</span>
            </div>
          </div>
        ) : (
          <div className="summary-block">{summary}</div>
        )}
      </div>
    </div>
  );
}

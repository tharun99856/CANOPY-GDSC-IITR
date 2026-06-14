import { memo } from "react";
import { Handle, Position } from "reactflow";

const TYPE_COLORS = {
  py: "var(--node-py)",
  js: "var(--node-js)",
  ts: "var(--node-ts)",
  jsx: "var(--node-jsx)",
  tsx: "var(--node-tsx)",
  other: "var(--border)",
};

const NodeCard = memo(function NodeCard({ data, selected }) {
  const { label, fullPath, loc, type, searchMatch, searchDim } = data;
  const color = TYPE_COLORS[type] || TYPE_COLORS.other;

  let cls = "canopy-node";
  if (selected) cls += " selected";
  if (searchMatch) cls += " search-match";
  if (searchDim) cls += " search-dim";

  return (
    <div className={cls} style={{ "--node-type-color": color }}>
      <Handle type="target" position={Position.Left} style={{ opacity: 0, width: 6, height: 6 }} />
      <div className="node-filename" title={label}>
        {fullPath}
      </div>
      <span className="loc-badge">{loc} lines</span>
      <Handle type="source" position={Position.Right} style={{ opacity: 0, width: 6, height: 6 }} />
    </div>
  );
});

export default NodeCard;

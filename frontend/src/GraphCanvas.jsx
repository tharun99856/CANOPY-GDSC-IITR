import { useMemo, useCallback, useEffect } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from "reactflow";
import dagre from "@dagrejs/dagre";
import "reactflow/dist/style.css";
import NodeCard from "./NodeCard";

const nodeTypes = { canopyNode: NodeCard };

function layoutGraph(nodes, edges) {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: "LR", ranksep: 120, nodesep: 50, edgesep: 20 });

  nodes.forEach((n) => {
    g.setNode(n.id, { width: 160, height: 50 });
  });
  edges.forEach((e) => {
    g.setEdge(e.source, e.target);
  });

  dagre.layout(g);

  const laidOut = nodes.map((n) => {
    const pos = g.node(n.id);
    return {
      ...n,
      position: { x: pos.x - 80, y: pos.y - 25 },
      sourcePosition: "right",
      targetPosition: "left",
    };
  });

  return { nodes: laidOut, edges };
}

export default function GraphCanvas({ g_data, sel_n, search_q, onNodeClick }) {
  const initial = useMemo(() => {
    if (!g_data || !g_data.nodes) return { nodes: [], edges: [] };

    const nodes = g_data.nodes.map((n) => ({
      id: n.id,
      type: "canopyNode",
      data: {
        label: n.id.split("/").pop(),
        fullPath: n.id,
        loc: n.loc,
        type: n.type,
        searchMatch: false,
        searchDim: false,
      },
      position: { x: 0, y: 0 },
    }));

    const edges = (g_data.edges || []).map((e, i) => ({
      id: `e-${i}-${e.src}-${e.tgt}`,
      source: e.src,
      target: e.tgt,
      type: "default",
      animated: false,
      style: { stroke: "var(--edge-default)", strokeWidth: 1.5 },
    }));

    return layoutGraph(nodes, edges);
  }, [g_data]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initial.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initial.edges);

  useEffect(() => {
    setNodes(initial.nodes);
    setEdges(initial.edges);
  }, [initial, setNodes, setEdges]);

  // Apply search highlighting
  useEffect(() => {
    if (!search_q.trim()) {
      setNodes((prev) =>
        prev.map((n) => ({
          ...n,
          data: { ...n.data, searchMatch: false, searchDim: false },
        }))
      );
      return;
    }
    const q = search_q.toLowerCase();
    setNodes((prev) =>
      prev.map((n) => {
        const match = n.data.label.toLowerCase().includes(q) || n.data.fullPath.toLowerCase().includes(q);
        return {
          ...n,
          data: { ...n.data, searchMatch: !match, searchDim: match },
        };
      })
    );
  }, [search_q, setNodes]);

  const handleNodeClick = useCallback(
    (_, node) => {
      onNodeClick(node);
    },
    [onNodeClick]
  );

  return (
    <div className="graph-wrap">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.1}
        maxZoom={2}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="var(--border)" gap={20} size={1} />
        <Controls />
        <MiniMap
          nodeColor={(n) => {
            const colors = {
              py: "#2a7a5a",
              js: "#a87820",
              ts: "#2e5fa3",
              jsx: "#6b4fa0",
              tsx: "#1e7a96",
            };
            return colors[n.data?.type] || "#243d24";
          }}
          maskColor="rgba(6, 13, 6, 0.7)"
        />
      </ReactFlow>
    </div>
  );
}

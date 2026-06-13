export default function SearchBar({ value, onChange }) {
  return (
    <div className="search-wrap">
      <input
        className="search-input"
        type="text"
        placeholder="Search files..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}

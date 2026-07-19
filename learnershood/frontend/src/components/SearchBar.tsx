import { Search } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  value: string;
  onChange: (value: string) => void;
}

function SearchBar({ onSearch, value, onChange }: SearchBarProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(value);
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search for African stories..."
        rows={3}
        className="w-full px-6 py-4 text-lg rounded-2xl border-2 border-indigo-200 focus:border-indigo-600 focus:outline-none shadow-lg pr-12 resize-none"
      />
      <button
        type="submit"
        className="absolute right-4 top-1/2 transform -translate-y-1/2 text-indigo-600 hover:text-indigo-800"
      >
        <Search className="w-6 h-6" />
      </button>
    </form>
  );
}

export default SearchBar;
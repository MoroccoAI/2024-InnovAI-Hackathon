import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

const SearchBar = ({ children }: Props) => {
  return <div className="searchBar">{children}</div>;
};

export default SearchBar;
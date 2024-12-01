import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

const Headings = ({ children }: Props) => {
  return <div>{children}</div>;
};

export default Headings;
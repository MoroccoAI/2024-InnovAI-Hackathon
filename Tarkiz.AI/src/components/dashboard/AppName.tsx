import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

const AppName = ({ children }: Props) => {
  return <div className="app-name">{children}</div>;
};

export default AppName;
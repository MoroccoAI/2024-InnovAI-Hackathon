import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

const Chat = ({ children }: Props) => {
  return <div className="chat">{children}</div>;
};

export default Chat;
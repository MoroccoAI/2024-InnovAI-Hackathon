export interface Task {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
  priority: 'low' | 'medium' | 'high';
}

export interface FocusSession {
  id: string;
  startTime: Date;
  duration: number; // in minutes
  taskId?: string;
  completed: boolean;
}

export interface Transaction {
  company: string;
  logo: string;
  client: string;
  amount: number;
  rating: number;
  status: 'Good' | 'Bad';
}

export interface MessageType {
  content: string;
  sender: 'user' | 'bot';
}
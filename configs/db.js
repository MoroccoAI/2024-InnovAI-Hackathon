import { drizzle } from 'drizzle-orm/neon-http';

export const db = drizzle(process.env.NEXT_PUBLIC_CONNECION_DATABASE_STRING);

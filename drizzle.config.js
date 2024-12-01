import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "postgresql",
  schema: "./configs/schema.js",
  dbCredentials:{
    url:'postgresql://ai%20study%20db_owner:XHLycqso5mC7@ep-plain-boat-a54u6c62.us-east-2.aws.neon.tech/ai%20study%20db?sslmode=require'
  }
});

// @ts-check
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import sitemap from "@astrojs/sitemap";
import node from "@astrojs/node";

// https://astro.build/config
export default defineConfig({
  output: "server",
  integrations: [
    react({
      include: ["**/react/*", "**/components/**/*.{jsx,tsx}"],
      experimentalReactChildren: true,
    }),
    sitemap(),
  ],
  server: {
    port: 3000,
    host: true,
  },
  adapter: node({
    mode: "standalone",
  }),
  experimental: {
    session: true,
  },
  vite: {
    ssr: {
      noExternal: ["react-router-dom"],
    },
    optimizeDeps: {
      include: ["react", "react-dom", "react-router-dom"],
    },
  },
});

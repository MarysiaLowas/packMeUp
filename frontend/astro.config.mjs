// @ts-check
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import sitemap from "@astrojs/sitemap";
import node from "@astrojs/node";
import tailwind from "@astrojs/tailwind";
import path from "path";

// https://astro.build/config
export default defineConfig({
  output: "server",
  integrations: [
    tailwind(),
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
    resolve: {
      alias: {
        "@": path.resolve("./src"),
      },
    },
  },
});

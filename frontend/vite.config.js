import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const refreshPreamble = `
  import { injectIntoGlobalHook } from "/@react-refresh";
  injectIntoGlobalHook(window);
  window.$RefreshReg$ = () => {};
  window.$RefreshSig$ = () => (type) => type;
  window.__vite_plugin_react_preamble_installed__ = true;
`;

export default defineConfig({
  plugins: [
    react(),
    {
      name: "sentinel-react-refresh-preamble",
      transformIndexHtml: {
        order: "pre",
        handler(_, context) {
          if (!context.server) return [];
          return [{
            tag: "script",
            attrs: { type: "module" },
            children: refreshPreamble,
            injectTo: "head-prepend",
          }];
        },
      },
    },
  ],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});

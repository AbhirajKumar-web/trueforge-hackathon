const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

app.use(createProxyMiddleware({
  target: 'http://localhost:8790',
  changeOrigin: true,
  pathFilter: '/api',
  on: {
    proxyReq: (proxyReq, req, res) => {
      proxyReq.setHeader('Cache-Control', 'no-cache');
      proxyReq.setHeader('Connection', 'keep-alive');
    },
    proxyRes: (proxyRes, req, res) => {
      if (proxyRes.headers['content-type'] && proxyRes.headers['content-type'].includes('text/event-stream')) {
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Connection', 'keep-alive');
        if (typeof res.flushHeaders === 'function') {
          res.flushHeaders();
        }
      }
    },
    error: (err, req, res) => {
      console.error('[Proxy Error]:', err.message);
    }
  }
}));

app.use(express.static(__dirname));

const server = app.listen(4000, () => {
  console.log('Open http://localhost:4000/anahita.html');
});

server.timeout = 0;
server.keepAliveTimeout = 0;
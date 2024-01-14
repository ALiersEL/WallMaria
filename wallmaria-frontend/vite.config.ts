import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default ({ mode }) => {
    process.env = {...process.env, ...loadEnv(mode, process.cwd())};
    return defineConfig({
        plugins: [ vue(),],
        server: {
            port: 5173,
            proxy: { // 本地开发环境通过代理实现跨域，生产环境使用 nginx 转发
                // 正则表达式写法
                '^/api': {
                    target: process.env.VITE_APP_BACKEND_URL,
                    ws: true,
                    changeOrigin: true, //开启代理
                    rewrite: (path) => path.replace(/^\/api/, '')
                }
            }
        },
    });
}


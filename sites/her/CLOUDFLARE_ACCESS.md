# Cloudflare Access 配置说明

Her 站点是一个私密站点，建议使用 Cloudflare Access 进行访问保护。

## 配置步骤

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)

2. 进入 **Zero Trust** > **Access** > **Applications**

3. 点击 **Add an application** > **Self-hosted**

4. 配置应用：
   - **Application name**: Her
   - **Session Duration**: 24 hours（或根据需要调整）
   - **Application domain**: `tarduspura.me/her/*`

5. 配置访问策略：
   - **Policy name**: Allow specific users
   - **Action**: Allow
   - **Include**: 
     - Emails: 添加允许访问的邮箱地址
     - 或使用 One-time PIN 方式

6. 保存配置

## 访问方式

配置完成后，访问 `/her/` 路径时会自动跳转到 Cloudflare 登录页面，只有授权用户才能访问。

## 注意事项

- 确保域名已经接入 Cloudflare
- Zero Trust 功能需要 Cloudflare 账户（免费版支持最多 50 用户）
- 建议定期检查访问日志

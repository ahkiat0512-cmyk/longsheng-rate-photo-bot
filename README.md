# 龙盛汇率做图助手

独立 Telegram 机器人：只允许一个指定群触发，群内发送标准龙盛汇率文字后，机器人自动回传固定黑金龙纹高清海报。

## 工作规则

- Bot 用户名：`@longshengratephoto_bot`
- 仅 `ALLOWED_CHAT_ID` 对应的群可使用。
- 私聊、其他群、频道消息一律忽略。
- 只有包含「马币转账」的完整汇率文字才会触发。
- 海报为固定模板；只更新日期和汇率。

## Render 部署

1. 将本项目上传到 GitHub 私人仓库。
2. 在 Render 建立 **New + / Blueprint**，选择该仓库。
3. 在 Render 的 Environment 中填入：
   - `TELEGRAM_BOT_TOKEN`：从 BotFather 新生成的 Token。
   - `ALLOWED_CHAT_ID`：指定群的数字 chat ID，例如 `-100...`。
   - `TELEGRAM_WEBHOOK_SECRET`：Render 自动生成；不要公开。
4. 部署完成后复制服务网址，例如 `https://longsheng-rate-photo-bot.onrender.com`。
5. 设置 Telegram webhook，URL 为：

   `https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<RENDER_URL>&secret_token=<TELEGRAM_WEBHOOK_SECRET>`

6. 将 `@longshengratephoto_bot` 加入指定群，并关闭 BotFather 的 privacy mode：`/setprivacy` → 选择机器人 → `Disable`。这样它才能读取群内普通文字。

## 本地检查

```bash
python3 -m unittest discover -s tests -v
```

# Longsheng Telegram Rate Bot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dedicated Telegram bot that turns approved 龙盛汇率文本 into a fixed-style high-resolution poster inside one whitelisted group.

**Architecture:** A Python service receives Telegram updates, rejects all chats except `ALLOWED_CHAT_ID`, parses the standard daily rate text into a typed object, and gives it to a deterministic poster renderer. The renderer draws text on a fixed high-resolution 龙盛 template and sends the resulting PNG back to the originating group.

**Tech Stack:** Python 3.12, aiogram 3, FastAPI, Pillow, pytest, Render.

**Spec:** `docs/superpowers/specs/2026-10-26-longsheng-telegram-rate-bot-design.md`

## Global Constraints

- One independent bot named 龙盛汇率做图助手.
- Respond only when `chat.id == ALLOWED_CHAT_ID`.
- Never commit `TELEGRAM_BOT_TOKEN`, `ALLOWED_CHAT_ID`, or any secret.
- Preserve one fixed black-gold 龙盛 visual template and combine MYR and RMB details in one PNG.

## Review Focus

- A private or other-group message must produce no image and no reply.
- A missing rate line must produce a clear validation error without generating an image.
- Unicode Chinese, `TNG`, `RM1,000`, and Telegram handles must render without clipping.
- Both Markdown-decorated and plain-text rate messages must parse identically.
- Concurrent group messages must return the matching poster, not each other’s data.

---

### Task 1: Project configuration and whitelist guard

**Files:**
- Create: `longsheng_rate_bot/config.py`
- Create: `longsheng_rate_bot/main.py`
- Create: `tests/test_whitelist.py`
- Create: `.env.example`
- Create: `pyproject.toml`

**Interfaces:**
- Produces: `Settings`, `is_allowed_chat(chat_id: int, settings: Settings) -> bool`.

- [ ] Write failing tests for the configured group ID being accepted and all other IDs being rejected.
- [ ] Run `pytest tests/test_whitelist.py -v` and confirm failure.
- [ ] Implement typed environment configuration and `is_allowed_chat`.
- [ ] Run the test and confirm pass.
- [ ] Commit configuration and whitelist guard.

### Task 2: Daily-rate message parser

**Files:**
- Create: `longsheng_rate_bot/models.py`
- Create: `longsheng_rate_bot/parser.py`
- Create: `tests/test_parser.py`

**Interfaces:**
- Produces: `RateSheet` with `date`, `local_rate`, `foreign_tng_rate`, three cash rates, and two RMB rates.
- Produces: `parse_rate_sheet(text: str) -> RateSheet`.

- [ ] Write failing parser tests using the 26/10/2026 supplied content and a Markdown-decorated variant.
- [ ] Run `pytest tests/test_parser.py -v` and confirm failure.
- [ ] Implement field normalization, parsing, and field-specific validation errors.
- [ ] Run parser tests and confirm pass.
- [ ] Commit parser.

### Task 3: Fixed high-resolution poster renderer

**Files:**
- Create: `assets/longsheng-template.png`
- Create: `longsheng_rate_bot/render.py`
- Create: `tests/test_render.py`

**Interfaces:**
- Consumes: `RateSheet`.
- Produces: `render_poster(sheet: RateSheet, output_path: Path) -> Path`.

- [ ] Create a blank, high-resolution 龙盛 black-gold template with header/footer and designated text zones.
- [ ] Write a failing render test that checks output is PNG, portrait, and contains non-empty rate zones.
- [ ] Run `pytest tests/test_render.py -v` and confirm failure.
- [ ] Implement deterministic Pillow typography, clipping-safe wrapping, and fixed footer copy.
- [ ] Run renderer tests and confirm pass.
- [ ] Commit rendering assets and renderer.

### Task 4: Telegram handlers and response flow

**Files:**
- Modify: `longsheng_rate_bot/main.py`
- Create: `longsheng_rate_bot/handlers.py`
- Create: `tests/test_handlers.py`

**Interfaces:**
- Consumes: `is_allowed_chat`, `parse_rate_sheet`, and `render_poster`.
- Produces: a photo reply for valid whitelisted group text and a validation reply for invalid whitelisted group text.

- [ ] Write handler tests for allowed valid message, allowed invalid message, and denied-chat message.
- [ ] Run `pytest tests/test_handlers.py -v` and confirm failure.
- [ ] Implement aiogram update handler and temp-file cleanup.
- [ ] Run handler tests and full `pytest -v` and confirm pass.
- [ ] Commit Telegram flow.

### Task 5: Deployment package and operating instructions

**Files:**
- Create: `Dockerfile`
- Create: `render.yaml`
- Create: `README.md`

**Interfaces:**
- Consumes: Render environment variables `TELEGRAM_BOT_TOKEN`, `ALLOWED_CHAT_ID`, and `WEBHOOK_BASE_URL`.
- Produces: a deployable web service and instructions to configure Telegram webhook.

- [ ] Add a deployment smoke test or container build check.
- [ ] Run the build check and full test suite.
- [ ] Document secure token entry, how to obtain the target chat ID, and how to make the bot group admin.
- [ ] Commit deployment package.

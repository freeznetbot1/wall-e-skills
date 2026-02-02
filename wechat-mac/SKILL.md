---
name: wechat-mac
description: Control and interact with WeChat client on macOS via GUI automation, OCR, and accessibility APIs.
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "os": ["darwin"],
        "requires": { "bins": ["python3", "cliclick"] },
        "install":
          [
            {
              "id": "pip-deps",
              "kind": "shell",
              "label": "Install Python dependencies",
              "command": "pip3 install pyautogui opencv-python pytesseract pillow"
            },
            {
              "id": "tesseract",
              "kind": "brew",
              "formula": "tesseract",
              "label": "Install Tesseract OCR (brew)"
            },
            {
              "id": "cliclick",
              "kind": "brew",
              "formula": "cliclick",
              "label": "Install cliclick for reliable keyboard input"
            }
          ],
      },
  }
---

# wechat-mac

Control and interact with WeChat macOS client via GUI automation.

## Capabilities

- **Screenshot & OCR**: Capture WeChat window and extract text
- **Click & Type**: Simulate clicks and keyboard input in WeChat
- **Find UI Elements**: Locate buttons, chat items, input fields
- **Send Messages**: Automate message sending to contacts
- **List Chats**: Read chat list and recent messages

## Requirements

1. Grant Accessibility permissions to Terminal in System Settings > Privacy & Security > Accessibility
2. WeChat must be running (`/Applications/WeChat.app`)
3. Tesseract OCR for text recognition

## Common Commands

```bash
# Screenshot current WeChat window
wechat-mac screenshot

# Extract text from WeChat window
wechat-mac ocr

# Find a button by image template
wechat-mac find --template /path/to/button.png

# Send message to contact
wechat-mac send --contact "微信昵称" --message "你好"

# Click at coordinates
wechat-mac click --x 500 --y 300

# Type text
wechat-mac type --text "Hello from WeChat Mac skill"
```

## Python Module Usage

```python
from wechat_mac import WeChatController

wc = WeChatController()
wc.activate()  # Bring WeChat to front

# Screenshot and OCR
text = wc.extract_text()

# Send message
wc.send_message("contact_name", "Hello!")

# Find UI element
location = wc.find_template("search_button.png")
if location:
    wc.click(location)
```

## Notes

- Coordinates are screen-relative (top-left is 0,0)
- Use `wechat-mac calibrate` to get coordinates for custom actions
- Screenshots are saved to /tmp/wechat_mac_screenshots/

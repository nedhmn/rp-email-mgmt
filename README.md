# rp-email-mgmt

Update Google Workspace email signatures programmatically.

## Requirements

### Code
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Google Cloud Setup
1. Create a project in [Google Cloud Console](https://console.cloud.google.com)
2. Enable APIs:
   - Gmail API
   - Admin SDK API
3. Create a Service Account and download the JSON key
4. Save key as `credentials/service-account.json`

### Google Workspace Admin Setup
1. Go to [admin.google.com](https://admin.google.com) � Security � Access and data control � API controls � Domain-wide delegation
2. Add the service account Client ID with these scopes:
   ```
   https://www.googleapis.com/auth/gmail.settings.basic,https://www.googleapis.com/auth/admin.directory.user.readonly
   ```

### User Data (Google Directory)
Each user needs these fields populated in Google Admin � Directory � Users:
- **Name** (first/last)
- **Job title** (Employee information � Job title)
- **Phone number** (Contact information � Phone)

## Configuration

### Environment Variables
Create `.env` file:
```
ADMIN_EMAIL=admin@yourdomain.com
USERS=user1@domain.com,user2@domain.com,user3@domain.com
```

### Settings
Edit `rpemail/config.py` for company-wide settings:
```python
company_website: str = Field(default="https://yourcompany.com")
logo_url: str = Field(default="https://i.imgur.com/XXXXX.png")
template_name: str = Field(default="signature_v1.html")
```

## Usage

```bash
# Install dependencies
uv sync

# Update signatures for all users
make start

# Lint code
make lint

# Type check
make typecheck

# Run both
make check
```

## Templates

HTML templates are in `rpemail/templates/`. Edit or create new templates there.

See `rpemail/templates/README.md` for template variables.

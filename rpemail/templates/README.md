# Email Signature Templates

## Available Templates

### `signature_v1.html`
Classic layout with logo on the left, details on the right.

```
[LOGO]  Name
        Title

        email@domain.com
        +1 234 567 8900
        https://example.com
```

### `signature_v2.html`
Modern layout with accent border, logo on the right.

```
|  Name
|  Title
|
|  phone | email
|  website              [LOGO]
```

## Template Variables

All templates use these Jinja2 variables:

| Variable | Description |
|----------|-------------|
| `{{ name }}` | Full name from Google Directory |
| `{{ title }}` | Job title from Google Directory |
| `{{ email }}` | User's email address |
| `{{ phone }}` | Phone number from Google Directory |
| `{{ website }}` | Company website (from config) |
| `{{ logo_url }}` | Company logo URL (from config) |

## Adding New Templates

1. Create a new HTML file: `signature_v3.html`
2. Use the variables above in your template
3. Update `template_name` in your `.env` or `config.py`
4. Run `make preview EMAIL=user@domain.com` to test

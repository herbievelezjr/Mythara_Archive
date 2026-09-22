# Mythara Glyph Assets

**Copyright © 2025 Herbert Velez Jr. All rights reserved.**  
**Proprietary and Confidential.**

## Directory Structure

```
assets/
├── glyphs/              # Original SVG files (scalable, production-ready)
│   ├── ssip_audit.svg
│   ├── engine_subscription_monthly.svg
│   ├── engine_subscription_annual.svg
│   ├── enterprise_license.svg
│   ├── custom_clause_dev.svg
│   ├── training_onboarding.svg
│   └── voip_bot_license.svg
│
└── glyphs_png/          # Exported PNG files (for PowerPoint, legacy systems)
    ├── dark/            # Near-black (#0A0A0A) for light backgrounds
    │   ├── 32/
    │   ├── 64/
    │   ├── 128/
    │   └── 256/
    ├── light/           # Near-white (#FAFAFA) for dark backgrounds
    │   ├── 32/
    │   ├── 64/
    │   ├── 128/
    │   └── 256/
    └── brand/           # Blue accent (#3B82F6) for highlights
        ├── 32/
        ├── 64/
        ├── 128/
        └── 256/
```

## Usage

### Web / Markdown (Recommended)
Use SVG files for best quality:
```html
<img src="./assets/glyphs/ssip_audit.svg" width="64" height="64" alt="SSIP Audit" />
```

### PowerPoint / Keynote
Use PNG files (choose color variant):
- **Light backgrounds:** Use `dark/` folder
- **Dark backgrounds:** Use `light/` folder
- **Brand highlights:** Use `brand/` folder

### Email Signatures / HTML Emails
Use PNG files (many email clients don't support SVG):
```html
<img src="https://yourdomain.com/assets/glyphs_png/dark/64/ssip_audit.png" width="64" height="64" alt="SSIP Audit" />
```

## Glyph Reference

| Glyph | File Name | Use Case |
|-------|-----------|----------|
| ![Audit](./glyphs/ssip_audit.svg) | `ssip_audit` | SSIP Compliance Audit |
| ![Monthly](./glyphs/engine_subscription_monthly.svg) | `engine_subscription_monthly` | Monthly Subscription |
| ![Annual](./glyphs/engine_subscription_annual.svg) | `engine_subscription_annual` | Annual Subscription |
| ![Enterprise](./glyphs/enterprise_license.svg) | `enterprise_license` | Enterprise License |
| ![Custom](./glyphs/custom_clause_dev.svg) | `custom_clause_dev` | Custom Clause Development |
| ![Training](./glyphs/training_onboarding.svg) | `training_onboarding` | Training & Onboarding |
| ![VoIP](./glyphs/voip_bot_license.svg) | `voip_bot_license` | VoIP Bot License (Q1 2026) |

## Color Variants

### Dark (#0A0A0A)
Best for: Light backgrounds, documents, white slides
- Near-black color ensures good contrast
- Professional appearance for business materials

### Light (#FAFAFA)
Best for: Dark backgrounds, dark mode websites, black slides
- Near-white color for visibility on dark surfaces
- Modern aesthetic for tech presentations

### Brand (#3B82F6)
Best for: Highlights, CTAs, featured items
- Blue accent matches Mythara brand palette
- Use sparingly for emphasis

## Regenerating PNGs

If you need different sizes or colors:

```powershell
# Edit export_glyph_pngs_simple.py
# Modify SIZES = [32, 64, 128, 256] or COLORS dict
# Then run:
py -3.11 export_glyph_pngs_simple.py
```

## Technical Specs

### SVG Files
- ViewBox: 256×256
- Stroke: `currentColor` (inherits parent color)
- Fill: `none`
- Stroke-width: 12px
- Style: Mono-line, rounded caps/joins
- Accessibility: `role="img"` and `aria-label` attributes

### PNG Files
- Format: PNG with transparency (RGBA)
- Sizes: 32×32, 64×64, 128×128, 256×256
- DPI: 96 (standard web resolution)
- Compression: Optimized for web use

## Notes

- **SVG is preferred** for web, apps, and high-resolution printing
- **PNG is fallback** for systems without SVG support (PowerPoint, email, older browsers)
- PNG files are simplified geometric versions for mockups
- For production materials, always use SVG when possible

## License

All glyphs are proprietary assets of Herbert Velez Jr. (Mythara Labs LLC planned — not yet formed). Do not distribute outside of Mythara commercial materials.


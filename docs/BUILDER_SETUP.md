# Builder.io Integration Setup Guide

This guide will help you set up Builder.io visual editing for the ValuAI UCaaS Valuation platform.

## Quick Setup

### 1. Get Your Builder.io API Key

1. Go to [Builder.io](https://builder.io) and sign up for a free account
2. Create a new space for your project
3. Go to Settings → API Keys
4. Copy your Public API Key (starts with `pub_`)

### 2. Configure API Key

Update the API key in these files:

**builder.config.json:**
```json
{
  "apiKey": "YOUR_ACTUAL_API_KEY_HERE"
}
```

**src/components/builder/BuilderPage.tsx:**
```typescript
builder.init('YOUR_ACTUAL_API_KEY_HERE');
```

### 3. VS Code Extension Setup

The Builder.io extension is already installed. To connect it:

1. Open VS Code Command Palette (`Ctrl+Shift+P`)
2. Run: `Builder.io: Connect`
3. Enter your API key when prompted
4. Select your Builder.io space

## Available Custom Components

We've registered these custom components for visual editing:

### FeatureCard
- **Props**: title, description, icon, gradient
- **Use**: Display feature highlights with icons
- **Icons**: sparkles, calculator, chart

### HeroSection  
- **Props**: title, subtitle, ctaText, backgroundGradient
- **Use**: Landing page hero sections
- **Gradients**: Multiple color scheme options

## Usage in Builder.io

1. **Create Content**: 
   - Go to builder.io → Content
   - Click "New" → "Page"
   - Use the visual editor to drag and drop components

2. **Preview**: 
   - Visit `http://localhost:5178/builder/[page-url]`
   - Content will render with your custom components

3. **Custom Components**:
   - In Builder.io editor, look for "FeatureCard" and "HeroSection" in the components panel
   - Drag them onto your page
   - Configure properties in the right panel

## Development Workflow

1. **Design in Builder.io**: Create pages visually
2. **Preview Locally**: See changes at `/builder/*` routes  
3. **Integrate**: Use BuilderComponent in your React components
4. **Deploy**: Builder.io content works with your deployment

## Advanced Usage

### Creating New Custom Components

1. Create component in `src/components/builder/`
2. Register with `Builder.registerComponent()`
3. Import in `BuilderComponents.tsx`
4. Component appears in Builder.io editor

### Dynamic Content

Use Builder.io's built-in features:
- A/B testing
- Personalization
- Scheduling
- Content targeting

## Troubleshooting

**White page in builder routes?**
- Verify API key is correct
- Check browser console for errors
- Ensure Builder.io space is published

**Components not showing in Builder.io?**
- Restart dev server after registering components
- Check component registration syntax
- Verify imports are correct

## Next Steps

1. Replace placeholder API key with your actual key
2. Create your first page in Builder.io
3. Test the `/builder/your-page` route
4. Start building visual content!

## Resources

- [Builder.io Documentation](https://www.builder.io/c/docs)
- [React SDK Guide](https://www.builder.io/c/docs/developers)
- [VS Code Extension Guide](https://www.builder.io/c/docs/vscode)

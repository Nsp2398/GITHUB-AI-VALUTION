# 🎯 Builder.io Integration - Quick Start

## ✅ What's Already Done

Your ValuAI project is now **Builder.io ready**! Here's what's been set up:

### 📦 Installed Packages
- `@builder.io/react` - React SDK for Builder.io
- `@builder.io/sdk` - Core Builder.io SDK  
- `@builder.io/dev-tools` - Development tools
- Builder.io VS Code extension (already installed)

### 🎨 Custom Components Created
- **FeatureCard**: For showcasing features with icons and gradients
- **HeroSection**: For landing page hero sections with CTAs
- **BuilderPage**: Main component for rendering Builder.io content

### 🚀 Integration Points
- `/builder/*` routes added to App.tsx
- Dashboard now has Builder.io section
- Custom components registered for visual editing

## 🔑 Get Your API Key (2 minutes)

### Step 1: Sign Up
1. Go to [builder.io](https://builder.io)
2. Click "Start Building" 
3. Sign up with email or GitHub

### Step 2: Create Space
1. After signup, you'll create your first "Space"
2. Name it "ValuAI" or similar
3. Select "React" as your framework

### Step 3: Get API Key
1. Go to Account → Space Settings
2. Copy your **Public API Key** (starts with `pub_`)

### Step 4: Update Config
Replace `pub_your_api_key_here` with your actual key in:

**1. builder.config.json**
```json
{
  "apiKey": "pub_YOUR_ACTUAL_KEY_HERE"
}
```

**2. src/components/builder/BuilderPage.tsx**
```typescript
builder.init('pub_YOUR_ACTUAL_KEY_HERE');
```

## 🎨 Start Creating

### Option 1: VS Code Extension
1. Open Command Palette (`Ctrl+Shift+P`)
2. Run: `Builder.io: Launch Visual Editor`
3. Start designing visually in VS Code!

### Option 2: Builder.io Website  
1. Go to your Builder.io dashboard
2. Click "Content" → "New" → "Page"
3. Use the visual editor
4. Preview at `http://localhost:5178/builder/your-page-url`

## 🚀 Your Custom Components

In the Builder.io editor, you'll find these custom components:

### FeatureCard
Perfect for feature showcases:
- **Title**: Feature name
- **Description**: Feature details  
- **Icon**: sparkles, calculator, chart
- **Gradient**: Multiple color schemes

### HeroSection
For impactful hero sections:
- **Title**: Main headline
- **Subtitle**: Supporting text
- **CTA Text**: Button text
- **Background**: Gradient options

## 🎯 Next Steps

1. **Get API Key**: Follow steps above
2. **Update Config**: Replace placeholder keys
3. **Create First Page**: Use Builder.io editor
4. **Preview**: Visit `/builder/your-page`
5. **Customize**: Add more components as needed

## 🔧 Development URLs

- **Frontend**: `http://localhost:5178/`
- **Builder Pages**: `http://localhost:5178/builder/*`
- **Dashboard**: Shows Builder.io section

## 📚 Resources

- [Builder.io Docs](https://www.builder.io/c/docs)
- [React Integration](https://www.builder.io/c/docs/developers)
- [Custom Components](https://www.builder.io/c/docs/custom-components)

---

🎉 **You're all set!** Just add your API key and start building visually!

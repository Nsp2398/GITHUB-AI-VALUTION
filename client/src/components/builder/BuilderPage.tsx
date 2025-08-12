/* BuilderPage.tsx has been uninstalled. */

import { builder, BuilderComponent, useIsPreviewing } from '@builder.io/react';

// Replace with your actual Builder.io API key
builder.init('pub_your_api_key_here');

interface BuilderPageProps {
  model?: string;
  content?: any;
}

export function BuilderPage({ model = 'page', content }: BuilderPageProps) {
  const isPreviewing = useIsPreviewing();
  
  if (content || isPreviewing) {
    return (
      <BuilderComponent model={model} content={content} />
    );
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Builder.io Integration Ready
        </h1>
        <p className="text-gray-600">
          Configure your Builder.io API key in builder.config.json and start creating visual content!
        </p>
      </div>
    </div>
  );
}

export default BuilderPage;

# Frontend Components Documentation

## Valuation Components

### UCaaSMetricsForm
A form component for collecting UCaaS-specific metrics.

#### Props
```typescript
interface UCaaSMetricsFormProps {
  onCalculate: (data: UCaaSMetricsData) => void;
  isLoading?: boolean;
  initialData?: UCaaSMetricsData;
}
```

#### Usage
```tsx
import { UCaaSMetricsForm } from 'components/valuation/UCaaSMetricsForm';

const MyComponent = () => {
  const handleCalculate = (data) => {
    // Handle calculation
  };

  return <UCaaSMetricsForm onCalculate={handleCalculate} />;
};
```

### MarketComparables
A component for displaying market comparables data and visualizations.

#### Props
```typescript
interface MarketComparablesProps {
  peerData: PeerComparisonData[];
  companyMetrics: CompanyMetrics;
  isLoading?: boolean;
}
```

#### Usage
```tsx
import { MarketComparables } from 'components/valuation/MarketComparables';

const MyComponent = () => {
  return (
    <MarketComparables 
      peerData={peerData}
      companyMetrics={metrics}
    />
  );
};
```

## UI Components

### FileUpload
A reusable file upload component with drag-and-drop support.

#### Props
```typescript
interface FileUploadProps {
  onFileUpload: (file: File) => Promise<void>;
  acceptedTypes?: string;
  maxSize?: number;
}
```

#### Usage
```tsx
import { FileUpload } from 'components/ui/FileUpload';

const MyComponent = () => {
  const handleUpload = async (file) => {
    // Handle file upload
  };

  return (
    <FileUpload 
      onFileUpload={handleUpload}
      acceptedTypes=".pdf,.doc,.docx"
      maxSize={10}
    />
  );
};
```

### InputField
A styled input field component with validation support.

#### Props
```typescript
interface InputFieldProps {
  label: string;
  name: string;
  type?: string;
  error?: string;
  required?: boolean;
  // ... other HTML input props
}
```

#### Usage
```tsx
import { InputField } from 'components/ui/InputField';

const MyComponent = () => {
  return (
    <InputField
      label="Monthly Revenue"
      name="mrr"
      type="number"
      required
    />
  );
};
```

## Pages

### ValuationWizard
The main valuation workflow component.

#### Features
- Multi-step form
- Progress tracking
- Data validation
- Results visualization

#### Usage
```tsx
import { ValuationWizard } from 'pages/ValuationWizard';

const App = () => {
  return <ValuationWizard />;
};
```

## Best Practices

1. Component Organization
   - Keep components focused and small
   - Use composition over inheritance
   - Follow the Single Responsibility Principle

2. State Management
   - Use React Query for server state
   - Use local state for UI state
   - Implement proper loading states

3. Error Handling
   - Implement error boundaries
   - Show user-friendly error messages
   - Log errors for debugging

4. Performance
   - Use React.memo for expensive renders
   - Implement proper list virtualization
   - Optimize re-renders

5. Accessibility
   - Use semantic HTML
   - Implement proper ARIA attributes
   - Ensure keyboard navigation

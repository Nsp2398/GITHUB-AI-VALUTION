import '@testing-library/jest-dom';

// Mock ResizeObserver which is not available in jsdom
globalThis.ResizeObserver = (window as any).ResizeObserver || class {
    observe() {}
    unobserve() {}
    disconnect() {}
};

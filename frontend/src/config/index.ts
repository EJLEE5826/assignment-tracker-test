// Environment configuration
interface Config {
  apiUrl: string;
}

// Get API URL from environment variable or use default based on environment
const getApiUrl = (): string => {
  // Check for explicit environment variable first
  if (typeof process !== 'undefined' && process.env?.VITE_FASTAPI_URL) {
    return process.env.VITE_FASTAPI_URL;
  }
  
  // For Jest testing environment, always use localhost
  if (typeof jest !== 'undefined') {
    return 'http://localhost:8000';
  }
  
  // For browser runtime, check hostname
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    }
  }
  
  // Default to production API for Vercel deployment
  return 'https://assignment-tracker-fastapi.onrender.com';
};

export const config: Config = {
  apiUrl: getApiUrl()
};

interface SearchParams {
  start_date: string;
  end_date: string;
  cnpj: string;
}

interface SITRAMResponse {
  success: boolean;
  data?: string;
  error?: string;
}

// Detect API URL based on environment
const getApiUrl = (): string => {
  // Production: GitHub Codespaces
  if (typeof window !== 'undefined' && window.location.hostname.includes('github.dev')) {
    return 'https://urban-potato-gxp745pxrjxc6gq-8000.app.github.dev/api';
  }

  // Development
  return import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
};

const API_BASE_URL = getApiUrl();

export async function searchSITRAMData(
  searchParams: SearchParams
): Promise<SITRAMResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/sitram/search/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        start_date: searchParams.start_date,
        end_date: searchParams.end_date,
        cnpj: searchParams.cnpj,
      }),
      credentials: 'include',
    });

    if (!response.ok) {
      const errorData = await response.json();
      return {
        success: false,
        error: errorData.error || `Request failed: ${response.status}`,
      };
    }

    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
    };
  }
}

export { SearchParams, SITRAMResponse };

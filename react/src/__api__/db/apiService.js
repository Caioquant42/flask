import axios from 'axios';

const API_BASE_URL = 'https://zommaquant.com.br/api'; // http://127.0.0.1:5000/api (Local) , https://zommaquant.com.br/api (Nginx-Server)
export default API_BASE_URL;

export const fetchSBendpoint = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/ibovstatic`);
    return response.data;
  } catch (error) {
    console.error("Error fetching SB analysis:", error);
    return { error: 'Error fetching SB analysis' };
  }
};

export const fetchVolatilityAnalysis = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/volatility`);
    return response.data;
  } catch (error) {
    console.error('Error fetching Volatility data:', error);
    throw error;
  }
};

export const fetchFLUXOendpoint = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/fluxo`);
    return response.data;
  } catch (error) {
    console.error("Error fetching fluxo endpoint:", error);
    return { error: 'Error fetching fluxo endpoint' };
  }
};

export const fetchBenchmarksHistoricalView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/performance`);
    return response.data;
  } catch (error) {
    console.error('Error fetching BenchmarksHistorical data:', error);
    throw error;
  }
};

export const fetchBRRecommendations = async (analysisType = 'all') => {
  try {
    const response = await axios.get(`${API_BASE_URL}/recommendations`, {
      params: { analysis: analysisType }
    });
    
    if (analysisType === 'all') {
      // Convert the object to an array of objects
      return Object.entries(response.data).map(([ticker, data]) => ({
        ticker,
        ...data
      }));
    } else {
      // For 'strong_buy' and 'buy', ensure we return an array
      return Array.isArray(response.data) ? response.data : [];
    }
  } catch (error) {
    console.error(`Error fetching BR recommendations (${analysisType}):`, error);
    return [];
  }
};

export const fetchBRStrongBuyAnalysis = () => fetchBRRecommendations('strong_buy');
export const fetchBRBuyAnalysis = () => fetchBRRecommendations('buy');
export const fetchBRIBOVAnalysis = () => fetchBRRecommendations('ibovlist');

export const fetchNASDAQRecommendations = async (analysisType = 'all') => {
  try {
    const response = await axios.get(`${API_BASE_URL}/nasdaq_recommendations`, {
      params: { analysis: analysisType }
    });
    
    if (analysisType === 'all') {
      // Convert the object to an array of objects
      return Object.entries(response.data).map(([ticker, data]) => ({
        ticker,
        ...data
      }));
    } else {
      // For 'strong_buy' and 'buy', ensure we return an array
      return Array.isArray(response.data) ? response.data : [];
    }
  } catch (error) {
    console.error(`Error fetching NASDAQ recommendations (${analysisType}):`, error);
    return [];
  }
};

export const fetchNASDAQStrongBuyAnalysis = () => fetchNASDAQRecommendations('strong_buy');
export const fetchNASDAQBuyAnalysis = () => fetchNASDAQRecommendations('buy');

export const fetchNYSERecommendations = async (analysisType = 'all') => {
  try {
    const response = await axios.get(`${API_BASE_URL}/nyse_recommendations`, {
      params: { analysis: analysisType }
    });
    
    if (analysisType === 'all') {
      // Convert the object to an array of objects
      return Object.entries(response.data).map(([ticker, data]) => ({
        ticker,
        ...data
      }));
    } else {
      // For 'strong_buy' and 'buy', ensure we return an array
      return Array.isArray(response.data) ? response.data : [];
    }
  } catch (error) {
    console.error(`Error fetching NYSE recommendations (${analysisType}):`, error);
    return [];
  }
};

export const fetchNYSEStrongBuyAnalysis = () => fetchNYSERecommendations('strong_buy');
export const fetchNYSEBuyAnalysis = () => fetchNYSERecommendations('buy');



export const fetchRSIAnalysis = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/screener`);
    return response.data;
  } catch (error) {
    console.error("Error fetching RSI analysis:", error);
    return { error: 'Error fetching RSI analysis' };
  }
};




export const fetchSurvivalAnalysis = async (ticker = null) => {
  try {
    let url = `${API_BASE_URL}/survival_lomax`;
    if (ticker) {
      url += `?ticker=${ticker}`;
    }
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error("Error fetching survival analysis data:", error);
    return {};
  }
};

export const fetchDividendAgenda = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/dividend_agenda`);
    return response.data;
  } catch (error) {
    console.error('Error fetching dividend agenda:', error);
    throw error;
  }
};

export const fetchStatments = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/statements`);
    return response.data;
  } catch (error) {
    console.error('Error fetching dividend agenda:', error);
    throw error;
  }
};

export const fetchHistoricalDY = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/historical_dy`);
    return response.data;
  } catch (error) {
    console.error('Error fetching Historical DY data:', error);
    throw error;
  }
};


export const fetchTOP10VolatilityAnalysis = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/top-volatility-stocks`);
    return response.data;
  } catch (error) {
    console.error('Error fetching Historical DY data:', error);
    throw error;
  }
};


export const fetchSurfaceView = async (ticker) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/surface`, {
      params: { ticker }
    });
    return response.data[ticker] || null;
  } catch (error) {
    console.error('Error fetching surface data:', error);
    throw error;
  }
};

export const fetchCointegrationView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/cointegration`);
    return response.data;
  } catch (error) {
    console.error('Error fetching cointegration data:', error);
    throw error;
  }
};

export const fetchCurrencyCointegrationView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/currency_cointegration`);
    return response.data;
  } catch (error) {
    console.error('Error fetching cointegration data:', error);
    throw error;
  }
};

export const fetchRRGView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/rrg`);
    return response.data;
  } catch (error) {
    console.error('Error fetching RRG data:', error);
    throw error;
  }
};

export const fetchRRGINDEXView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/rrg`);
    return response.data;
  } catch (error) {
    console.error('Error fetching RRG data:', error);
    throw error;
  }
};

export const fetchOTMCOLLARView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/collar_analysis?category=otm`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchITMCOLLARView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/collar_analysis?category=intrinsic`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchINVERTEDOTMCOLLARView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/inverted_collar_analysis?inverted=true&category=otm`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchINVERTEDITMCOLLARView = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/inverted_collar_analysis?inverted=true&category=intrinsic`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchCoveredCalls = async (maturityRange = null) => {
  try {
    let url = `${API_BASE_URL}/covered_call`;
    if (maturityRange) {
      url += `?maturity_range=${maturityRange}`;
    }
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching covered calls data:', error);
    throw error;
  }
};



















export const fetchCOLLAR14View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/14/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchCOLLAR30View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/30/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar30 data:', error);
    throw error;
  }
};

export const fetchCOLLAR60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/60/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar60 data:', error);
    throw error;
  }
};

export const fetchCOLLARABOVE60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/above60/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collarabove60 data:', error);
    throw error;
  }
};

export const fetchOTMCOLLAR14View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/14/otm/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchOTMCOLLAR30View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/30/otm/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar30 data:', error);
    throw error;
  }
};

export const fetchOTMCOLLAR60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/60/otm/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar60 data:', error);
    throw error;
  }
};

export const fetchOTMCOLLARABOVE60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/above60/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collarabove60 data:', error);
    throw error;
  }
};




export const fetchInvertedCOLLAR14View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/14/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchInvertedCOLLAR30View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/30/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar30 data:', error);
    throw error;
  }
};

export const fetchInvertedCOLLAR60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/60/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar60 data:', error);
    throw error;
  }
};

export const fetchInvertedCOLLARABOVE60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/above60/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collarabove60 data:', error);
    throw error;
  }
};

export const fetchInvertedOTMCOLLAR14View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/14/otm/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar14 data:', error);
    throw error;
  }
};

export const fetchInvertedOTMCOLLAR30View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/30/otm/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar30 data:', error);
    throw error;
  }
};

export const fetchInvertedOTMCOLLAR60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/60/otm/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collar60 data:', error);
    throw error;
  }
};

export const fetchInvertedOTMCOLLARABOVE60View = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/opcoes/riscozero/above60/inverted`);
    return response.data;
  } catch (error) {
    console.error('Error fetching collarabove60 data:', error);
    throw error;
  }
};




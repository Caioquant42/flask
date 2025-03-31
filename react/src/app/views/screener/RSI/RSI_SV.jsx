//RSI_SV.jsx
import React, { useState, useEffect } from "react";
import { Small } from "app/components/Typography";
import { MatxProgressBar, SimpleCard } from "app/components";
import { fetchRSIAnalysis } from "/src/__api__/db/apiService";

export default function RSISV() {
  const [rsiData, setRsiData] = useState({
    stockdata_15m: { overbought: [], oversold: [] },
    stockdata_60m: { overbought: [], oversold: [] },
    stockdata_1d: { overbought: [], oversold: [] },
    stockdata_1w: { overbought: [], oversold: [] }
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await fetchRSIAnalysis();
        setRsiData(result);
      } catch (error) {
        console.error("Error fetching RSI analysis:", error);
      }
    };
    fetchData();
  }, []);

  const getColor = (rsi) => {
    if (rsi < 20) return "success";
    if (rsi < 30) return "primary";
    return "secondary";
  };

  const renderRSICard = (title, data, interval) => {
    if (!data || data.length === 0) {
      return (
        <SimpleCard title={title} sx={{ marginTop: 3 }}>
          <Small color="text.secondary" display="block" mb={2}>
            Sem dados disponíveis para {interval}
          </Small>
        </SimpleCard>
      );
    }

    return (
      <SimpleCard title={title} sx={{ marginTop: 3 }}>
        <Small color="text.secondary" display="block" mb={2}>
          {interval} Values
        </Small>
        {data.map((item, index) => (
          <MatxProgressBar
            key={`${interval}-${index}`}
            value={item.RSI}
            color={getColor(item.RSI)}
            text={`${item.Symbol} (${item.RSI.toFixed(2)})`}
          />
        ))}
      </SimpleCard>
    );
  };

  return (
    <div>
      {renderRSICard("Sobrevendido - 15 Minutos", rsiData.stockdata_15m?.oversold, "15 Minutes")}
      {renderRSICard("Sobrevendido - 60 Minutos", rsiData.stockdata_60m?.oversold, "60 Minutes")}
      {renderRSICard("Sobrevendido - Diário", rsiData.stockdata_1d?.oversold, "1 Day")}
      {renderRSICard("Sobrevendido - Semanal", rsiData.stockdata_1w?.oversold, "1 Week")}
    </div>
  );
}
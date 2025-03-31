from marshmallow import Schema, fields,INCLUDE

class SpecificDayResultSchema(Schema):
    survival_probability = fields.Float()
    hazard_rate = fields.Float()
    cumulative_hazard = fields.Float()

class ThresholdDataSchema(Schema):
    days_since_last_incident = fields.Int()
    tail_index = fields.Float()
    current_survival_probability = fields.Float()
    current_hazard_rate = fields.Float()
    current_cumulative_hazard = fields.Float()
    specific_day_results = fields.Dict(keys=fields.Str(), values=fields.Nested(SpecificDayResultSchema))

    class Meta:
        unknown = INCLUDE

class TickerDataSchema(Schema):
    _threshold_data = fields.Dict(keys=fields.Str(), values=fields.Nested(ThresholdDataSchema))

    class Meta:
        unknown = INCLUDE

class SurvivalAnalysisSchema(Schema):
    _ticker_data = fields.Dict(keys=fields.Str(), values=fields.Nested(TickerDataSchema))

    class Meta:
        unknown = INCLUDE


class FluxoDDMItemSchema(Schema):
    Data = fields.Str()
    Estrangeiro = fields.Str()
    Institucional = fields.Str()
    PF = fields.Str(data_key="Pessoa física")
    IF = fields.Str(data_key="Inst. Financeira")
    Outros = fields.Str()
    Todos = fields.Str()

    class Meta:
        unknown = INCLUDE

class FluxoDDMSchema(Schema):
    fluxo_ddm = fields.List(fields.Nested(FluxoDDMItemSchema))
    

class CumulativePerformanceSchema(Schema):
    CDI = fields.Dict(keys=fields.Str(), values=fields.Float())
    SP500 = fields.Dict(keys=fields.Str(), values=fields.Float())
    Gold = fields.Dict(keys=fields.Str(), values=fields.Float())
    USDBRL = fields.Dict(keys=fields.Str(), values=fields.Float())
    IBOV = fields.Dict(keys=fields.Str(), values=fields.Float())

class VolatilityAnalysisSchema(Schema):
    symbol = fields.Str()
    open = fields.Float()
    high = fields.Float()
    low = fields.Float()
    close = fields.Float()
    variation = fields.Float()
    volume = fields.Int()
    financial_volume = fields.Float()
    ewma_1y_max = fields.Float()
    ewma_1y_min = fields.Float()
    ewma_1y_percentile = fields.Float()
    ewma_1y_rank = fields.Float()
    ewma_6m_max = fields.Float()
    ewma_6m_min = fields.Float()
    ewma_6m_percentile = fields.Float()
    ewma_6m_rank = fields.Float()
    ewma_current = fields.Float()
    iv_1y_max = fields.Float()
    iv_1y_min = fields.Float()
    iv_1y_percentile = fields.Float()
    iv_1y_rank = fields.Float()
    iv_6m_max = fields.Float()
    iv_6m_min = fields.Float()
    iv_6m_percentile = fields.Float()
    iv_6m_rank = fields.Float()
    iv_current = fields.Float()
    middle_term_trend = fields.Int()
    semi_return_1y = fields.Float()
    short_term_trend = fields.Int()
    beta_ibov = fields.Float()
    garch11_1y = fields.Float()
    correl_ibov = fields.Float()
    entropy = fields.Float()
    iv_to_ewma_ratio_1y = fields.Float()
    iv_to_ewma_ratio_6m = fields.Float()
    iv_to_ewma_ratio_current = fields.Float()

class IBOVSchema(Schema):
    symbol = fields.Str()
    type = fields.Str()
    name = fields.Str()
    open = fields.Float()
    high = fields.Float()
    low = fields.Float()
    close = fields.Float()
    volume = fields.Int()
    financial_volume = fields.Float()
    trades = fields.Int()
    bid = fields.Float()
    ask = fields.Float()
    category = fields.Str()
    contract_size = fields.Int()
    created_at = fields.Str()
    updated_at = fields.Str()
    variation = fields.Float()
    ewma_1y_max = fields.Float()
    ewma_1y_min = fields.Float()
    ewma_1y_percentile = fields.Float()
    ewma_1y_rank = fields.Float()
    ewma_6m_max = fields.Float()
    ewma_6m_min = fields.Float()
    ewma_6m_percentile = fields.Float()
    ewma_6m_rank = fields.Float()
    ewma_current = fields.Float()
    has_options = fields.Bool()
    iv_1y_max = fields.Float()
    iv_1y_min = fields.Float()
    iv_1y_percentile = fields.Float()
    iv_1y_rank = fields.Float()
    iv_6m_max = fields.Float()
    iv_6m_min = fields.Float()
    iv_6m_percentile = fields.Float()
    iv_6m_rank = fields.Float()
    iv_current = fields.Float()
    middle_term_trend = fields.Int()
    semi_return_1y = fields.Float()
    short_term_trend = fields.Int()
    stdv_1y = fields.Float()
    stdv_5d = fields.Float()
    beta_ibov = fields.Float()
    garch11_1y = fields.Float()
    isin = fields.Str()
    correl_ibov = fields.Float()
    entropy = fields.Float()
    sector = fields.Str()
    cvmCode = fields.Str(allow_none=True)
    currency = fields.Str(allow_none=True)
    currencyScale = fields.Int(allow_none=True)
    marketMaker = fields.Bool(allow_none=True)
    previousClose = fields.Float(allow_none=True)
    time = fields.Str()





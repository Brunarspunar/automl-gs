    {{ field }}_dayofweeks_enc = pd.to_datetime(df['{{ field }}']).dt.dayofweek
    {{ field }}_dayofweeks_enc = encoders['dayofweeks_encoder'].transform({{ field }}_dayofweeks_enc)

    {{ field }}_hour = pd.to_datetime(df['{{ field }}']).dt.hour
    {{ field }}_hour = encoders['hour_encoder'].transform({{ field }}_hour)

    {% if params['datetime_month'] %}
    {{ field }}_month_enc = pd.to_datetime(df['{{ field }}']).dt.month - 1
    {{ field }}_month_enc = encoders['month_encoder'].transform({{ field }}_month_enc)
    {% endif %}

    {% if params['datetime_year'] %}
    {{ field }}_year_enc = pd.to_datetime(df['{{ field }}']).dt.year
    {{ field }}_year = encoders['{{ field }}_year_encoder'].fit_transform({{ field }}_year_enc)
    {% endif %}

    {% if params['datetime_holiday'] %}
    year_range = pd.to_datetime(df['{{ field }}']).dt.year
    us_holidays = holidays.US(years=range(year_range.min()[0],
                                                    year_range.max()[0]))
    df_holidays = pd.DataFrame(list(us_holidays.items()),
                                columns=['holiday_date', 'holiday'])
    holidays_df['holiday_date'] = pd.to_datetime(holidays_df['holiday_date'])
    holidays_df['holiday'] = holidays_df['holiday'].str.replace(' (Observed)', '')
    {{ field }}_date = pd.DataFrame(pd.to_datetime(df['{{ field }}']).dt.date, columns=['date'])
    {{ field }}_date = pd.merge(holidays_df, {{ field }}_date, how='right', on=['holiday_date', 'date'])

    {{ field }}_holiday = encoders['{{ field }}_holiday_lb'].fit_transform({{ field }}_date['holiday'].values)

    {% endif %}
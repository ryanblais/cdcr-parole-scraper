scheduleUrl = "https://www.cdcr.ca.gov/bph/2023/01/25/february-2024-hearing-calendar/"
resultUrl = "https://www.cdcr.ca.gov/bph/2024/03/20/hearing-results-february-2024/"

df1 = getData(scheduleUrl)
df2 = getData(resultUrl)

df1 = df1[['CDC#','HEARING TYPE', 'PANEL', 'HEARING LOCATION', 'HEARING METHOD', 'SCHEDULED DATE', 'HEARING TIME']]
df2  = df2[['CDC#', 'SCHEDULED DATE', 'OFFENDER NAME', 'HEARING METHOD', 'COUNTY OF COMMITMENT', 'GOV CODE', 'HEARING TYPE', 'RESULT']]

merge_columns = ['CDC#', 'SCHEDULED DATE']
for col in df1.columns:
    if col in df2.columns and col not in merge_columns:
        df1.rename(columns={col: col + '(SCHEDULE TABLE)'}, inplace=True)
        df2.rename(columns={col: col + '(RESULT TABLE)'}, inplace=True)

merged_data = pd.merge(df1, df2, on=merge_columns, how='outer')



print(merged_data.columns)
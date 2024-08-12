import pandas as pd

# 엑셀 파일 경로
file1 = 'data_1202_20240812.xlsx'
file2 = 'data_1209_20240812.xlsx'
output_file = 'theme.xlsx'

# 두 엑셀 파일 읽기
df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)

# 'Code' 열을 기준으로 병합합니다. 'Theme' 열이 포함되어 있지 않을 경우 다른 열을 지정하세요.
merged_df = pd.merge(df1[['Code', 'Theme']], df2[['Code', 'Theme']], on='Code', how='outer')

# 'Theme' 열을 하나로 통합합니다. 우선 순위를 지정하여 어느 열의 'Theme'을 사용할지 결정합니다.
# 여기서는 df1의 'Theme'을 우선적으로 사용하고, df2의 'Theme'이 존재할 경우 덮어씁니다.
merged_df['Theme'] = merged_df['Theme_x'].combine_first(merged_df['Theme_y'])

# 불필요한 열 제거
merged_df = merged_df[['Code', 'Theme']]

# 병합된 데이터를 새로운 엑셀 파일로 저장
merged_df.to_excel(output_file, index=False)

print(f"파일이 성공적으로 저장되었습니다: {output_file}")